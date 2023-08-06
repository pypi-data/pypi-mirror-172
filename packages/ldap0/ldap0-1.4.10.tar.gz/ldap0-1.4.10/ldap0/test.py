# -*- coding: ascii -*-
"""
ldap0.test - module for spawning test instances of OpenLDAP's slapd server
"""

import os
import socket
import time
import subprocess
import logging
import unittest
from typing import List

from urllib.parse import quote_plus

import _libldap0

from .base import encode_list
from .ldapobject import LDAPObject
from .functions import escape_format
from .filter import escape_str as escape_filter_str
from .ldif import LDIFParser
from .typehints import EntryStr

# a template string for generating simple slapd.conf file
SLAPD_CONF_TEMPLATE = r"""
moduleload back_%(database)s

include "%(schema_prefix)s/core.schema"
include "%(schema_prefix)s/cosine.schema"
include "%(schema_prefix)s/nis.schema"

serverID %(serverid)s
loglevel %(loglevel)s
allow bind_v2
sasl-secprops none
security ssf=0 simple_bind=0 sasl=0 transport=0

TLSVerifyClient allow
TLSProtocolMin 3.3
TLSCACertificateFile tests/tls/ca-chain.pem
TLSCertificateFile tests/tls/localhost.crt
TLSCertificateKeyFile tests/tls/localhost.key
TLSDHParamFile tests/tls/slapd-dhparams.pem

authz-regexp
  "gidnumber=%(root_gid)s\\+uidnumber=%(root_uid)s,cn=peercred,cn=external,cn=auth"
  "%(rootdn)s"

authz-regexp
  "uid=([a-zA-Z0-9_-]+),cn=(DIGEST-MD5|CRAM-MD5|PLAIN|SCRAM-SHA-1),cn=auth"
  "ldap:///%(suffix)s??sub?(cn=$1)"

database config
access to
  dn.subtree="cn=config"
    by dn.exact="%(rootdn)s" manage

database %(database)s
directory "%(directory)s"
suffix "%(suffix)s"
rootdn "%(rootdn)s"
rootpw "%(rootpw)s"

dbnosync

access to
  dn.subtree="%(suffix)s"
  attrs=userPassword
    by self =w
    by anonymous auth

access to
  dn.subtree="%(suffix)s"
    by * auth
"""

LOCALHOST = '127.0.0.1'

CONSOLE_LOG_FORMAT = '%(name)s %(asctime)s %(levelname)s %(message)s'


