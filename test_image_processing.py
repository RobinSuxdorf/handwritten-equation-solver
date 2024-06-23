import pytest
import numpy as np
import cv2

from image_processing import (
    _crop_and_resize_images,
    _find_and_sort_contours,
    _load_and_preprocess_image,
    extract_objects
)

def create_test_image() -> str:
    image = np.ones((100, 100), np.uint8) * 255

    cv2.rectangle(image, (10, 10), (30, 50), (0, 0, 0), -1)
    cv2.rectangle(image, (40, 10), (70, 50), (0, 0, 0), -1)
    cv2.rectangle(image, (80, 10), (90, 50), (0, 0, 0), -1)

    test_image_path = "test_image_path.png"
    cv2.imwrite(test_image_path, image)
    return test_image_path

@pytest.fixture
def test_image_path() -> str:
    return create_test_image()

def test_load_and_preprocess_image(test_image_path) -> None:
    binary_image = _load_and_preprocess_image(test_image_path)

    assert binary_image is not None
    assert binary_image.shape == (100, 100)
    assert np.array_equal(np.unique(binary_image), [0, 255])

def test_find_and_sort_contours(test_image_path) -> None:
    binary_image = _load_and_preprocess_image(test_image_path)
    bounding_rects = _find_and_sort_contours(binary_image)

    assert len(bounding_rects) == 3
    assert bounding_rects[0][0] < bounding_rects[1][0] < bounding_rects[2][0]

def test_crop_and_resize_images(test_image_path) -> None:
    binary_image = _load_and_preprocess_image(test_image_path)
    bounding_rects = _find_and_sort_contours(binary_image)
    resized_images = _crop_and_resize_images(binary_image, bounding_rects)

    assert len(resized_images) == 3
    for img in resized_images:
        assert img.shape == (28, 28)

def test_split_and_resize_image(test_image_path) -> None:
    resized_images = extract_objects(test_image_path)

    assert len(resized_images) == 3
    for img in resized_images:
        assert img.shape == (28, 28)