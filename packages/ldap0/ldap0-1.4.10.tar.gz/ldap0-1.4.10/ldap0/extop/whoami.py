# -*- coding: ascii -*-
"""
ldap0.extop.whoami - Classes for "Who am I?" extended operation
(see RFC 4532)
"""

from . import ExtendedRequest, ExtendedResponse


class WhoAmIRequest(ExtendedRequest):
    """
    Who Am I? extended request
    """

    requestName: str = '1.3.6.1.4.1.4203.1.11.3'


class WhoAmIResponse(ExtendedResponse):
    """
    Who Am I? extended response
    """

    responseName = None

    @classmethod
    def check_resp_name(cls, name):
        """
        work around MS AD returning obscure OID as responseName
        """
        return name in (cls.responseName, WhoAmIRequest.requestName)

    def decode(self, value: bytes):
        self.responseValue = value.decode(self.encoding, errors='strict')
