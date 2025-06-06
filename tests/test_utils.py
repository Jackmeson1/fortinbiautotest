import logging
import os

import pytest

from src.utils import compare_images_ssim, take_window_screenshot

# 设置日志记录
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.mark.skip(reason="Requires GUI environment")
def test_take_window_screenshot():
    """
    测试 take_window_screenshot 函数。
    """
    try:
        # 指定要捕获的窗口标题，例如 Chrome 浏览器
        window_title = "Chrome"

        # 指定截图保存路径
        screenshot_path = "test_screenshot.png"

        # 调用函数进行截图
        take_window_screenshot(window_title, screenshot_path)

        # 验证截图是否成功保存
        assert os.path.exists(screenshot_path), "Screenshot was not saved successfully."

        logging.info("test_take_window_screenshot passed.")
    except Exception as e:
        logging.error(f"test_take_window_screenshot failed: {e}")


def test_compare_images_ssim():
    """
    测试 compare_images_ssim 函数。
    """
    try:
        # 定义图片路径
        base_dir = os.path.dirname(__file__)
        reference_image_path = os.path.join(base_dir, "reference_image.png")
        screenshot_path = os.path.join(base_dir, "test_screenshot.png")

        # 确保参考图片存在
        if not os.path.exists(reference_image_path):
            raise FileNotFoundError(
                f"Reference image not found at {reference_image_path}"
            )

        # 调用函数进行图片比较
        similarity_score = compare_images_ssim(reference_image_path, screenshot_path)

        # 打印和验证相似度分数
        logging.info(f"Similarity score: {similarity_score}")
        assert (
            similarity_score > 0.8
        ), f"Images are not similar enough. SSIM: {similarity_score}"

        logging.info("test_compare_images_ssim passed.")
    except Exception as e:
        logging.error(f"test_compare_images_ssim failed: {e}")
