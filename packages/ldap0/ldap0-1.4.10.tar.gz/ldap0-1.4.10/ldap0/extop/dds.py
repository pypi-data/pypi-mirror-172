# -*- coding: ascii -*-
"""
ldap0.extop.dds - Classes for Dynamic Entries extended operations
(see RFC 2589)
"""

# Imports from pyasn1
from pyasn1.type import namedtype, univ, tag
from pyasn1.codec.der import encoder, decoder
from pyasn1_modules.rfc2251 import LDAPDN

from . import ExtendedRequest, ExtendedResponse


class RefreshRequest(ExtendedRequest):
    """
    Refresh Request
    (see https://tools.ietf.org/html/rfc2589#section-4.1)
    """
    __slots__ = (
        'entryName',
        'requestTtl',
    )
    requestName: str = '1.3.6.1.4.1.1466.101.119.1'
    defaultRequestTtl = 86400

    class RefreshRequestValue(univ.Sequence):
        """
        SEQUENCE {
            entryName  [0] LDAPDN,
            requestTtl [1] INTEGER
        }
        (see https://tools.ietf.org/html/rfc2589#section-4.1)
        """
        componentType = namedtype.NamedTypes(
            namedtype.NamedType(
                'entryName',
                LDAPDN().subtype(
                    implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
                )
            ),
            namedtype.NamedType(
                'requestTtl',
                univ.Integer().subtype(
                    implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)
                )
            ),
        )

    def __init__(self, entryName, requestTtl=None):
        ExtendedRequest.__init__(self)
        self.entryName = entryName
        self.requestTtl = requestTtl or self.defaultRequestTtl

    def encode(self) -> bytes:
        req_value = self.RefreshRequestValue()
        req_value.setComponentByName(
            'entryName',
            LDAPDN(self.entryName.encode(self.encoding)).subtype(
                implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
            )
        )
        req_value.setComponentByName(
            'requestTtl',
            univ.Integer(self.requestTtl).subtype(
                implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)
            )
        )
        return encoder.encode(req_value)


class RefreshResponse(ExtendedResponse):
    """
    Refresh Response
    (see https://tools.ietf.org/html/rfc2589#section-4.2)
    """
    __slots__ = (
        'responseTtl',
    )
    responseName = '1.3.6.1.4.1.1466.101.119.1'

    class RefreshResponseValue(univ.Sequence):
        """
        SEQUENCE {
            responseTtl [1] INTEGER
        }
        """
        componentType = namedtype.NamedTypes(
            namedtype.NamedType(
                'responseTtl',
                univ.Integer().subtype(
                    implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)
                )
            )
        )

    def decode(self, value: bytes):
        refresh_response, _ = decoder.decode(
            value,
            asn1Spec=self.RefreshResponseValue(),
        )
        self.responseTtl = int(refresh_response.getComponentByName('responseTtl'))
        return self.responseTtl
