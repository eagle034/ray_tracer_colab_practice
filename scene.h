#ifndef SCENE_H_
#define SCENE_H_

#include "hittable_list.h"
#include "camera.h"

class Scene {
 public:
  // Default constructor is needed to create this object on stack in Cython.
  Scene() {}
  Scene(int image_width, int image_height,
        int samples_per_pixel,
        int max_depth, hittable_list world, Camera camera);

  bool RenderLine(int y, uint8_t* line) const;

 private:
  // Note we can't use const here, because we want to keep this object
  // assignable, which is used in Cython code.
  int image_width_ = -1;
  int image_height_ = -1;
  int samples_per_pixel_ = -1;
  int max_depth_ = -1;
  hittable_list world_;
  Camera camera_;
};

#endif  // SCENE_H_
