import os
import pytest

from src.screenshot_search import capture_and_search


@pytest.mark.skip(reason="Requires CLIP model and Windows screenshot")
def test_capture_and_search(monkeypatch):
    def fake_screenshot(title, run_dir, function_type):
        return os.path.join(os.path.dirname(__file__), "test_screenshot.png")

    def fake_search(image_path, top_k=3):
        return [("baseline1.png", 0.9), ("baseline2.png", 0.85)]

    monkeypatch.setattr("src.screenshot_search.take_window_screenshot", fake_screenshot)
    monkeypatch.setattr("src.screenshot_search.search", fake_search)

    result = capture_and_search("Chrome", "freeze")
    assert result["best_match"] == "baseline1.png"
    assert result["faiss_results"][0][0] == "baseline1.png"
