# -*- coding: ascii -*-
"""
ldap0.controls.pagedresults - classes for Simple Paged control
(see RFC 2696)
"""

# Imports from pyasn1
from pyasn1.type import namedtype, univ
from pyasn1.codec.ber import encoder, decoder
from pyasn1_modules.rfc2251 import LDAPString

from . import RequestControl, ResponseControl


__all__ = [
    'SimplePagedResultsControl'
]

class SimplePagedResultsControl(RequestControl, ResponseControl):
    controlType: str = '1.2.840.113556.1.4.319'

    class PagedResultsControlValue(univ.Sequence):
        componentType = namedtype.NamedTypes(
            namedtype.NamedType('size', univ.Integer()),
            namedtype.NamedType('cookie', LDAPString()),
        )

    def __init__(self, criticality: bool = False, size=10, cookie=''):
        RequestControl.__init__(self, criticality=criticality)
        self.size = size
        self.cookie = cookie or b''

    def encode(self) -> bytes:
        pc = self.PagedResultsControlValue()
        pc.setComponentByName('size', univ.Integer(self.size))
        pc.setComponentByName('cookie', LDAPString(self.cookie))
        return encoder.encode(pc)

    def decode(self, encodedControlValue: bytes):
        decodedValue, _ = decoder.decode(
            encodedControlValue,
            asn1Spec=self.PagedResultsControlValue(),
        )
        self.size = int(decodedValue.getComponentByName('size'))
        self.cookie = decodedValue.getComponentByName('cookie')
