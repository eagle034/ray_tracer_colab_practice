from libcpp.memory cimport unique_ptr

from ray_tracer_colab.pxd.hittable cimport hittable

cdef extern from 'hittable_list.h':
  cdef cppclass hittable_list:
    hittable_list() nogil
    void clear() nogil
    void add(unique_ptr[hittable] obj) nogil
