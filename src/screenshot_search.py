import os
from typing import Optional, List, Tuple

from .utils import take_window_screenshot, create_run_directory
from .visual_index import search
from .ai_screenshot_analysis import compare_with_ai


def capture_and_search(
    window_title: str,
    function_type: str,
    api_key: Optional[str] = None,
    run_dir: Optional[str] = None,
    top_k: int = 3,
    similarity_threshold: float = 0.05,
) -> dict:
    """Capture a window screenshot and identify the closest baseline image.

    Parameters
    ----------
    window_title: str
        Title of the window to capture.
    function_type: str
        Name used for the screenshot file prefix (e.g. ``block``).
    api_key: Optional[str]
        OpenAI key for optional RAG disambiguation.
    run_dir: Optional[str]
        Directory in which to save the screenshot. If ``None`` a new
        run directory is created.
    top_k: int
        Number of candidates to retrieve from the FAISS index.
    similarity_threshold: float
        If the top two FAISS scores differ by less than this value and
        ``api_key`` is provided, the AI comparison step is used to choose
        the best match.

    Returns
    -------
    dict
        Dictionary containing the screenshot path, FAISS results and the
        chosen baseline path.
    """
    if run_dir is None:
        run_dir = create_run_directory()

    screenshot_path = take_window_screenshot(window_title, run_dir, function_type)
    results = search(screenshot_path, top_k=top_k)

    best_path = results[0][0] if results else None

    if (
        api_key
        and len(results) > 1
        and abs(results[0][1] - results[1][1]) < similarity_threshold
    ):
        # Use AI analysis to disambiguate between close scores
        ai_scores: List[Tuple[str, float]] = []
        for candidate, _score in results:
            ai_result = compare_with_ai(
                screenshot_path, candidate, api_key, function_type
            )
            confidence = ai_result.get("confidence", 0.0)
            if not ai_result.get("functionality_match", True):
                confidence = 0.0
            ai_scores.append((candidate, confidence))
        ai_scores.sort(key=lambda x: x[1], reverse=True)
        if ai_scores:
            best_path = ai_scores[0][0]

    return {
        "screenshot": screenshot_path,
        "faiss_results": results,
        "best_match": best_path,
    }
