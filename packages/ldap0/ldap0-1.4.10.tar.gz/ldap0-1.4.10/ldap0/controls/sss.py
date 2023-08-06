# -*- coding: ascii -*-
"""
ldap0.controls.sss - classes for Server Side Sorting
(see RFC 2891)
"""

from pyasn1.type import univ, namedtype, tag, namedval, constraint
from pyasn1.codec.ber import encoder, decoder

from . import RequestControl, ResponseControl


__all__ = [
    'SSSRequestControl',
    'SSSResponseControl',
]


class SortKeyType(univ.Sequence):
    """
    SEQUENCE {
       attributeType   AttributeDescription,
       orderingRule    [0] MatchingRuleId OPTIONAL,
       reverseOrder    [1] BOOLEAN DEFAULT FALSE }
    """
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('attributeType', univ.OctetString()),
        namedtype.OptionalNamedType(
            'orderingRule',
            univ.OctetString().subtype(
                implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
            )
        ),
        namedtype.DefaultedNamedType(
            'reverseOrder',
            univ.Boolean(False).subtype(
                implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)
            )
        )
    )


class SortKeyListType(univ.SequenceOf):
    """
    SortKeyList ::= SEQUENCE OF SEQUENCE {
                     attributeType   AttributeDescription,
                     orderingRule    [0] MatchingRuleId OPTIONAL,
                     reverseOrder    [1] BOOLEAN DEFAULT FALSE }
    """
    componentType = SortKeyType()


class SSSRequestControl(RequestControl):
    """
    Order result server side

    >>> s = SSSRequestControl(ordering_rules=['-cn'])
    """
    controlType: str = '1.2.840.113556.1.4.473'

    def __init__(
            self,
            criticality: bool = False,
            ordering_rules=None,
        ):
        RequestControl.__init__(self, self.controlType, criticality)
        self.ordering_rules = ordering_rules
        for rule in ordering_rules:
            rule = rule.split(':')
            assert len(rule) < 3, 'syntax for ordering rule: [-]<attribute-type>[:ordering-rule]'

    def encode(self) -> bytes:
        p = SortKeyListType()
        for i, rule in enumerate(self.ordering_rules):
            q = SortKeyType()
            reverse_order = rule.startswith('-')
            if reverse_order:
                rule = rule[1:]
            try:
                attribute_type, ordering_rule = rule.split(':')
            except ValueError:
                attribute_type, ordering_rule = rule, None
            q.setComponentByName('attributeType', attribute_type.encode(self.encoding))
            if ordering_rule:
                q.setComponentByName('orderingRule', ordering_rule.encode(self.encoding))
            if reverse_order:
                q.setComponentByName('reverseOrder', 1)
            p.setComponentByPosition(i, q)
        return encoder.encode(p)


class SortResultType(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'sortResult',
            univ.Enumerated().subtype(
                namedValues=namedval.NamedValues(
                    ('success', 0),
                    ('operationsError', 1),
                    ('timeLimitExceeded', 3),
                    ('strongAuthRequired', 8),
                    ('adminLimitExceeded', 11),
                    ('noSuchAttribute', 16),
                    ('inappropriateMatching', 18),
                    ('insufficientAccessRights', 50),
                    ('busy', 51),
                    ('unwillingToPerform', 53),
                    ('other', 80)
                ),
                subtypeSpec=univ.Enumerated.subtypeSpec + \
                    constraint.SingleValueConstraint(0, 1, 3, 8, 11, 16, 18, 50, 51, 53, 80)
            )
        ),
        namedtype.OptionalNamedType(
            'attributeType',
            univ.OctetString().subtype(
                implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
            )
        )
    )


class SSSResponseControl(ResponseControl):
    controlType: str = '1.2.840.113556.1.4.474'

    def __init__(self, criticality=False):
        ResponseControl.__init__(self, self.controlType, criticality)

    def decode(self, encodedControlValue: bytes):
        p, rest = decoder.decode(encodedControlValue, asn1Spec=SortResultType())
        assert not rest, 'all data could not be decoded'
        sort_result = p.getComponentByName('sortResult')
        self.sortResult = int(sort_result)
        attribute_type = p.getComponentByName('attributeType')
        if attribute_type.hasValue():
            self.attributeType = attribute_type
        else:
            self.attributeType = None
