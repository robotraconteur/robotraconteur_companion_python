RobotRaconteurCompanion.Util.RobDef
=======================================

Utility function to register custom robdef service definition files from a Python package.
Custom robdef files can be included as package resources. See the `abb_robotraconteur_driver_hmp <https://github.com/robotraconteur-contrib/abb_robotraconteur_driver_hmp>`_
driver for an example of using this utility.

Note that the setup.py file or pyproject.toml will have to explicitly include the robdef files as package resources.
For setup.py, with setuptools, this can be done with the following:

.. code-block:: python

    from setuptools import setup, find_packages
    setup(
        ...
        package_data={'': ['*.robdef']},
        include_package_data=True,
        ...
    )

An example of using this utility is as follows:

.. code-block:: python

    import RobotRaconteur as RR
    RRN = RR.RobotRaconteurNode.s
    from RobotRaconteurCompanion.Util.RobDef import register_service_type_from_resource

    # Assume there is a package resource named "custom_robdef.robdef" in the package

    register_service_type_from_resource(RRN, __package__, "custom_robdef.robdef")

RobDef
----------

.. automodule:: RobotRaconteurCompanion.Util.RobDef
    :members:
