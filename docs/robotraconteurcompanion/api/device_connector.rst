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

An example of using the DeviceConnector to connect to a device using the device name is shown below:

.. code-block:: python

    from RobotRaconteur.Client import *
    from RobotRaconteurCompanion.Util.DeviceConnector import DeviceConnector, DeviceConnectorDetails

    # Create a DeviceConnector
    connector = DeviceConnector()

    # Create a DeviceConnectorDetails using the device name "abb_robot"
    # For this example, we do not use other metadata like tags, serial number, UUIDs, etc
    device_details = DeviceConnectorDetails(device_nickname="robot", device="abb_robot")

    # Add to the device
    device = connector.AddDevice(device_details)

    # Get the device subscription
    device_sub = connector.GetDevice("robot")

    # Get the device client
    device_client = device_sub.GetDefaultClientWait(5)

    # Read and print the device info
    device_info = device_client.device_info
    print(device_info)

    # The device client can be used to connect to other services on the device. The subscription
    # can be used to subscribe the wires and pipes on the device.

    # Close the connector
    connector.Close()

An example of using the DeviceConnector to connect to a device using a URL is shown below:

.. code-block:: python

    from RobotRaconteur.Client import *
    from RobotRaconteurCompanion.Util.DeviceConnector import DeviceConnector, DeviceConnectorDetails

    # Create a DeviceConnector
    connector = DeviceConnector()

    # Create a DeviceConnectorDetails using the URL "rr+tcp://localhost:58653?service=device"
    # For this example, we do not use other metadata like tags, serial number, UUIDs, etc
    device_url = "rr+tcp://localhost:52512/?service=robot"
    device_details = DeviceConnectorDetails(device_nickname="robot", urls=[device_url])

    # Add to the device
    device = connector.AddDevice(device_details)

    # Get the device subscription
    device_sub = connector.GetDevice("robot")

    # Get the device client
    device_client = device_sub.GetDefaultClientWait(5)

    # Read and print the device info
    device_info = device_client.device_info
    print(device_info)

    # The device client can be used to connect to other services on the device. The subscription
    # can be used to subscribe the wires and pipes on the device.

    # Close the connector
    connector.Close()

An example using a YAML file to specify the connection details is shown below:

YAML file:

.. code-block:: yaml

    devices:
      robot:
        device: abb_robot
      robot2:
        urls:
          - rr+tcp://localhost:52512/?service=robot

Python code using ``argparse`` to specify the YAML file:

.. code-block:: python

    from RobotRaconteur.Client import *
    from RobotRaconteurCompanion.Util.DeviceConnector import DeviceConnector, DeviceConnectorDetails
    import argparse

    # Use argparse to specify the YAML file
    parser = argparse.ArgumentParser(description="Device Connector Example")
    parser.add_argument("--client-config-file", type=argparse.FileType('r'), required=True, help="Client connection configuration file")

    args, _ = parser.parse_known_args()

    # Create a DeviceConnector and load the device details from the YAML file
    connector = DeviceConnector(devices_yaml_f=args.client_config_file)

    # Get robot default client
    robot = connector.GetDevice("robot").GetDefaultClientWait(5)
    robot2 = connector.GetDevice("robot2").GetDefaultClientWait(5)

    print(robot.device_info)
    print(robot2.device_info)

    # The devices are now connected and can be used

    # Close the connector
    connector.Close()

DeviceConnector
---------------

.. autoclass:: RobotRaconteurCompanion.Util.DeviceConnector.DeviceConnector
    :members:

DeviceConnectorDetails
----------------------

.. autoclass:: RobotRaconteurCompanion.Util.DeviceConnector.DeviceConnectorDetails
    :members:

YAML Functions
--------------

.. autofunction:: RobotRaconteurCompanion.Util.DeviceConnector.load_device_details_from_yaml_path

.. autofunction:: RobotRaconteurCompanion.Util.DeviceConnector.load_device_details_from_yaml

.. autofunction:: RobotRaconteurCompanion.Util.DeviceConnector.load_device_details_from_yaml_dict
