from ray_tracer_colab.pxd.vec3 cimport vec3

cdef extern from 'camera.h':
  cdef cppclass Camera:
    Camera(vec3 lookfrom, vec3 lookat, vec3 vup, double vfov,
           double aspect_ratio, double aperture, double focus_dist,
           double _time0, double _time1) nogil
