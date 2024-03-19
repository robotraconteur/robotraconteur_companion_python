RobotRaconteurCompanion.Util.ServicePathUtil
===========================================

Utility class for working with Robot Raconteur service paths.

Robot Raconteur service paths are used to identify services and objects in Robot Raconteur services. They are
represented as a string with segments separated by periods. Each segment consists of a name and an optional index.
The name is made up of alphanumeric characters and underscores, starting with a letter. The index is a string
consisting of alphanumeric characters, with any non alphanumeric characters encoded using the percent encoding
scheme used by URLs. Any UTF-8 characters are encoded using the percent encoding scheme used by URLs.

See the Robot Raconteur documentation for more information on service paths.

This module provides functions to build and parse service paths. Some Robot Raconteur functions require the use of
service paths, and these utilities can be used to build and parse them.

.. code-block:: python

    .. code-block:: python

        from RobotRaconteurCompanion.Util.ServicePathUtil import parse_service_path, build_service_path, \
            ServicePathSegment

        # An example service path
        path = "example.example_service.example_object[myindex]"

        # Parse the service path
        parsed_path = parse_service_path(path)

        # Print the parsed path
        print(parsed_path)

        # Define a service path using the ServicePathSegment class
        path_segments = [
            ServicePathSegment('example', None),
            ServicePathSegment('example_service', None),
            ServicePathSegment('example_object', 'myindex')
        ]

        # Build the service path
        built_path = build_service_path(path_segments)

        # Print the built path
        print(built_path)



ServicePathUtil
---------------

.. autofunction:: RobotRaconteurCompanion.Util.ServicePathUtil.parse_service_path


.. autofunction:: RobotRaconteurCompanion.Util.ServicePathUtil.build_service_path


.. autoclass:: RobotRaconteurCompanion.Util.ServicePathUtil.ServicePathSegment
    :members:


.. autofunction:: RobotRaconteurCompanion.Util.ServicePathUtil.encode_service_path_index


.. autofunction:: RobotRaconteurCompanion.Util.ServicePathUtil.decode_service_path_index
