import numpy as np
import cv2

def _load_and_preprocess_image(image_path: str) -> np.ndarray:
    """
    Loads the image in grayscale and apply binary thresholding.

    Args:
        image_path (str): Path to the image file.

    Returns:
        np.ndarray: Binary imager after thresholding.
    """
    grayscale_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if grayscale_image is None:
        raise ValueError(f"Image not found at path: {image_path}")

    _, binary_image = cv2.threshold(grayscale_image, 128, 255, cv2.THRESH_BINARY_INV)

    return binary_image

def _find_and_sort_contours(binary_image: np.ndarray) -> list[tuple[int, int, int, int]]:
    """
    Finds the contours and sorts them by their x-coordinate.

    Args:
        binary_image (np.ndarray): Binary image to find contours in.

    Returns:
        list[tuple[int, int, int, int]]: List of sorted bounding rects.
    """
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    bounding_rects = [cv2.boundingRect(contour) for contour in contours]
    bounding_rects = sorted(bounding_rects, key=lambda rect: rect[0])

    return bounding_rects

def _crop_and_resize_images(binary_image: np.ndarray, bounding_rects: list[tuple[int, int, int, int]]) -> list[np.ndarray]:
    """
    Crops and resizes the images based on bounding rects.

    Args:
        binary_image (np.ndarray): Binary image to crop from.
        bounding_rects: (list[tuple[int, int, int, int]]): List of bounding rects to crop.

    Returns:
        list[np.ndarray]: List of resized images.
    """
    resized_images: list[np.ndarray] = []

    for rect in bounding_rects:
        x, y, w, h = rect
        im_crop = binary_image[y - 10:y + h + 10, x - 10:x + w + 10]

        im_resize = cv2.resize(im_crop, (28, 28))

        resized_images.append(im_resize)

    return resized_images

def extract_objects(image_path: str) -> list[np.ndarray]:
    """
    Extracts objects from an input image.

    Args:
        image_path (str): Path to the input image file.

    Returns:
        list[np.ndarray]: List of resized images containing the detected objects.
    """
    binary_image = _load_and_preprocess_image(image_path)
    bounding_rects = _find_and_sort_contours(binary_image)
    resized_images = _crop_and_resize_images(binary_image, bounding_rects)
    return resized_images
    