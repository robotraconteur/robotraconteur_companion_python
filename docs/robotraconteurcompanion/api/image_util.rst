RobotRaconteurCompanion.Util.ImageUtil
===========================================

Utility class for working with Robot Raconteur images. The images are converted between the Robot Raconteur
image structure and the OpenCV image structure. OpenCV image structures in Python are typically numpy arrays.
Compressed and uncompressed Robot Raconteur images are supported.

A simple example:

.. code-block:: python

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


ImageUtil
--------------

.. autoclass:: RobotRaconteurCompanion.Util.ImageUtil.ImageUtil
    :members:
