RobotRaconteurCompanion.Util.DeviceConnector
============================================

The DeviceConnector class is designed to simplify connecting to devices using Robot Raconteur. Finding and
connecting to multiple services can be complex, especially when using advanced features such as service
discovery filters. The DeviceConnector takes advantage of the "device" concept introduced by the Robot Raconteur
standard types. The "device" concept introduces the ``com.robotraconteur.device.Device`` interface, which provides
the structure ``com.robotraconteur.device.DeviceInfo`` containing metadata about the device. The "device" concept
provides a more descriptive way to identify, connect, and interrogate devices.

The DeviceConnector can use device metadata, URLs, or service discovery filters to connect to devices. The
DeviceConnectorDetails structure is used to specify the connection details. The DeviceConnector uses
the Robot Raconteur ServiceSubscriptionManager class to manage subscriptions to services based on the
information provided in the DeviceConnectorDetails structure. Each device uses a unique ``nickname`` to
identify the device locally.

The list of DeviceConnectorDetails can also be specified using YAML files to simplify the configuration of
the DeviceConnector when connecting to multiple devices. The file can easily be specified on the command
line using the Python ``argparse`` module.

The DeviceConnector is used by applications like the PyRI Open Source Teaching Pendant to simplify the
connection to multiple devices. It is recommended to use the PyRI Device Manager capability to manage
complex systems with multiple devices when practical to do so.

DeviceConnector
---------------

.. autoclass:: RobotRaconteurCompanion.Util.DeviceConnector.DeviceConnector
    :members:

.. autofunction:: RobotRaconteurCompanion.Util.DeviceConnector.load_device_details_from_yaml_path

.. autofunction:: RobotRaconteurCompanion.Util.DeviceConnector.load_device_details_from_yaml

.. autofunction:: RobotRaconteurCompanion.Util.DeviceConnector.load_device_details_from_yaml_dict
