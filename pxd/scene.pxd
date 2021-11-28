from libc.stdint cimport uint8_t
from libcpp cimport bool

from ray_tracer_colab.pxd.camera cimport Camera
from ray_tracer_colab.pxd.hittable_list cimport hittable_list

cdef extern from 'scene.h':
  cdef cppclass Scene:
    Scene() nogil
    Scene(int image_width, int image_height, int samples_per_pixel,
          int max_depth, hittable_list world, Camera camera) nogil
    bool RenderLine(int y, uint8_t* line) nogil
