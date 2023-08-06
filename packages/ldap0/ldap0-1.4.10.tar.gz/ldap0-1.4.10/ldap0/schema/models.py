# -*- coding: ascii -*-
"""
ldap0.schema.models - support for subSchemaSubEntry information
"""

from collections.abc import MutableSet
from collections import UserDict, OrderedDict
from typing import Any, Mapping, Sequence

from ..cidict import CIDict
from .parse import split_tokens, extract_tokens


__all__ = [
    'AttributeType',
    'DITContentRule',
    'DITStructureRule',
    'Entry',
    'LDAPSyntax',
    'MatchingRule',
    'MatchingRuleUse',
    'NameForm',
    'ObjectClass',
    'SchemaElement',
    'SchemaElementOIDSet',
    'NOT_HUMAN_READABLE_LDAP_SYNTAXES',
    'OBJECTCLASS_KIND_STR',
]

#TokenDefaults = Mapping[str, Union[int, str, Tuple[Union[None, str]]]]
TokenDefaults = Mapping[str, Any]

NOT_HUMAN_READABLE_LDAP_SYNTAXES = {
    '1.3.6.1.4.1.1466.115.121.1.4',  # Audio
    '1.3.6.1.4.1.1466.115.121.1.5',  # Binary
    '1.3.6.1.4.1.1466.115.121.1.8',  # Certificate
    '1.3.6.1.4.1.1466.115.121.1.9',  # Certificate List
    '1.3.6.1.4.1.1466.115.121.1.10', # Certificate Pair
    '1.3.6.1.4.1.1466.115.121.1.23', # G3 FAX
    '1.3.6.1.4.1.1466.115.121.1.28', # JPEG
    '1.3.6.1.4.1.1466.115.121.1.40', # Octet String
    '1.3.6.1.4.1.1466.115.121.1.49', # Supported Algorithm
}

ATTRIBUTE_USAGE = CIDict({
    'userApplication': 0, # work-around for non-compliant schema
    'userApplications': 0,
    'directoryOperation': 1,
    'distributedOperation': 2,
    'dSAOperation': 3,
})

OBJECTCLASS_KIND_STR = {
    0: 'STRUCTURAL',
    1: 'ABSTRACT',
    2: 'AUXILIARY'
}


class SchemaElement:
    """
    Base class for all schema element classes. Not used directly!

    Arguments:

    schema_element_str
      String which contains the schema element description to be parsed.

    Class attributes:

    schema_attribute
      LDAP attribute type containing a certain schema element description
    token_defaults
      Dictionary internally used by the schema element parser
      containing the defaults for certain schema description key-words
    """
    __slots__ = (
        'oid',
        'desc',
        'obsolete',
    )
    token_defaults: TokenDefaults = {
        'DESC':(None,),
    }
    oid: str
    desc: str

    def __init__(self, schema_element_str=None):
        if schema_element_str:
            tkl = split_tokens(schema_element_str)
            self.set_id(tkl[1])
            opts = extract_tokens(tkl, self.token_defaults)
            self._set_attrs(opts)

    def _set_attrs(self, opts):
        self.desc = opts['DESC'][0]

    def set_id(self, element_id):
        self.oid = element_id

    def get_id(self):
        return self.oid

    @staticmethod
    def key_attr(key, value, quoted=0):
        assert value is None or isinstance(value, str), \
            TypeError("value has to be of str, was %r" % value)
        if not value:
            return ""
        if quoted:
            return " %s '%s'" % (key, value.replace("'", "\\'"))
        return " %s %s" % (key, value)

    @staticmethod
    def key_list(key, values, sep=' ', quoted=0):
        assert isinstance(values, tuple), TypeError("values has to be a tuple, was %r" % values)
        if not values:
            return ''
        if quoted:
            quoted_values = ["'%s'" % value.replace("'", "\\'") for value in values]
        else:
            quoted_values = values
        if len(values) == 1:
            return ' %s %s' % (key, quoted_values[0])
        return ' %s ( %s )' % (key, sep.join(quoted_values))

    def __str__(self):
        result = [str(self.oid)]
        result.append(self.key_attr('DESC', self.desc, quoted=1))
        return '( %s )' % ''.join(result)


