RobotRaconteurCompanion.Util.DateTimeUtil
=========================================

Utility class for working with Robot Raconteur standard times structures.

.. code-block:: python

    import RobotRaconteur as RR
    RRN = RR.RobotRaconteurNode.s
    import RobotRaconteurCompanion as RRC
    from RobotRaconeteurCompanion.Util.DateTimeUtil import DateTimeUtil

    RRC.RegisterStdRobDefServiceTypes(RRN)

    # Create a DateTimeUtil object
    dt_util = DateTimeUtil(RRN)

    # Create a Robot Raconteur TimeSpec2
    now_timespec2 = dt_util.NowTimeSpec()

    # Create a Robot Raconteur TimeSpec3
    now_timespec3 = dt_util.NowTimeSpec3()

    # Create a Robot Raconteur DateTimeUTC
    now_datetimeutc = dt_util.NowDateTimeUTC()


DateTimeUtil
------------

.. autoclass:: RobotRaconteurCompanion.Util.DateTimeUtil.DateTimeUtil
    :members:
