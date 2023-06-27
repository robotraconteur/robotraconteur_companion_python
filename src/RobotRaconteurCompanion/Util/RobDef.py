import RobotRaconteur as RR
import importlib.resources

def register_service_type_from_resource(node, package, resource):
    """
    Register a service type from a package resource

    :param node: The node to register the service type with
    :type node: RobotRaconteur.RobotRaconteurNode
    :param package: The package containing the resource
    :type package: str
    :param resource: The resource name
    :type resource: str
    """
    robdef_text = get_service_type_from_resource(package,resource)
    node.RegisterServiceType(robdef_text)

def register_service_types_from_resources(node, package, resources):
    """
    Register a list of service types from a package resource

    :param node: The node to register the service types with
    :type node: RobotRaconteur.RobotRaconteurNode
    :param package: The package containing the resource
    :type package: str
    :param resources: The list of resource names
    :type resources: list[str]
    """
    robdefs_text = get_service_types_from_resources(package,resources)
    node.RegisterServiceTypes(robdefs_text)

def get_service_type_from_resource(package, resource):
    """
    Return the text of a service type from a package resource

    :param package: The package containing the resource
    :type package: str
    :param resource: The resource name
    :type resource: str
    :return: The service type text
    :rtype: str
    """
    ext = ""
    if importlib.resources.is_resource(package, resource + ".robdef"):
        ext = ".robdef"    
    robdef_text = importlib.resources.read_text(package,resource + ext)
    return robdef_text

def get_service_types_from_resources(package, resources):
    """
    Get a list of service type texts from a package resource

    :param package: The package containing the resource
    :type package: str
    :param resources: The list of resource names
    :type resources: list[str]
    :return: The list of service type texts
    :rtype: list[str]
    """
    robdefs_text = []
    for resource in resources:
        ext = ""
        if importlib.resources.is_resource(package, resource + ".robdef"):
            ext = ".robdef"
        robdef_text = importlib.resources.read_text(package,resource + ext)
        robdefs_text.append(robdef_text)
    return robdefs_text