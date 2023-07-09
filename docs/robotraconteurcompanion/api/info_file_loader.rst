RobotRaconteurCompanion.Util.InfoFileLoader
===========================================

Utility class for loading Robot Raconteur device info structure from YAML files. These info structures
contain metadata and are passed to clients to describe the device.

The following types are supported:

* `com.robotraconteur.actuator.ActuatorInfo`
* `com.robotraconteur.clock.ClockDeviceInfo`
* `com.robotraconteur.isoch.IsochDeviceInfo`
* `com.robotraconteur.device.DeviceInfo`
* `com.robotraconteur.eventlog.EventLogInfo`
* `com.robotraconteur.fiducial.FiducialInfo`
* `com.robotraconteur.fiducial.FiducialSensorInfo`
* `com.robotraconteur.hid.joystick.JoystickInfo`
* `com.robotraconteur.image.ImageInfo`
* `com.robotraconteur.image.FreeformImageInfo`
* `com.robotraconteur.imaging.camerainfo.PlumbBobDistortionInfo`
* `com.robotraconteur.imaging.camerainfo.CameraInfo`
* `com.robotraconteur.imaging.camerainfo.MultiCameraInfo`
* `com.robotraconteur.laserscan.LaserScanInfo`
* `com.robotraconteur.laserscan.LaserScanInfof`
* `com.robotraconteur.laserscan.LaserScanSensorInfo`
* `com.robotraconteur.lighting.LightInfo`
* `com.robotraconteur.objectrecognition.ObjectRecognitionSensorInfo`
* `com.robotraconteur.octree.OcTreeInfo`
* `com.robotraconteur.param.ParameterInfo`
* `com.robotraconteur.pointcloud.sensor.PointCloudSensorInfo`
* `com.robotraconteur.resource.BucketInfo`
* `com.robotraconteur.resource.ResourceInfo`
* `com.robotraconteur.robotics.joint.JointInfo`
* `com.robotraconteur.robotics.payload.PayloadInfo`
* `com.robotraconteur.robotics.robot.RobotInfo`
* `com.robotraconteur.robotics.robot.RobotKinChainInfo`
* `com.robotraconteur.robotics.tool.ToolInfo`
* `com.robotraconteur.sensor.SensorInfo`
* `com.robotraconteur.sensordata.SensorDataSourceInfo`
* `com.robotraconteur.servo.ServoInfo`
* `com.robotraconteur.signal.SignalInfo`
* `com.robotraconteur.signal.SignalGroupInfo`

.. code-block:: python

    import RobotRaconteur as RR
    RRN = RR.RobotRaconteurNode.s
    import RobotRaconteurCompanion as RRC
    from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
    from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil

    RRC.RegisterStdRobDefServiceTypes(RRN)
    info_loader = InfoFileLoader(RRN)
    camera_info, camera_ident_fd = info_loader.LoadInfoFileFromString(camera_info_text, "com.robotraconteur.imaging.camerainfo.CameraInfo", "camera")
    attributes_util = AttributesUtil(RRN)
    camera_attributes = attributes_util.GetDefaultServiceAttributesFromDeviceInfo(camera_info.device_info)

    # Register a service and set attributes
    service_ctx = RRN.RegisterService("camera","com.robotraconteur.imaging.Camera",camera)
    service_ctx.SetServiceAttributes(camera_attributes)


InfoFileLoader
------------

.. autoclass:: RobotRaconteurCompanion.Util.InfoFileLoader.InfoFileLoader
    :members:
    