class ObjectClass(SchemaElement):
    """
    Arguments:

    schema_element_str
      String containing an ObjectClassDescription

    Class attributes:

    oid
      OID assigned to the object class
    names
      This list of strings contains all NAMEs of the object class
    desc
      This string contains description text (DESC) of the object class
    obsolete
      Integer flag (0 or 1) indicating whether the object class is marked
      as OBSOLETE in the schema
    must
      This list of strings contains NAMEs or OIDs of all attributes
      an entry of the object class must have
    may
      This list of strings contains NAMEs or OIDs of additional attributes
      an entry of the object class may have
    kind
      Kind of an object class:
      0 = STRUCTURAL,
      1 = ABSTRACT,
      2 = AUXILIARY
    sup
      This list of strings contains NAMEs or OIDs of object classes
      this object class is derived from
    """
    __slots__ = (
        'names',
        'obsolete',
        'sup',
        'must',
        'may',
        'kind',
    )
    schema_attribute = 'objectClasses'
    token_defaults: TokenDefaults = {
        'NAME': (()),
        'DESC': (None,),
        'OBSOLETE': None,
        'SUP': (()),
        'STRUCTURAL': None,
        'AUXILIARY': None,
        'ABSTRACT': None,
        'MUST': (()),
        'MAY': ()
    }
    names: Sequence[str]

    def _set_attrs(self, opts):
        self.obsolete = opts['OBSOLETE'] is not None
        self.names = opts['NAME']
        self.desc = opts['DESC'][0]
        self.must = opts['MUST']
        self.may = opts['MAY']
        # Default is STRUCTURAL, see RFC 4512
        self.kind = 0
        if opts['ABSTRACT'] is not None:
            self.kind = 1
        elif opts['AUXILIARY'] is not None:
            self.kind = 2
        if self.kind == 0 and not opts['SUP'] and self.oid != '2.5.6.0':
            # STRUCTURAL object classes are sub-classes of 'top' by default
            self.sup = ('top',)
        else:
            self.sup = opts['SUP']

    def __str__(self):
        result = [str(self.oid)]
        result.append(self.key_list('NAME', self.names, quoted=1))
        result.append(self.key_attr('DESC', self.desc, quoted=1))
        result.append(self.key_list('SUP', self.sup, sep=' $ '))
        result.append({0:'', 1:' OBSOLETE'}[self.obsolete])
        result.append(' %s' % OBJECTCLASS_KIND_STR[self.kind])
        result.append(self.key_list('MUST', self.must, sep=' $ '))
        result.append(self.key_list('MAY', self.may, sep=' $ '))
        return '( %s )' % ''.join(result)


class AttributeType(SchemaElement):
    """
    Arguments:

    schema_element_str
      String containing an AttributeTypeDescription

    Class attributes:

    oid
      OID assigned to the attribute type
    names
      This list of strings contains all NAMEs of the attribute type
    desc
      This string contains description text (DESC) of the attribute type
    obsolete
      Integer flag (0 or 1) indicating whether the attribute type is marked
      as OBSOLETE in the schema
    single_value
      Integer flag (0 or 1) indicating whether the attribute must
      have only one value
    syntax
      String contains OID of the LDAP syntax assigned to the attribute type
    no_user_mod
      Integer flag (0 or 1) indicating whether the attribute is modifiable
      by a client application
    equality
      String contains NAME or OID of the matching rule used for
      checking whether attribute values are equal
    substr
      String contains NAME or OID of the matching rule used for
      checking whether an attribute value contains another value
    ordering
      String contains NAME or OID of the matching rule used for
      checking whether attribute values are lesser-equal than
    usage
      USAGE of an attribute type:
      0 = userApplications
      1 = directoryOperation,
      2 = distributedOperation,
      3 = dSAOperation
    sup
      This list of strings contains NAMEs or OIDs of attribute types
      this attribute type is derived from
    """
    __slots__ = (
        'names',
        'obsolete',
        'sup',
        'equality',
        'ordering',
        'syntax',
        'syntax_len',
        'single_value',
        'collective',
        'substr',
        'x_origin',
        'x_ordered',
        'no_user_mod',
        'usage',
    )
    schema_attribute = 'attributeTypes'
    token_defaults: TokenDefaults = {
        'NAME': (()),
        'DESC': (None,),
        'OBSOLETE': None,
        'SUP': (()),
        'EQUALITY': (None,),
        'ORDERING': (None,),
        'SUBSTR': (None,),
        'SYNTAX': (None,),
        'SINGLE-VALUE': None,
        'COLLECTIVE': None,
        'NO-USER-MODIFICATION': None,
        'USAGE': ('userApplications',),
        'X-ORIGIN': (None,),
        'X-ORDERED': (None,),
    }

    def _set_attrs(self, opts):
        self.names = opts['NAME']
        self.desc = opts['DESC'][0]
        self.obsolete = opts['OBSOLETE'] is not None
        self.sup = opts['SUP']
        self.equality = opts['EQUALITY'][0]
        self.ordering = opts['ORDERING'][0]
        self.substr = opts['SUBSTR'][0]
        self.x_origin = opts['X-ORIGIN'][0]
        self.x_ordered = opts['X-ORDERED'][0]
        try:
            syntax = opts['SYNTAX'][0]
        except IndexError:
            self.syntax = None
            self.syntax_len = None
        else:
            if syntax is None:
                self.syntax = None
                self.syntax_len = None
            else:
                try:
                    self.syntax, syntax_len = opts['SYNTAX'][0].split("{")
                except ValueError:
                    self.syntax = opts['SYNTAX'][0]
                    self.syntax_len = None
                else:
                    self.syntax_len = int(syntax_len[:-1])
        self.single_value = opts['SINGLE-VALUE'] is not None
        self.collective = opts['COLLECTIVE'] is not None
        self.no_user_mod = opts['NO-USER-MODIFICATION'] is not None
        self.usage = ATTRIBUTE_USAGE.get(opts['USAGE'][0], 0)

    def __str__(self):
        result = [str(self.oid)]
        result.append(self.key_list('NAME', self.names, quoted=1))
        result.append(self.key_attr('DESC', self.desc, quoted=1))
        result.append(self.key_list('SUP', self.sup, sep=' $ '))
        result.append({0:'', 1:' OBSOLETE'}[self.obsolete])
        result.append(self.key_attr('EQUALITY', self.equality))
        result.append(self.key_attr('ORDERING', self.ordering))
        result.append(self.key_attr('SUBSTR', self.substr))
        result.append(self.key_attr('SYNTAX', self.syntax))
        if self.syntax_len is not None:
            result.append(('{%d}' % (self.syntax_len))*(self.syntax_len > 0))
        result.append({0:'', 1:' SINGLE-VALUE'}[self.single_value])
        result.append({0:'', 1:' COLLECTIVE'}[self.collective])
        result.append({0:'', 1:' NO-USER-MODIFICATION'}[self.no_user_mod])
        result.append(
            {
                0: "",
                1: " USAGE directoryOperation",
                2: " USAGE distributedOperation",
                3: " USAGE dSAOperation",
            }[self.usage]
        )
        result.append(self.key_attr('X-ORIGIN', self.x_origin, quoted=1))
        result.append(self.key_attr('X-ORDERED', self.x_ordered, quoted=1))
        return '( %s )' % ''.join(result)


class LDAPSyntax(SchemaElement):
    """
    SyntaxDescription

    oid
      OID assigned to the LDAP syntax
    desc
      This string contains description text (DESC) of the LDAP syntax
    not_human_readable
      Integer flag (0 or 1) indicating whether the attribute type is marked
      as not human-readable (X-NOT-HUMAN-READABLE)
    """
    __slots__ = (
        'x_subst',
        'not_human_readable',
        'x_binary_transfer_required',
    )
    schema_attribute = 'ldapSyntaxes'
    token_defaults: TokenDefaults = {
        'DESC': (None,),
        'X-NOT-HUMAN-READABLE': (None,),
        'X-BINARY-TRANSFER-REQUIRED': (None,),
        'X-SUBST': (None,),
    }

    def _set_attrs(self, opts):
        self.desc = opts['DESC'][0]
        self.x_subst = opts['X-SUBST'][0]
        self.not_human_readable = \
            self.oid in NOT_HUMAN_READABLE_LDAP_SYNTAXES or \
            opts['X-NOT-HUMAN-READABLE'][0] == 'TRUE'
        self.x_binary_transfer_required = opts['X-BINARY-TRANSFER-REQUIRED'][0] == 'TRUE'

    def __str__(self):
        result = [str(self.oid)]
        result.append(self.key_attr('DESC', self.desc, quoted=1))
        result.append(self.key_attr('X-SUBST', self.x_subst, quoted=1))
        result.append(
            {0:'', 1:" X-NOT-HUMAN-READABLE 'TRUE'"}[self.not_human_readable]
        )
        result.append(
            {0:'', 1:" X-BINARY-TRANSFER-REQUIRED 'TRUE'"}[self.x_binary_transfer_required]
        )
        return '( %s )' % ''.join(result)


class MatchingRule(SchemaElement):
    """
    Arguments:

    schema_element_str
      String containing an MatchingRuleDescription

    Class attributes:

    oid
      OID assigned to the matching rule
    names
      This list of strings contains all NAMEs of the matching rule
    desc
      This string contains description text (DESC) of the matching rule
    obsolete
      Integer flag (0 or 1) indicating whether the matching rule is marked
      as OBSOLETE in the schema
    syntax
      String contains OID of the LDAP syntax this matching rule is usable with
    """
    __slots__ = (
        'names',
        'syntax',
    )
    schema_attribute = 'matchingRules'
    token_defaults: TokenDefaults = {
        'NAME': (()),
        'DESC': (None,),
        'OBSOLETE': None,
        'SYNTAX': (None,),
    }

    def _set_attrs(self, opts):
        self.names = opts['NAME']
        self.desc = opts['DESC'][0]
        self.obsolete = opts['OBSOLETE'] is not None
        self.syntax = opts['SYNTAX'][0]

    def __str__(self):
        result = [str(self.oid)]
        result.append(self.key_list('NAME', self.names, quoted=1))
        result.append(self.key_attr('DESC', self.desc, quoted=1))
        result.append({0:'', 1:' OBSOLETE'}[self.obsolete])
        result.append(self.key_attr('SYNTAX', self.syntax))
        return '( %s )' % ''.join(result)


class MatchingRuleUse(SchemaElement):
    """
    Arguments:

    schema_element_str
      String containing an MatchingRuleUseDescription

    Class attributes:

    oid
      OID of the accompanying matching rule
    names
      This list of strings contains all NAMEs of the matching rule
    desc
      This string contains description text (DESC) of the matching rule
    obsolete
      Integer flag (0 or 1) indicating whether the matching rule is marked
      as OBSOLETE in the schema
    applies
      This list of strings contains NAMEs or OIDs of attribute types
      for which this matching rule is used
    """
    __slots__ = (
        'names',
        'applies',
    )
    schema_attribute = 'matchingRuleUse'
    token_defaults: TokenDefaults = {
        'NAME': (()),
        'DESC': (None,),
        'OBSOLETE': None,
        'APPLIES': (()),
    }

    def _set_attrs(self, opts):
        self.names = opts['NAME']
        self.desc = opts['DESC'][0]
        self.obsolete = opts['OBSOLETE'] is not None
        self.applies = opts['APPLIES']

    def __str__(self):
        result = [str(self.oid)]
        result.append(self.key_list('NAME', self.names, quoted=1))
        result.append(self.key_attr('DESC', self.desc, quoted=1))
        result.append({0:'', 1:' OBSOLETE'}[self.obsolete])
        result.append(self.key_list('APPLIES', self.applies, sep=' $ '))
        return '( %s )' % ''.join(result)


