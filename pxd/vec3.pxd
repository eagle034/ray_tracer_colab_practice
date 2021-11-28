cdef extern from 'vec3.h':
  cdef cppclass vec3:
    vec3() nogil
    vec3(double e0, double e1, double e2) nogil
    double x() nogil
    double y() nogil
    double z() nogil
    double length() nogil
    double length_squared() nogil
    # TODO: It seems Cython does not support overloading a static class method?
    # @staticmethod
    # vec3 random() nogil
    @staticmethod
    vec3 random(double min, double max) nogil
