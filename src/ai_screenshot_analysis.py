# src/ai_screenshot_analysis.py
import base64
import json
import os

import requests

from src.utils import archive_old_runs, create_run_directory, take_window_screenshot


def compare_with_ai(screenshot_path, example_image_path, api_key, function_type):
    # Read and encode the images
    with open(screenshot_path, "rb") as image_file:
        screenshot_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    with open(example_image_path, "rb") as image_file:
        example_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    # Prepare the API request
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    prompt = f"""You are an AI assistant specializing in analyzing browser extension functionality.
    You will be presented with two images:
    1. An example image showing the expected {function_type.upper()} functionality.
    2. A screenshot of the actual browser extension in use.

    Your task is to:
    1. Compare the two images.
    2. Determine if the screenshot accurately demonstrates the {function_type.upper()} functionality.
    3. Provide your assessment, confidence level, and detailed reasoning.

    Please format your response as a JSON object with the following keys:
    - "functionality_match": A boolean indicating whether the screenshot matches the expected {function_type.upper()} functionality.
    - "confidence": A float between 0 and 1 representing your confidence in the assessment.
    - "reasoning": A string explaining your analysis and decision.
    - "observed_differences": A list of strings describing any notable differences between the example and the screenshot.
    - "ui_elements_present": A list of strings naming key UI elements you can identify in the screenshot.

    Ensure your response can be parsed as valid JSON."""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{example_base64}"
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{screenshot_base64}"
                        },
                    },
                ],
            }
        ],
        "max_tokens": 500,
        "response_format": {"type": "json_object"},
    }

    # Send the API request
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    result = response.json()
    # print (result)
    # Parse and return the result
    ai_assessment = result["choices"][0]["message"]["content"]
    # Check and clean up the string
    if "```" in ai_assessment:
        ai_assessment = ai_assessment.replace("```json\n", "").replace("\n```", "")
        ai_assessment = ai_assessment.replace(
            "```", ""
        )  # In case there are other types of code block markers

    # Print the cleaned string for debugging
    print("Cleaned assessment:", ai_assessment)
    return json.loads(ai_assessment)


def analyze_screenshot(window_title, example_image_path, api_key, function_type):
    run_dir = create_run_directory()

    try:
        screenshot_path = take_window_screenshot(window_title, run_dir, function_type)
        ai_result = compare_with_ai(
            screenshot_path, example_image_path, api_key, function_type
        )

        # Save the AI analysis result
        result_path = os.path.join(run_dir, f"{function_type}_analysis_result.json")
        with open(result_path, "w") as f:
            json.dump(ai_result, f, indent=2)

        return ai_result
    finally:
        # Archive old runs
        archive_old_runs()


if __name__ == "__main__":
    # Example usage
    api_key = os.getenv("OPENAI_API_KEY")
    window_title = "Chrome"
    example_image_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "resources",
        "baseline_images",
        "freeze_example.png",
    )
    function_type = "freeze"

    result = analyze_screenshot(
        window_title, example_image_path, api_key, function_type
    )
    print(result)
