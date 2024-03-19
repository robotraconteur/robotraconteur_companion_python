import urllib.parse
import string
from collections import namedtuple


def encode_service_path_index(index):
    """
    Encode a service path index for use in a Robot Raconteur service path

    :param index: The index to encode
    :type index: str
    :return: The encoded index
    :rtype: str
    """
    return urllib.parse.quote(index, safe=string.ascii_letters + string.digits)


def decode_service_path_index(index):
    """
    Decode a service path index from a Robot Raconteur service path

    :param index: The index to decode
    :type index: str
    :return: The decoded index
    :rtype: str
    """
    return urllib.parse.unquote(index)


ServicePathSegment = namedtuple('ServicePathSegment', ['name', 'index'])
ServicePathSegment.__doc__ = """
A named tuple representing a segment in a service path.

Attributes:
    name (str): The name of the service path segment.
    index (str): The index of the service path segment or None if the segment has no index.
"""


def parse_service_path(path):
    """
    Parse a Robot Raconteur service path into segments

    :param path: The service path to parse
    :type path: str
    :return: The parsed service path segments
    :rtype: List[ServicePathSegment]
    """
    segments = path.split('.')
    parsed_segments = []
    for segment in segments:
        if '[' in segment:
            name, index = segment.split('[')
            index = index[:-1]
            parsed_segments.append(ServicePathSegment(name, decode_service_path_index(index)))
        else:
            parsed_segments.append(ServicePathSegment(segment, None))
    return parsed_segments


def build_service_path(segments):
    """
    Build a Robot Raconteur service path from segments

    :param segments: The segments to build the service path from
    :type segments: List[ServicePathSegment]
    :return: The built service path
    :rtype: str
    """
    return '.'.join([f'{segment.name}[{encode_service_path_index(segment.index)}]' if segment.index is not None else segment.name for segment in segments])