class DITContentRule(SchemaElement):
    """
    Arguments:

    schema_element_str
      String containing an DITContentRuleDescription

    Class attributes:

    oid
      OID of the accompanying structural object class
    names
      This list of strings contains all NAMEs of the DIT content rule
    desc
      This string contains description text (DESC) of the DIT content rule
    obsolete
      Integer flag (0 or 1) indicating whether the DIT content rule is marked
      as OBSOLETE in the schema
    aux
      This list of strings contains NAMEs or OIDs of all auxiliary
      object classes usable in an entry of the object class
    must
      This list of strings contains NAMEs or OIDs of all attributes
      an entry of the object class must have which may extend the
      list of required attributes of the object classes of an entry
    may
      This list of strings contains NAMEs or OIDs of additional attributes
      an entry of the object class may have which may extend the
      list of optional attributes of the object classes of an entry
    nots
      This list of strings contains NAMEs or OIDs of attributes which
      may not be present in an entry of the object class
    """
    __slots__ = (
        'names',
        'aux',
        'must',
        'may',
        'nots',
    )
    schema_attribute = 'dITContentRules'
    token_defaults: TokenDefaults = {
        'NAME': (()),
        'DESC': (None,),
        'OBSOLETE': None,
        'AUX': (()),
        'MUST': (()),
        'MAY': (()),
        'NOT': (()),
    }

    def _set_attrs(self, opts):
        self.names = opts['NAME']
        self.desc = opts['DESC'][0]
        self.obsolete = opts['OBSOLETE'] is not None
        self.aux = opts['AUX']
        self.must = opts['MUST']
        self.may = opts['MAY']
        self.nots = opts['NOT']

    def __str__(self):
        result = [str(self.oid)]
        result.append(self.key_list('NAME', self.names, quoted=1))
        result.append(self.key_attr('DESC', self.desc, quoted=1))
        result.append({0:'', 1:' OBSOLETE'}[self.obsolete])
        result.append(self.key_list('AUX', self.aux, sep=' $ '))
        result.append(self.key_list('MUST', self.must, sep=' $ '))
        result.append(self.key_list('MAY', self.may, sep=' $ '))
        result.append(self.key_list('NOT', self.nots, sep=' $ '))
        return '( %s )' % ''.join(result)


class DITStructureRule(SchemaElement):
    """
    Arguments:

    schema_element_str
      String containing an DITStructureRuleDescription

    Class attributes:

    ruleid
      rule ID of the DIT structure rule (only locally unique)
    names
      This list of strings contains all NAMEs of the DIT structure rule
    desc
      This string contains description text (DESC) of the DIT structure rule
    obsolete
      Integer flag (0 or 1) indicating whether the DIT content rule is marked
      as OBSOLETE in the schema
    form
      List of strings with NAMEs or OIDs of associated name forms
    sup
      List of strings with NAMEs or OIDs of allowed structural object classes
      of superior entries in the DIT
    """
    __slots__ = (
        'ruleid',
        'names',
        'sup',
        'form',
    )
    schema_attribute = 'dITStructureRules'
    token_defaults: TokenDefaults = {
        'NAME': (()),
        'DESC': (None,),
        'OBSOLETE': None,
        'FORM': (None,),
        'SUP': (()),
    }
    ruleid: str

    def set_id(self, element_id):
        self.ruleid = element_id

    def get_id(self):
        return self.ruleid

    def _set_attrs(self, opts):
        self.names = opts['NAME']
        self.desc = opts['DESC'][0]
        self.obsolete = opts['OBSOLETE'] is not None
        self.form = opts['FORM'][0]
        self.sup = opts['SUP']

    def __str__(self):
        result = [str(self.ruleid)]
        result.append(self.key_list('NAME', self.names, quoted=1))
        result.append(self.key_attr('DESC', self.desc, quoted=1))
        result.append({0:'', 1:' OBSOLETE'}[self.obsolete])
        result.append(self.key_attr('FORM', self.form, quoted=0))
        result.append(self.key_list('SUP', self.sup, sep=' $ '))
        return '( %s )' % ''.join(result)


