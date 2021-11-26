#ifndef COLOR_H
#define COLOR_H

// Originally written in 2020 by Peter Shirley <ptrshrl@gmail.com>

#include <iostream>

#include "vec3.h"

inline color process_color(const color& pixel_color, int samples_per_pixel) {
  auto r = pixel_color.x();
  auto g = pixel_color.y();
  auto b = pixel_color.z();

  // Replace NaN components with zero. See explanation in Ray Tracing: The Rest
  // of Your Life.
  if (r != r) r = 0.0;
  if (g != g) g = 0.0;
  if (b != b) b = 0.0;

  // Divide the color by the number of samples and gamma-correct for gamma=2.0.
  auto scale = 1.0 / samples_per_pixel;
  r = sqrt(scale * r);
  g = sqrt(scale * g);
  b = sqrt(scale * b);

  return color(r, g, b);
}

inline void write_color(std::ostream& out, const color& pixel_color) {
  // Write the translated [0,255] value of each color component.
  out << static_cast<int>(256 * clamp(pixel_color.x(), 0.0, 0.999)) << ' '
      << static_cast<int>(256 * clamp(pixel_color.y(), 0.0, 0.999)) << ' '
      << static_cast<int>(256 * clamp(pixel_color.z(), 0.0, 0.999)) << '\n';
}

#endif
