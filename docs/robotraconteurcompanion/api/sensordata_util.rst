RobotRaconteurCompanion.Util.SensorDataUtil
===========================================

Utility class for filling in com.robotraconteur.sensordata.SensorDataHeader structures

.. code-block:: python

    import RobotRaconteur as RR
    RRN = RR.RobotRaconteurNode.s
    import RobotRaconteurCompanion as RRC
    from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
    from RobotRaconteurCompanion.Util.SensorDataUtil import SensorDataUtil

    RRC.RegisterStdRobDefServiceTypes(RRN)
    info_loader = InfoFileLoader(RRN)
    camera_info, camera_ident_fd = info_loader.LoadInfoFileFromString(camera_info_text, "com.robotraconteur.imaging.camerainfo.CameraInfo", "camera")

    sensordata_util = SensorDataUtil(RRN)

    while True:

        # Do some work on the driver

        # Create a new sensor data structure
        seqno += 1
        sensor_data_header = sensordata_util.FillSensorDataHeader(camera_info, seqno, time.time())

        # Sensor data structures typically have a data_header field of type SensorDataHeader
        my_sensor_data.data_header = sensor_data_header

SensorDataUtil
--------------

.. autoclass:: RobotRaconteurCompanion.Util.SensorDataUtil.SensorDataUtil
    :members:
