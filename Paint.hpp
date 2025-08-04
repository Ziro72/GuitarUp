#pragma once
#include <iostream>
#include <string>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>

constexpr std::string background_image_path = "./src/backgrounds/";

void paste_image(cv::Mat& image, const cv::Mat& inserted_image,
                 const cv::Rect& rectangle);

inline void paste_image(cv::Mat& image, const cv::Mat& inserted_image,
                 const cv::Point& coordinate) {
  cv::Rect rectangle(coordinate, inserted_image.size());
  paste_image(image, inserted_image, rectangle);
}

inline void paste_image(cv::Mat& image, const cv::Mat& inserted_image,
                 const std::pair<int, int>& coordinate) {
  cv::Rect rectangle(coordinate.first, coordinate.second,
                     inserted_image.cols, inserted_image.rows);
  paste_image(image, inserted_image, rectangle);
}

inline void paste_image(cv::Mat& image, const cv::Mat& inserted_image,
                 const int& x, const int& y) {
  cv::Rect rectangle(x, y, inserted_image.cols, inserted_image.rows);
  paste_image(image, inserted_image, rectangle);
}

cv::Mat cut_out_a_rectangle(const cv::Mat& image,
                            const cv::Rect& rectangle);

class Paint {
 public:
 private:
  cv::Mat image_;
  std::string background_image_name = "default";
  std::string image_name_ = "default";
};