# -*- coding: ascii -*-
"""
ldap0.controls.simple - classes for some very simple LDAP controls
"""

import struct

from . import RequestControl, ResponseControl, LDAPControl


__all__ = [
    'AuthorizationIdentityRequestControl',
    'AuthorizationIdentityResponseControl',
    'BooleanControl',
    'ManageDSAITControl',
    'OctetStringInteger',
    'ProxyAuthzControl',
    'RelaxRulesControl',
    'ValueLessRequestControl',
]


class ValueLessRequestControl(RequestControl):
    """
    Base class for controls without a controlValue.
    The presence of the control in a LDAPv3 request changes the server's
    behaviour when processing the request simply based on the controlType.

    controlType
      OID of the request control
    criticality
      criticality request control
    """

    def __init__(self, controlType=None, criticality=False):
        RequestControl.__init__(
            self,
            controlType=controlType,
            criticality=criticality,
        )

    def encode(self) -> bytes:
        return None


class OctetStringInteger(LDAPControl):
    """
    Base class with controlValue being unsigend integer values

    integerValue
      Integer to be sent as OctetString
    """

    def __init__(self, controlType=None, criticality: bool = False, integerValue=None):
        LDAPControl.__init__(
            self,
            controlType=controlType,
            criticality=criticality,
        )
        self.integerValue = integerValue

    def encode(self) -> bytes:
        return struct.pack('!Q', self.integerValue)

    def decode(self, encodedControlValue: bytes):
        self.integerValue = struct.unpack('!Q', encodedControlValue)[0]


class BooleanControl(LDAPControl):
    """
    Base class for simple request controls with boolean control value.

    Constructor argument and class attribute:

    booleanValue
      Boolean (True/False or 1/0) which is the boolean controlValue.
    """
    boolean2ber = {
        1: b'\x01\x01\xFF',
        0: b'\x01\x01\x00',
    }
    ber2boolean = {
        b'\x01\x01\xFF': 1,
        b'\x01\x01\x00': 0,
    }

    def __init__(self, controlType=None, criticality: bool = False, booleanValue=False):
        LDAPControl.__init__(
            self,
            controlType=controlType,
            criticality=criticality,
        )
        self.booleanValue = booleanValue

    def encode(self) -> bytes:
        return self.boolean2ber[int(self.booleanValue)]

    def decode(self, encodedControlValue: bytes):
        self.booleanValue = bool(self.ber2boolean[encodedControlValue])


class ManageDSAITControl(ValueLessRequestControl):
    """
    Manage DSA IT Control
    """
    controlType: str = '2.16.840.1.113730.3.4.2'

    def __init__(self, criticality=False):
        ValueLessRequestControl.__init__(
            self,
            criticality=criticality,
        )


class RelaxRulesControl(ValueLessRequestControl):
    """
    Relax Rules Control
    """
    controlType: str = '1.3.6.1.4.1.4203.666.5.12'

    def __init__(self, criticality=False):
        ValueLessRequestControl.__init__(
            self,
            criticality=criticality,
        )


class ProxyAuthzControl(RequestControl):
    """
    Proxy Authorization Control

    authzId
      string containing the authorization ID indicating the identity
      on behalf which the server should process the request
    """
    controlType: str = '2.16.840.1.113730.3.4.18'

    def __init__(self, criticality: bool = False, authzId=''):
        RequestControl.__init__(
            self,
            criticality=criticality,
            encodedControlValue=authzId.encode(self.encoding),
        )


class AuthorizationIdentityRequestControl(ValueLessRequestControl):
    """
    Authorization Identity Request and Response Controls
    """
    controlType: str = '2.16.840.1.113730.3.4.16'

    def __init__(self, criticality=False):
        ValueLessRequestControl.__init__(
            self,
            criticality=criticality,
        )


class AuthorizationIdentityResponseControl(ResponseControl):
    """
    Authorization Identity Request and Response Controls

    Class attributes:

    authzId
        decoded authorization identity
    """
    controlType: str = '2.16.840.1.113730.3.4.15'

    def decode(self, encodedControlValue: bytes):
        self.authzId = encodedControlValue


class SubentriesControl(BooleanControl):
    """
    Subentries Control (RFC 3672)
    https://tools.ietf.org/html/rfc3672#section-3
    """
    controlType: str = '1.3.6.1.4.1.4203.1.10.1'

    def __init__(self, criticality: bool = False, booleanValue=False):
        BooleanControl.__init__(
            self,
            controlType=None,
            criticality=criticality,
            booleanValue=booleanValue
        )
