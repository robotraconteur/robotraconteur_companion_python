RobotRaconteurCompanion.Util.AttributesUtil
===========================================

Utility classes to help with Robot Raconteur service attributes. Example usage:

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



AttributesUtil
--------------

.. autoclass:: RobotRaconteurCompanion.Util.AttributesUtil.AttributesUtil
    :members:
    