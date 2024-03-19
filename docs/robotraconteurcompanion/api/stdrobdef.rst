Standard Robot Raconteur Service Types
======================================

The companion library contains the standard Robot Raconteur service types, ofter referred to as the
"standard robdef" types. The can be loaded into the Robot Raconteur node using the utility
function ``RobotRaconteurCompanion.StdRobDef.RegisterStdRobDefServiceTypes()``. The
names of the service types and the text can be accessed using the ``STANDARD_ROBDEF_NAMES`` and
``STANDARD_ROBDEF_TEXT`` variables.

The standard types can be found on GitHub at https://github.com/robotraconteur/robotraconteur_standard_robdef

Registering the standard types for clients is not necessary as the standard types are automatically
pulled when the client connects to a service.

In most cases, the standard robdef types are registered to the default node.

.. code-block:: python

    import RobotRaconteur as RR
    RRN = RR.RobotRaconteurNode.s
    import RobotRaconteurCompanion as RRC
    RRC.RegisterStdRobDefServiceTypes(RRN)
    # The standard types are now registered to the default node

RobotRaconteurCompanion.StdRobDef
----------------------------------

.. autofunction:: RobotRaconteurCompanion.StdRobDef.RegisterStdRobDefServiceTypes
