#include "scene.h"

#include <algorithm>
#include <utility>

#include "color.h"
#include "material.h"
#include "rtweekend.h"
#include "sphere.h"

namespace {

color ray_color(const ray& r, const hittable& world, int depth) {
  hit_record rec;

  // If we've exceeded the ray bounce limit, no more light is gathered.
  if (depth <= 0) {
    return color(0, 0, 0);
  }

  if (world.hit(r, 0.001, infinity, rec)) {
    ray scattered;
    color attenuation;
    if (rec.mat_ptr->scatter(r, rec, attenuation, scattered))
      return attenuation * ray_color(scattered, world, depth - 1);
    return color(0, 0, 0);
  }

  vec3 unit_direction = unit_vector(r.direction());
  auto t = 0.5 * (unit_direction.y() + 1.0);
  return (1.0 - t) * color(1.0, 1.0, 1.0) + t * color(0.5, 0.7, 1.0);
}

}  // namespace

Scene::Scene(int image_width, int image_height, int samples_per_pixel,
             int max_depth, hittable_list world, Camera camera)
    : image_width_(image_width),
      image_height_(image_height),
      samples_per_pixel_(samples_per_pixel),
      max_depth_(max_depth),
      world_(std::move(world)),
      camera_(std::move(camera)) {}

// TODO: move
uint8_t Uint8FromFloat(float v) {
  return static_cast<uint8_t>(std::clamp(static_cast<int>(v * 255), 0, 255));
}

bool Scene::RenderLine(int y, uint8_t* line) const {
  for (int x = 0; x < image_width_; ++x) {
    color pixel_color(0, 0, 0);
    for (int s = 0; s < samples_per_pixel_; ++s) {
      auto u = (x + random_double()) / (image_width_ - 1);
      auto v = (y + random_double()) / (image_height_ - 1);
      ray r = camera_.get_ray(u, v);
      pixel_color += ray_color(r, world_, max_depth_);
    }
    pixel_color = process_color(pixel_color, samples_per_pixel_);
    *line++ = Uint8FromFloat(pixel_color.x());
    *line++ = Uint8FromFloat(pixel_color.y());
    *line++ = Uint8FromFloat(pixel_color.z());
  }
  return true;
}
