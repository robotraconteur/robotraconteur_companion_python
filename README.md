# Robot Raconteur Companion Python

<p align="center"><img src="docs/figures/logo-header.svg"></p>

The Robot Raconteur companion library contains utilities for working with Robot Raconteur services and devices.
This companion library is intended to be used with the Robot Raconteur Core library
(https://github.com/robotraconteur/robotraconteur). This version of the companion library is for Python.
Other language versions are available at https://github.com/robotraconteur.

Robot Raconteur Core focuses on the core capabilities of Robot Raconteur, such as transport, discovery, and
communication. The companion contains a number of miscelanous utilities that are useful for working with other libraries
such as Eigen, and for working with standard Robot Raconteur service types 
(https://github.com/robotraconteur/robotraconteur_standard_robdef).

The companion library is not required to use Robot Raconteur, but is recommended for most users.

The companion is intended to evolve faster than the core library, and accept contributions from the community.

The companion library is licensed under the Apache 2.0 license.

The Robot Raconteur Companion library contains the following utilities:

* Standard Service Definition (robdef) types
* YAML parsers for device info structures
* Service attribute utilities
* Geometry type converters
* Image type converters
* Date/time converters
* Identifier utilities
* UUID utilities
* Miscellaneous support utilities

## Installation

The Robot Raconteur companion library is available on PyPI. It can be installed using pip:

```
pip install RobotRaconteurCompanion
```

## Documentation

Documentation for the Robot Raconteur companion library is available at https://robot-raconteur-companion-python.readthedocs.io/en/latest/

## Standard Service Types 

The companion library contains the standard service types available at 
https://github.com/robotraconteur/robotraconteur_standard_robdef . These types can be registered
with the local Node using the following code:

```python
import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
RRC.RegisterStdRobDefServiceTypes(RRN)
```

Registering the standard service types is not required for clients since they will be pulled from the service.

## Device Info Structure YAML Parsers and Attributes Util

Device Info structures are used to describe devices and their capabilities. The structures are provided
to clients at runtime, typically through a property of a device service. For example, the 
`com.robotraconteur.device.Device` standard type defines the `device_info` property. The 
`com.robotraconteur.robotics.robot.Robot` standard type defines both `device_info` and `robot_info` properties.
These structures can be used to describe a wide variety of devices, including robots, sensors, and other devices.
YAML files are used to store the contents of these structures to make it easier to create and edit them. The
Robot Raconteur companion library contains parsers for these YAML files. The following device info structure types
are supported:

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

The attributes utility class can be used to generate the attributes for a registered service. These attributes
are used by clients to locate a desired service.

Device info files can be parsed using the `RobotRaconteurCompanion.Util.InfoFileLoader` class. The following example
parses a device info file and prints the device name:

```python
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
```

## Geometry Type Converters

The Robot Raconteur companion library contains type converters for geometry types defined in,
 `com.robotraconteur.geometry`, `com.robotraconteur.geometryf`, and `com.robotraconteur.geometryi`. These types
can be converted to and from the corresponding Python types.

An example of converting a few types:

```python
from RobotRaconteur.Client import *
from RobotRaconteur.Companion.Util import GeometryUtil

c = RRN.ConnectService('rr+tcp://localhost:22222?service=MyRobot')
geom_util = GeometryUtil(client_obj=c)

# Create GeometryUtil using the connected object

# Get a position vector
v = c.getf_position()

# Convert to numpy array
v2 = vector3_to_xyz(v)

# Convert a rpy xyz to a Robot Raconteur com.robotraconteur.geometry.Transform
t = rpy_xyz_to_transform(np.deg2rad([10,20,30],[0.1,0.2,0.3]))
```

## Image Type Converters

The image utilities provide functions to convert between Robot Raconteur image structures and OpenCV numpy arrays.

An example of converting a few types:

```python
 from RobotRaconteur.Client import *
from RobotRaconteurCompanion.Util.ImageUtil import ImageUtil

c = RRN.ConnectService('rr+tcp://localhost:2355?service=camera')
im = c.capture_frame()

im_util = ImageUtil(client_obj=c)
im_mat = im_util.image_to_numpy(im)

# Do something with the image

# Create a random image
im_mat = np.random.randint(0,255,(480,640,3),dtype=np.uint8)
rr_img = im_util.array_to_image(im_mat, "bgr888")

# Send the image
c.send_frame(rr_img)
```

## Date/Time Utilities

The date/time utilities provide functions for populating Robot Raconteur date/time structures.

An example of using the date/time utilities:

```python
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
```

## Identifier and UUID Utilities

The identifier utilities provide functions for creating and parsing Robot Raconteur identifiers and UUIDs.

An example of using the identifier utilities:

```python
import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
from RobotRaconeteurCompanion.Util.IdentifierUtil import IdentifierUtil

RRC.RegisterStdRobDefServiceTypes(RRN)

# Create an IdentifierUtil
id_util = IdentifierUtil(RRN)

# Create an identifier from a name
my_device_identifier = id_util.CreateIdentifierFromName("my_device")

# Convert the identifier to a string
my_device_identifier_str = id_util.IdentifierToString(my_device_identifier)

# Convert the identifier string back to an identifier
my_device_identifier2 = id_util.StringToIdentifier(my_device_identifier_str)

# Compare identifiers
assert id_util.IsIdentifierMatch(my_device_identifier, my_device_identifier2)
```

## Miscellaneous Utilities

Other utility classes are provided for various purposes. These include populating 
`com.robotraconteur.sensordata.SensorData` structures, periodically calling a function, and loading
Robot Raconteur service info files from packages. See the documentation for more information.

## License

Apache 2.0
