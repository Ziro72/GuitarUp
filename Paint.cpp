#include "Paint.hpp"

void paste_image(cv::Mat& image, const cv::Mat& inserted_image,
                 const cv::Rect& rectangle) {
  if (image.empty() || inserted_image.empty()) {
    return;
  }
  if (rectangle.x < 0 || rectangle.y < 0 ||
      rectangle.x >= image.cols || rectangle.y >= image.rows) {
    return;
  }
  if (rectangle.x + rectangle.width < 0 || rectangle.y + rectangle.height < 0 ||
      rectangle.x + rectangle.width >= image.cols ||
      rectangle.y + rectangle.height >= image.rows) {
    return;
  }
  std::vector<cv::Mat> source(4);
  cv::split(inserted_image, source);
  inserted_image.copyTo(image(rectangle), source[3]);
}

cv::Mat cut_out_a_rectangle(const cv::Mat& image,
                            const cv::Rect& rectangle) {
  if (image.empty()) {
    return {};
  }
  if (rectangle.x < 0 || rectangle.y < 0 ||
      rectangle.x >= image.cols || rectangle.y >= image.rows) {
    return {};
  }
  return image(rectangle).clone();
}

int main() {
}
