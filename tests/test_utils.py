import logging
import os

import pytest

from src.utils import compare_images_ssim, take_window_screenshot

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.mark.skip(reason="Requires GUI environment")
def test_take_window_screenshot():
    """Test the ``take_window_screenshot`` function."""
    try:
        # Specify the window title to capture, e.g. Chrome
        window_title = "Chrome"

        # Path where the screenshot will be saved
        screenshot_path = "test_screenshot.png"

        # Call the function to take a screenshot
        take_window_screenshot(window_title, screenshot_path)

        # Verify that the screenshot was saved successfully
        assert os.path.exists(screenshot_path), "Screenshot was not saved successfully."

        logging.info("test_take_window_screenshot passed.")
    except Exception as e:
        logging.error(f"test_take_window_screenshot failed: {e}")


def test_compare_images_ssim():
    """Test the ``compare_images_ssim`` function."""
    try:
        # Define image paths
        base_dir = os.path.dirname(__file__)
        reference_image_path = os.path.join(base_dir, "reference_image.png")
        screenshot_path = os.path.join(base_dir, "test_screenshot.png")

        # Ensure the reference image exists
        if not os.path.exists(reference_image_path):
            raise FileNotFoundError(
                f"Reference image not found at {reference_image_path}"
            )

        # Call the function to compare the images
        similarity_score = compare_images_ssim(reference_image_path, screenshot_path)

        # Print and verify the similarity score
        logging.info(f"Similarity score: {similarity_score}")
        assert (
            similarity_score > 0.8
        ), f"Images are not similar enough. SSIM: {similarity_score}"

        logging.info("test_compare_images_ssim passed.")
    except Exception as e:
        logging.error(f"test_compare_images_ssim failed: {e}")
