from libc.stdint cimport uint8_t
from libcpp cimport bool

cdef extern from 'scene.h':
  cdef cppclass Scene:
    bool RenderLine(int y, uint8_t* line) nogil