class SlapdObject:
    """
    Controller class for a slapd instance, OpenLDAP's server.

    This class creates a temporary data store for slapd, runs it
    listening on a private Unix domain socket and TCP port,
    and initialises it with a top-level entry and the root user.

    When a reference to an instance of this class is lost, the slapd
    server is shut down.
    """
    slapd_conf_template = SLAPD_CONF_TEMPLATE
    database = 'mdb'
    suffix = 'o=\xE4\xF6\xFC,dc=example,dc=org'
    root_cn = 'M\xE4nager'
    root_dn = 'cn=%s,%s' % (root_cn, suffix)
    root_pw = 'password'
    slapd_loglevel = [
        v.strip()
        for v in os.environ.get('SLAPD_LOGLEVEL', 'stats,stats2').split(',')
    ]
    # use SASL/EXTERNAL via LDAPI when invoking OpenLDAP CLI tools
    cli_sasl_external = True
    local_host = '127.0.0.1'
    testrunsubdirs = (
        'schema',
    )
    openldap_schema_files = (
        'core.schema',
        'cosine.schema',
        'nis.schema',
    )

    TMPDIR = os.environ.get('TMP', os.getcwd())
    BINDIR = os.environ.get('BIN', '/usr/bin')
    SCHEMADIR = os.environ.get('SCHEMA', '/etc/openldap/schema')
    PATH_LDAPADD = os.path.join(BINDIR, 'ldapadd')
    PATH_LDAPMODIFY = os.path.join(BINDIR, 'ldapmodify')
    PATH_LDAPWHOAMI = os.path.join(BINDIR, 'ldapwhoami')
    PATH_SLAPD = os.environ.get('SLAPD', '/usr/sbin/slapd')

    # time in secs to wait before trying to access slapd via LDAP (again)
    start_sleep = float(os.environ.get('START_SLEEP', '1.5'))

    def __init__(self):
        self._proc = None
        self._port = self._avail_tcp_port()
        self.server_id = self._port % 4096
        self.testrundir = os.path.join(self.TMPDIR, 'slapdtest-%d' % self._port)
        self._schema_prefix = os.path.join(self.testrundir, 'schema')
        self._slapd_conf = os.path.join(self.testrundir, 'slapd.conf')
        self._db_directory = os.path.join(self.testrundir, "openldap-data")
        self.ldap_uri = "ldap://%s:%d/" % (LOCALHOST, self._port)
        ldapi_path = os.path.join(self.testrundir, 'ldapi')
        self.ldapi_uri = "ldapi://%s" % quote_plus(ldapi_path)
        self._slapd_version = None

    @property
    def slapd_version(self):
        if self._slapd_version is None:
            self._slapd_version = '.'.join(self.get_slapd_version())
        return self._slapd_version

    def setup_rundir(self):
        """
        creates rundir structure

        for setting up a custom directory structure you have to override
        this method
        """
        os.mkdir(self.testrundir)
        os.mkdir(self._db_directory)
        self._create_sub_dirs(self.testrunsubdirs)
        self._ln_schema_files(self.openldap_schema_files, self.SCHEMADIR)

    def _cleanup_rundir(self):
        """
        Recursively delete whole directory specified by `path'
        """
        if not os.path.exists(self.testrundir):
            return
        logging.debug('clean-up %s', self.testrundir)
        for dirpath, dirnames, filenames in os.walk(
                self.testrundir,
                topdown=False
            ):
            for filename in filenames:
                logging.debug('remove %s', os.path.join(dirpath, filename))
                os.remove(os.path.join(dirpath, filename))
            for dirname in dirnames:
                logging.debug('rmdir %s', os.path.join(dirpath, dirname))
                os.rmdir(os.path.join(dirpath, dirname))
        os.rmdir(self.testrundir)
        logging.info('cleaned-up %s', self.testrundir)

    def _avail_tcp_port(self) -> int:
        """
        find an available port for TCP connection
        """
        sock = socket.socket()
        sock.bind((self.local_host, 0))
        port = sock.getsockname()[1]
        sock.close()
        logging.info('Found available port %d', port)
        return port

    def gen_config(self) -> str:
        """
        generates a slapd.conf and returns it as one string

        for generating specific static configuration files you have to
        override this method
        """
        config_dict = {
            'serverid': hex(self.server_id),
            'schema_prefix':self._schema_prefix,
            'loglevel': ' '.join(self.slapd_loglevel),
            'database': self.database,
            'directory': self._db_directory,
            'suffix': self.suffix,
            'rootdn': self.root_dn,
            'rootpw': self.root_pw,
            'root_uid': os.getuid(),
            'root_gid': os.getgid(),
        }
        return self.slapd_conf_template % config_dict

    def _create_sub_dirs(self, dir_names):
        """
        create sub-directories beneath self.testrundir
        """
        for dname in dir_names:
            dir_name = os.path.join(self.testrundir, dname)
            logging.debug('Create directory %s', dir_name)
            os.mkdir(dir_name)

    def _ln_schema_files(self, file_names, source_dir):
        """
        write symbolic links to original schema files
        """
        for fname in file_names:
            ln_source = os.path.join(source_dir, fname)
            ln_target = os.path.join(self._schema_prefix, fname)
            logging.debug('Create symlink %s -> %s', ln_source, ln_target)
            os.symlink(ln_source, ln_target)

    def _write_config(self):
        """Writes the slapd.conf file out, and returns the path to it."""
        logging.debug('Writing config to %s', self._slapd_conf)
        with open(self._slapd_conf, 'w', encoding='utf-8') as config_file:
            config_file.write(self.gen_config())
        logging.info('Wrote config to %s', self._slapd_conf)

    def _test_config(self):
        logging.debug('testing config %s', self._slapd_conf)
        popen_list = [
            self.PATH_SLAPD,
            '-T', 'test',
            '-f', self._slapd_conf,
            '-u',
        ]
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            popen_list.append('-v')
            popen_list.extend(['-d', 'config'])
        else:
            popen_list.append('-Q')
        proc = subprocess.Popen(popen_list)
        if proc.wait() != 0:
            raise RuntimeError("configuration test failed")
        logging.info("config ok: %s", self._slapd_conf)

    def get_slapd_version(self) -> tuple:
        """
        Determines slapd version
        """
        proc = subprocess.Popen(
            [self.PATH_SLAPD, '-V'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _, stderr_data = proc.communicate(None)
        return tuple(stderr_data.decode('utf-8').split('\n')[0].split(' ')[3].split('.'))

    def _start_slapd(self):
        """
        Spawns/forks the slapd process
        """
        slapd_args = [
            self.PATH_SLAPD,
            '-f', self._slapd_conf,
            '-h', '%s' % ' '.join((self.ldap_uri, self.ldapi_uri)),
        ]
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            slapd_args.extend(['-d', ','.join(self.slapd_loglevel)])
        else:
            slapd_args.extend(['-d', '0'])
        logging.info(
            'starting slapd %s: %r',
            '.'.join(self.get_slapd_version()),
            ' '.join(slapd_args),
        )
        self._proc = subprocess.Popen(slapd_args)
        # Waits until the LDAP server socket is open, or slapd crashed
        while True:
            if self._proc.poll() is not None:
                self._stopped()
                raise RuntimeError("slapd exited before opening port")
            time.sleep(self.start_sleep)
            try:
                logging.debug("slapd connection check to %s", self.ldapi_uri)
                self.ldapwhoami()
            except RuntimeError:
                pass
            else:
                return

    def start(self):
        """
        Starts the slapd server process running, and waits for it to come up.
        """

        if self._proc is None:
            # prepare directory structure
            self._cleanup_rundir()
            self.setup_rundir()
            self._write_config()
            self._test_config()
            self._start_slapd()
            logging.debug(
                'slapd with pid=%d listening on %s and %s',
                self._proc.pid, self.ldap_uri, self.ldapi_uri
            )

    def stop(self):
        """
        Stops the slapd server, and waits for it to terminate and cleans up
        """
        if self._proc is not None:
            logging.debug('stopping slapd with pid %d', self._proc.pid)
            self._proc.terminate()
            self.wait()
        self._cleanup_rundir()

    def restart(self):
        """
        Restarts the slapd server with same data
        """
        self._proc.terminate()
        self.wait()
        self._start_slapd()

    def wait(self):
        """Waits for the slapd process to terminate by itself."""
        if self._proc:
            self._proc.wait()
            self._stopped()

    def _stopped(self):
        """Called when the slapd server is known to have terminated"""
        if self._proc is not None:
            logging.info('slapd[%d] terminated', self._proc.pid)
            self._proc = None

    def _cli_auth_args(self) -> List[str]:
        if self.cli_sasl_external:
            authc_args = [
                '-Y', 'EXTERNAL',
            ]
            if not logging.getLogger().isEnabledFor(logging.DEBUG):
                authc_args.append('-Q')
        else:
            authc_args = [
                '-x',
                '-D', self.root_dn,
                '-w', self.root_pw,
            ]
        return authc_args

    def _cli_popen(self, ldapcommand, extra_args=None, ldap_uri=None, stdin_data=None):
        args = [
            ldapcommand,
            '-H', ldap_uri or self.ldapi_uri,
        ] + self._cli_auth_args() + (extra_args or [])
        logging.debug('Run command: %r', ' '.join(args))
        proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        logging.debug('stdin_data=%r', stdin_data)
        stdout_data, stderr_data = proc.communicate(stdin_data)
        if stdout_data is not None:
            logging.debug('stdout_data=%r', stdout_data)
        if stderr_data is not None:
            logging.debug('stderr_data=%r', stderr_data)
        if proc.wait() != 0:
            raise RuntimeError('ldapadd process failed')
        return stdout_data, stderr_data

    def ldapwhoami(self, extra_args=None):
        """
        Runs ldapwhoami on this slapd instance
        """
        self._cli_popen(self.PATH_LDAPWHOAMI, extra_args=extra_args)

    def ldapadd(self, ldif_data: bytes, extra_args=None):
        """
        Runs ldapadd on this slapd instance, passing it the ldif content
        """
        self._cli_popen(self.PATH_LDAPADD, extra_args=extra_args, stdin_data=ldif_data)

    def ldapmodify(self, ldif_data: bytes, extra_args=None):
        """
        Runs ldapadd on this slapd instance, passing it the ldif content
        """
        self._cli_popen(self.PATH_LDAPMODIFY, extra_args=extra_args, stdin_data=ldif_data)


class SlapdTestCase(unittest.TestCase):
    """
    test class which also clones or initializes a running slapd
    """

    server_class = SlapdObject
    ldap_object_class = LDAPObject
    server = None
    trace_level = int(os.environ.get('LDAP0_TRACE_LEVEL', '0'))

    def _open_ldap_conn(self, who=None, cred=None):
        """
        return a LDAPObject instance after simple bind
        """
        ldap_conn = self.ldap_object_class(
            self.server.ldap_uri,
            trace_level=self.trace_level,
        )
        ldap_conn.protocol_version = 3
        #ldap_conn.set_option(ldap0.OPT_REFERRALS, 0)
        ldap_conn.simple_bind_s(
            (who or self.server.root_dn),
            (cred or self.server.root_pw).encode('utf-8'),
        )
        return ldap_conn

    @classmethod
    def setUpClass(cls):
        logging.getLogger().setLevel(os.environ.get('LDAP0_LOG_LEVEL', 'WARN').upper())
        cls.server = cls.server_class()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        try:
            self._ldap_conn
        except AttributeError:
            # open local LDAP connection
            self._ldap_conn = self._open_ldap_conn()
            self.mdb_config_dn = self._ldap_conn.search_s(
                'cn=config',
                _libldap0.SCOPE_SUBTREE,
                escape_format(escape_filter_str, '(olcSuffix={0})', self.server.suffix),
            )[0].dn_s

    def enable_overlay(self, slapo_entry: EntryStr, schema_files=None, config_dn=None):
        logging.debug('Enable overlay with %r', slapo_entry)
        olc_overlay = slapo_entry['olcOverlay'][0]
        try:
            enabled_overlays = [
                val.split('}', 1)[1]
                for val in self._ldap_conn.read_s(
                    'cn=module{0},cn=config',
                    attrlist=['olcModuleLoad'],
                ).entry_s['olcModuleLoad']
            ]
            if olc_overlay in enabled_overlays:
                return
        except _libldap0.NO_SUCH_OBJECT:
            enabled_overlays = []

        schema_entries = []
        for schema_filename in schema_files or []:
            with open(os.path.join(self.server.SCHEMADIR, schema_filename), 'rb') as schema_file:
                ldif_parser = LDIFParser(schema_file)
                schema_entries.extend(ldif_parser.parse())
        try:
            for dn, entry in schema_entries:
                self._ldap_conn.add_s(
                    dn.decode('utf-8'),
                    {at.decode('ascii'): avs for at, avs in entry.items()}
                )
            if enabled_overlays:
                self._ldap_conn.modify_s(
                    'cn=module{0},cn=config',
                    [(_libldap0.MOD_ADD, b'olcModuleLoad', [olc_overlay.encode('utf-8')])]
                )
            else:
                self._ldap_conn.add_s(
                    'cn=module{0},cn=config',
                    {
                        'objectclass': ['olcModuleList'.encode('utf-8')],
                        'olcModuleload': [olc_overlay.encode('utf-8')],
                    }
                )
            self._ldap_conn.add_s(
                'olcOverlay={{0}}{0},{1}'.format(
                    olc_overlay,
                    config_dn or self.mdb_config_dn,
                ),
                {
                    at: encode_list(avs)
                    for at, avs in slapo_entry.items()
                },
            )
        except _libldap0.OTHER as ldap_err:
            self.skipTest(
                'installing slapo-%s failed: %s' % (
                    olc_overlay,
                    ldap_err,
                )
            )
