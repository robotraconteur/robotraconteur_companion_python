import pytest
from RobotRaconteurCompanion.Util.ServicePathUtil import encode_service_path_index, decode_service_path_index, \
    parse_service_path, build_service_path, ServicePathSegment


def test_encode_service_path_index():
    assert encode_service_path_index('index') == 'index'
    assert encode_service_path_index('index with spaces') == 'index%20with%20spaces'


def test_decode_service_path_index():
    assert decode_service_path_index('index') == 'index'
    assert decode_service_path_index('index%20with%20spaces') == 'index with spaces'


def test_parse_service_path():
    path = 'segment1.segment2[index].segment3'
    expected_result = [
        ServicePathSegment('segment1', None),
        ServicePathSegment('segment2', 'index'),
        ServicePathSegment('segment3', None)
    ]
    assert parse_service_path(path) == expected_result


def test_build_service_path():
    segments = [
        ServicePathSegment('segment1', None),
        ServicePathSegment('segment2', 'index'),
        ServicePathSegment('segment3', None)
    ]
    expected_result = 'segment1.segment2[index].segment3'
    assert build_service_path(segments) == expected_result
