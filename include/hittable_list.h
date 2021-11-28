#ifndef HITTABLE_LIST_H
#define HITTABLE_LIST_H

// Originally written in 2016 by Peter Shirley <ptrshrl@gmail.com>

#include <memory>
#include <utility>
#include <vector>

#include "hittable.h"
#include "rtweekend.h"

class hittable_list : public hittable {
 public:
  hittable_list() {}

  void clear() { objects.clear(); }
  void add(std::unique_ptr<hittable> object) {
    objects.emplace_back(std::move(object));
  }

  virtual bool hit(const ray& r, double t_min, double t_max,
                   hit_record& rec) const override;

 public:
  std::vector<std::unique_ptr<hittable>> objects;
};

inline bool hittable_list::hit(const ray& r, double t_min, double t_max,
                               hit_record& rec) const {
  hit_record temp_rec;
  auto hit_anything = false;
  auto closest_so_far = t_max;

  for (const auto& object : objects) {
    if (object->hit(r, t_min, closest_so_far, temp_rec)) {
      hit_anything = true;
      closest_so_far = temp_rec.t;
      rec = temp_rec;
    }
  }

  return hit_anything;
}

#endif
