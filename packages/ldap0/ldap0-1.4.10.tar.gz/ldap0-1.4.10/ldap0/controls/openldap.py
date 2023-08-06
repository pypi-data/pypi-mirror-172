# -*- coding: ascii -*-
"""
ldap0.controls.openldap - classes for OpenLDAP-specific controls
"""

from pyasn1.type import univ
from pyasn1.codec.ber import decoder

from . import ResponseControl
from .simple import ValueLessRequestControl

__all__ = [
    'SearchNoOpControl',
]


class SearchNoOpControl(ValueLessRequestControl, ResponseControl):
    """
    No-op control attached to search operations implementing sort of a
    count operation

    see https://bugs.openldap.org/show_bug.cgi?id=6598#followup4
    """
    controlType: str = '1.3.6.1.4.1.4203.666.5.18'

    class SearchNoOpControlValue(univ.Sequence):
        pass

    def decode(self, encodedControlValue: bytes):
        decodedValue, _ = decoder.decode(
            encodedControlValue,
            asn1Spec=self.SearchNoOpControlValue(),
        )
        self.resultCode = int(decodedValue[0])
        self.numSearchResults = int(decodedValue[1])
        self.numSearchContinuations = int(decodedValue[2])