class NameForm(SchemaElement):
    """
    Arguments:

    schema_element_str
      String containing an NameFormDescription

    Class attributes:

    oid
      OID of the name form
    names
      This list of strings contains all NAMEs of the name form
    desc
      This string contains description text (DESC) of the name form
    obsolete
      Integer flag (0 or 1) indicating whether the name form is marked
      as OBSOLETE in the schema
    form
      List of strings with NAMEs or OIDs of associated name forms
    oc
      String with NAME or OID of structural object classes this name form
      is usable with
    must
      This list of strings contains NAMEs or OIDs of all attributes
      an RDN must contain
    may
      This list of strings contains NAMEs or OIDs of additional attributes
      an RDN may contain
    """
    __slots__ = (
        'names',
        'oc',
        'must',
        'may',
    )
    schema_attribute = 'nameForms'
    token_defaults: TokenDefaults = {
        'NAME': (()),
        'DESC': (None,),
        'OBSOLETE': None,
        'OC': (None,),
        'MUST': (()),
        'MAY': (()),
    }

    def _set_attrs(self, opts):
        self.names = opts['NAME']
        self.desc = opts['DESC'][0]
        self.obsolete = opts['OBSOLETE'] is not None
        self.oc = opts['OC'][0]
        self.must = opts['MUST']
        self.may = opts['MAY']

    def __str__(self):
        result = [str(self.oid)]
        result.append(self.key_list('NAME', self.names, quoted=1))
        result.append(self.key_attr('DESC', self.desc, quoted=1))
        result.append({0:'', 1:' OBSOLETE'}[self.obsolete])
        result.append(self.key_attr('OC', self.oc))
        result.append(self.key_list('MUST', self.must, sep=' $ '))
        result.append(self.key_list('MAY', self.may, sep=' $ '))
        return '( %s )' % ''.join(result)


class SchemaElementOIDSet(MutableSet):
    """
    set-like class which handles OIDs and NAMEs of schema elements
    """

    def __init__(self, schema, se_class, nameoroids):
        self._schema = schema
        self._se_class = se_class
        self._nameoroid_dict = OrderedDict()
        self.update(nameoroids)

    def __iter__(self):
        for key in self._nameoroid_dict.keys():
            yield key

    def __len__(self):
        return len(self._nameoroid_dict)

    def _key_oid(self, nameoroid):
        return self._schema.get_oid(self._se_class, nameoroid, raise_keyerror=False).lower()

    def discard(self, nameoroid):
        try:
            del self._nameoroid_dict[self._key_oid(nameoroid)]
        except KeyError:
            pass

    def __contains__(self, nameoroid):
        return self._key_oid(nameoroid) in self._nameoroid_dict

    def intersection(self, s):
        return SchemaElementOIDSet(
            self._schema,
            self._se_class,
            [
                i
                for i in s
                if i in self
            ]
        )

    def add(self, se_name):
        se_name = se_name.strip()
        if not se_name:
            return
        if se_name[0] == '@':
            if self._se_class != AttributeType:
                raise ValueError('@-form only possible with class AttributeType')
            must_attr, may_attr = self._schema.attribute_types(
                (se_name[1:],),
                attr_type_filter=None,
                raise_keyerror=True,
                ignore_dit_content_rule=True
            )
            se_list = [
                (se_oid, (se_obj.names or [se_oid])[0])
                for se_oid, se_obj in list(must_attr.items()) + list(may_attr.items())
            ]
        else:
            se_list = [(self._key_oid(se_name), se_name)]
        for se_oid, se_name0 in se_list:
            if not se_oid in self._nameoroid_dict:
                self._nameoroid_dict[se_oid] = se_name0
        # end of add()

    def update(self, seq):
        for item in seq:
            self.add(item)

    @property
    def names(self):
        return list(self._nameoroid_dict.values())


