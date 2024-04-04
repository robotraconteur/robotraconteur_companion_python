import threading
import RobotRaconteur as RR
import collections.abc
import uuid as py_uuid
from contextlib import suppress
import yaml


class DeviceConnectorDetails:
    def __init__(self, device_nickname, device=None, serial_number=None, tags=None, tag_match_operation="and",
                 service_nodes=None,
                 transport_schemes=None, urls=None, url_auth=None, root_object_type=None, subscription_filter=None,
                 max_connections=10):
        if not any([device, serial_number, urls, root_object_type]):
            raise RR.InvalidArgumentException(
                "At least one of device, serial_number, urls, or root_object_type must be specified")

        if (any([device, serial_number, tags]) and any([urls, url_auth, subscription_filter])):
            raise RR.InvalidArgumentException(
                "If device, serial_number, or tags are specified, urls and subscription_filter must not be specified")

        if (urls and any([subscription_filter, service_nodes, transport_schemes])):
            raise RR.InvalidArgumentException(
                "If urls are specified, service_nodes, transport_schemes, and subscription_filter must not be specified")
        if (subscription_filter and any([device, serial_number, tags, service_nodes, transport_schemes])):
            raise RR.InvalidArgumentException(
                "If subscription_filter is specified, device, serial_number, tags, service_nodes, and transport_schemes must not be specified")

        self.device_nickname = device_nickname
        self.device = device
        self.serial_number = serial_number
        self.tags = tags
        self.service_nodes = service_nodes
        self.urls = urls
        self.root_object_type = root_object_type
        self.subscription_filter = subscription_filter
        self.transport_schemes = transport_schemes
        self.url_auth = url_auth
        self.max_connections = max_connections
        self.tag_match_operation = tag_match_operation


class DeviceConnector:
    def __init__(self, device_list=None, devices_yaml_f=None, autoconnect=True, node=None):
        self._lock = threading.Lock()
        if node is None:
            self._node = RR.RobotRaconteurNode.s
        else:
            self._node = node

        self.subscription_manager = RR.ServiceSubscriptionManager(node=self._node)

        self._autoconnect = autoconnect

        if devices_yaml_f is not None:
            if device_list is not None:
                raise RR.InvalidArgumentException("Cannot specify both device_list and devices_yaml_f")
            device_list = load_device_details_from_yaml(devices_yaml_f)

        if device_list is not None:
            try:
                for device in device_list:
                    self._do_update_device(device)
            except:
                with suppress(Exception):
                    self.subscription_manager.Close()
                raise

    def _do_update_device(self, device_details):
        sub_details = _device_details_to_subscription_details(
            self._node, device_details.device_nickname, device_details)
        sub_details.Enabled = self._autoconnect
        self.subscription_manager.AddSubscription(sub_details)

    def AddDevice(self, device_details):

        self._do_update_device(device_details)

    def RemoveDevice(self, device_nickname, close=True):

        self.subscription_manager.RemoveSubscription(device_nickname, close)

    def ConnectDevice(self, device_nickname):

        self.subscription_manager.EnableSubscription(device_nickname)

    def DisconnectDevice(self, device_nickname, close=True):

        self.subscription_manager.DisableSubscription(device_nickname, close)

    def GetDevice(self, device_nickname, force_create=False):
        return self.subscription_manager.GetSubscription(device_nickname, force_create)

    def TryGetDevice(self, device_nickname):
        try:
            return True, self.get_device(device_nickname)
        except:
            return False, None

    def Close(self):
        self.subscription_manager.Close()


def _device_details_to_subscription_details(node, nickname, device_details):
    if device_details.urls is not None:
        url_param = device_details.urls
        if not isinstance(device_details.urls, collections.abc.Sequence) and not isinstance(device_details.urls, str):
            url_param = [device_details.urls]
        username = None
        credentials = None
        if device_details.url_auth is not None:
            username = device_details.url_auth.username
            credentials = device_details.url_auth.credentials

        return RR.ServiceSubscriptionManagerDetails(Name=nickname,
                                                    ConnectionMethod=RR.ServiceSubscriptionManager_CONNECTION_METHOD_URL,
                                                    Urls=url_param, UrlUsername=username, UrlCredentials=credentials)
    elif device_details.subscription_filter is not None:
        return RR.ServiceSubscriptionManagerDetails(Name=nickname,
                                                    ConnectionMethod=RR.ServiceSubscriptionManager_CONNECTION_METHOD_TYPE,
                                                    Filter=device_details.subscription_filter,
                                                    ServiceTypes=device_details.root_object_type)
    else:
        service_types, details_filter = _device_details_to_subscription_filter(node, device_details)
        return RR.ServiceSubscriptionManagerDetails(Name=nickname,
                                                    ConnectionMethod=RR.ServiceSubscriptionManager_CONNECTION_METHOD_TYPE,
                                                    Filter=details_filter,
                                                    ServiceTypes=service_types)


