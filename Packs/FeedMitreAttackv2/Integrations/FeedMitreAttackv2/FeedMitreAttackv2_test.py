import pytest
from test_data.mitre_test_data import ATTACK_PATTERN, COURSE_OF_ACTION, INTRUSION_SET, MALWARE, TOOL, ID_TO_NAME, \
    RELATION_1


@pytest.mark.parametrize('field_name, field_value, expected_result', [
    ('created', '2017-05-31T21:31:43.540Z', '2017-05-31T21:31:43.540Z'),
    ('created', '2019-04-25T20:53:07.719Z\n2019-04-25T20:53:07.814Z', '2019-04-25T20:53:07.719Z'),
    ('modified', '2017-05-31T21:31:43.540Z', '2017-05-31T21:31:43.540Z'),
    ('modified', '2020-03-16T15:38:37.650Z\n2020-01-17T16:45:24.252Z', '2020-03-16T15:38:37.650Z'),
])
def test_handle_multiple_dates_in_one_field(field_name, field_value, expected_result):
    from FeedMitreAttackv2 import handle_multiple_dates_in_one_field
    assert handle_multiple_dates_in_one_field(field_name, field_value) == expected_result


@pytest.mark.parametrize('indicator, expected_result', [
    ({"x_mitre_deprecated": True}, True),
    ({"revoked": True}, True),
    ({}, False)
])
def test_is_indicator_deprecated_or_revoked(indicator, expected_result):
    from FeedMitreAttackv2 import is_indicator_deprecated_or_revoked
    assert is_indicator_deprecated_or_revoked(indicator) == expected_result


@pytest.mark.parametrize('indicator_type, indicator_json, expected_result', [
    ('STIX Attack Pattern', ATTACK_PATTERN.get('response'), ATTACK_PATTERN.get('result')),
    ('Course of Action', COURSE_OF_ACTION.get('response'), COURSE_OF_ACTION.get('result')),
    ('Intrusion Set', INTRUSION_SET.get('response'), INTRUSION_SET.get('result')),
    ('STIX Malware', MALWARE.get('response'), MALWARE.get('result')),
    ('STIX Tool', TOOL.get('response'), TOOL.get('result'))
])
def test_map_fields_by_type(indicator_type, indicator_json, expected_result):
    from FeedMitreAttackv2 import map_fields_by_type
    assert map_fields_by_type(indicator_type, indicator_json) == expected_result


def test_create_relationship():
    from FeedMitreAttackv2 import create_relationship
    relation = create_relationship(RELATION_1.get('response'), ID_TO_NAME)
    relation._entity_a = 'entity a'
    relation._entity_a_type = 'STIX Malware'
    relation._entity_b = 'entity b'
    relation._entity_b_type = 'STIX Attack Pattern'
    relation._name = 'uses'
    relation._relation_type = 'IndicatorToIndicator'
    relation._reverse_name = 'used-by'