class Entry(UserDict):
    """
    Schema-aware implementation of an LDAP entry class.

    Mainly it holds the attributes in a string-keyed dictionary with
    the OID as key.
    """

    def __init__(self, schema, dn, entry):
        self._keytuple2attrtype = {}
        self._attrtype2keytuple = {}
        self._s = schema
        self.dn = dn
        UserDict.__init__(self, {})
        self.update(entry)

    def name2key(self, nameoroid):
        """
        Return tuple of OID and all sub-types of attribute type specified
        in nameoroid.
        """
        if isinstance(nameoroid, tuple):
            return nameoroid
        try:
            # Mapping already in cache
            return self._attrtype2keytuple[nameoroid]
        except KeyError:
            # Mapping has to be constructed
            noid_l = nameoroid.lower().split(';')
            oid = self._s.get_oid(AttributeType, noid_l[0])
            if oid.lower() == 'entrydn':
                oid = '1.3.6.1.1.20'
            self._attrtype2keytuple[nameoroid] = (oid,)+tuple(noid_l[1:])
            return self._attrtype2keytuple[nameoroid]

    def __contains__(self, nameoroid):
        return self.name2key(nameoroid) in self.data

    def __getitem__(self, nameoroid):
        key = self.name2key(nameoroid)
        try:
            return self.data[key]
        except KeyError as err:
            if (
                    key[0] == '1.3.6.1.1.20' and
                    self.dn is not None
                ):
                return [self.dn.encode('utf-8')]
            raise err

    def __setitem__(self, nameoroid, attr_values):
        if isinstance(nameoroid, bytes):
            nameoroid = nameoroid.decode('ascii')
        key = self.name2key(nameoroid)
        self._keytuple2attrtype[key] = nameoroid
        self.data[key] = attr_values

    def __delitem__(self, nameoroid):
        key = self.name2key(nameoroid)
        del self._keytuple2attrtype[key]
        del self.data[key]

    def __iter__(self):
        for key in self.data.keys():
            yield self._keytuple2attrtype[key]

    def has_key(self, key):
        raise NotImplementedError('do not use %s.has_key() method' % (self.__class__.__name__,))

    def keys(self):
        return self.__iter__()

    def items(self):
        for k in self.keys():
            yield (k, self[k])

    def attribute_types(
            self,
            attr_type_filter=None,
            raise_keyerror=1
        ):
        """
        Convenience wrapper around SubSchema.attribute_types() which
        passes object classes of this particular entry as argument to
        SubSchema.attribute_types()
        """
        return self._s.attribute_types(
            self.object_class_oid_set(),
            attr_type_filter,
            raise_keyerror,
        )

    def object_class_oid_set(self):
        try:
            object_classes = [
                oc.decode('ascii')
                for oc in self.__getitem__('objectClass')
            ]
        except KeyError:
            object_classes = []
        return SchemaElementOIDSet(self._s, ObjectClass, object_classes)

    def get_structural_oc(self):
        try:
            structural_object_class_oid = self._s.get_oid(
                ObjectClass,
                self.__getitem__('structuralObjectClass')[-1].decode('ascii')
            )
        except (KeyError, IndexError):
            try:
                structural_object_class_oid = self._s.get_structural_oc(
                    [av.decode('ascii') for av in self.__getitem__('objectClass')]
                )
            except KeyError:
                return None
        return structural_object_class_oid

    def get_possible_dit_structure_rules(self, dn):
        try:
            structural_oc = self.get_structural_oc()
        except KeyError:
            return None
        else:
            return self._s.get_possible_dit_structure_rules(dn, structural_oc)

    def get_rdn_templates(self):
        return self._s.get_rdn_templates(self.get_structural_oc())