def _device_details_identifier_to_filter_attribute(details_ident):
    if details_ident is None:
        return None
    details_ident_name = None
    details_ident_uuid = None
    if isinstance(details_ident, str):
        if "|" in details_ident:
            details_ident_name, details_ident_uuid = details_ident.split("|", 1)
            return RR.CreateServiceSubscriptionFilterAttributeIdentifier(details_ident_name, details_ident_uuid)
        else:
            try:
                return RR.CreateServiceSubscriptionFilterAttributeIdentifier("", details_ident)
            except:
                return RR.CreateServiceSubscriptionFilterAttributeIdentifier(details_ident, "")

    else:
        details_ident_name = getattr(details_ident, "name", None)
        details_ident_uuid = getattr(details_ident, "uuid", None)
        if (details_ident_name is None and details_ident_uuid is None and isinstance(details_ident, dict)):
            details_ident_name = details_ident.get("name", None)
            details_ident_uuid = details_ident.get("uuid", None)
        if not (details_ident_name is not None or details_ident_uuid is not None):
            raise RR.InvalidArgumentException("Invalid identifier")

        if not isinstance(details_ident_uuid, str):
            uuid_bytes = details_ident_uuid["uuid_bytes"].tobytes()
            details_ident_uuid = str(py_uuid.UUID(bytes=uuid_bytes))

        return RR.CreateServiceSubscriptionFilterAttributeIdentifier(details_ident_name or "", details_ident_uuid or "")


def _device_details_to_subscription_filter(node, device_details):
    if device_details.device_nickname is None or device_details.device_nickname == "":
        raise RR.InvalidArgumentException("Device details to filter must contain device_nickname")
    try:
        if device_details.urls is not None:
            raise RR.InvalidArgumentException("Device details to filter must not contain urls")
        if device_details.subscription_filter is not None:
            raise RR.InvalidArgumentException("Device details to filter must contain subscription filter")

        sub_filter = RR.ServiceSubscriptionFilter()

        root_object_type = ["com.robotraconteur.device.Device"]

        if device_details.root_object_type is not None:
            if isinstance(device_details.root_object_type, str):
                root_object_type = [device_details.root_object_type]
            else:
                root_object_type = device_details.root_object_type

        sub_filter.MaxConnections = device_details.max_connections

        attr_filter = {}

        if device_details.device is not None:
            dev_attr_group = RR.ServiceSubscriptionFilterAttributeGroup()
            dev_attr_group.Attributes.append(_device_details_identifier_to_filter_attribute(device_details.device))
            attr_filter["device"] = dev_attr_group

        if device_details.serial_number is not None:
            attr_filter["serial_number"] = RR.ServiceSubscriptionFilterAttribute(device_details.serial_number)

        if device_details.tags is not None and len(device_details.tags) > 0:
            tags = device_details.tags
            if not isinstance(tags, collections.abc.Sequence) and not isinstance(tags, str):
                tags = [tags]

            tag_grp = RR.ServiceSubscriptionFilterAttributeGroup()
            if device_details.tag_match_operation is None:
                tag_grp.Operation = RR.ServiceSubscriptionFilterAttributeGroupOperation_AND
            elif device_details.tag_match_operation.lower() == "and":
                tag_grp.Operation = RR.ServiceSubscriptionFilterAttributeGroupOperation_AND
            elif device_details.tag_match_operation.lower() == "or":
                tag_grp.Operation = RR.ServiceSubscriptionFilterAttributeGroupOperation_OR
            elif device_details.tag_match_operation.lower() == "nand":
                tag_grp.Operation = RR.ServiceSubscriptionFilterAttributeGroupOperation_NAND
            elif device_details.tag_match_operation.lower() == "nor":
                tag_grp.Operation = RR.ServiceSubscriptionFilterAttributeGroupOperation_NOR
            else:
                raise RR.InvalidArgumentException("Invalid tag match operation")

            for tag in tags:
                tag_grp.Attributes.append(_device_details_identifier_to_filter_attribute(tag))
            attr_filter["tags"] = tag_grp

        sub_filter.Attributes = attr_filter
        sub_filter.AttributesMatchOperation = RR.ServiceSubscriptionFilterAttributeGroupOperation_AND

        if device_details.transport_schemes is not None:
            sub_filter.TransportSchemes = device_details.transport_schemes

        if device_details.service_nodes is not None:
            sub_filter.Nodes = device_details.service_nodes

        return root_object_type, sub_filter
    except Exception as e:
        raise RR.InvalidArgumentException(
            f"Invalid device details for device {device_details.device_nickname}: {str(e)}")


def load_device_details_from_yaml_path(yaml_filename):
    with open(yaml_filename, "r") as f:
        return load_device_details_from_yaml(f)


def load_device_details_from_yaml(yaml_file):
    yaml_dict = yaml.safe_load(yaml_file)
    return load_device_details_from_yaml_dict(yaml_dict)


def load_device_details_from_yaml_dict(yaml_dict):
    details_out = []
    details_in = yaml_dict["devices"]
    for k, v in details_in.items():
        details_out1 = DeviceConnectorDetails(k)
        urls = v.get("urls", None)
        if urls is not None:
            details_out1.urls = urls
        if v.get("device") is not None:
            details_out1.device = v["device"]
        if v.get("serial_number") is not None:
            details_out1.serial_number = v["serial_number"]
        if v.get("tags") is not None:
            details_out1.tags = v["tags"]

        details_out.append(details_out1)
    return details_out
