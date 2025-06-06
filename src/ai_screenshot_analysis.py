# src/ai_screenshot_analysis.py
import json

from src.utils import take_window_screenshot, create_run_directory, archive_old_runs

import os
import base64
import requests


def compare_with_ai(screenshot_path, example_image_path, api_key, function_type):
    # 读取并编码图片
    with open(screenshot_path, "rb") as image_file:
        screenshot_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    with open(example_image_path, "rb") as image_file:
        example_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # 准备API请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

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
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{screenshot_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500,
        "response_format": {"type": "json_object"}
    }

    # 发送API请求
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()
    # print (result)
    # 解析并返回结果
    ai_assessment = result['choices'][0]['message']['content']
    # 检查并清理字符串
    if '```' in ai_assessment:
        ai_assessment = ai_assessment.replace('```json\n', '').replace('\n```', '')
        ai_assessment = ai_assessment.replace('```', '')  # 以防万一还有其他格式的代码块标记

    # 打印清理后的字符串，用于调试
    print("Cleaned assessment:", ai_assessment)
    return json.loads(ai_assessment)


def analyze_screenshot(window_title, example_image_path, api_key, function_type):
    run_dir = create_run_directory()

    try:
        screenshot_path = take_window_screenshot(window_title, run_dir, function_type)
        ai_result = compare_with_ai(screenshot_path, example_image_path, api_key, function_type)

        # 保存 AI 分析结果
        result_path = os.path.join(run_dir, f"{function_type}_analysis_result.json")
        with open(result_path, 'w') as f:
            json.dump(ai_result, f, indent=2)

        return ai_result
    finally:
        # 存档旧的运行
        archive_old_runs()
if __name__ == '__main__':
    # 使用示例
    api_key = "sk-XDqRTRrsImefMErTQDJt2lyla2exNLY9UnDx6Z-uiTT3BlbkFJcv1Rv7iwR8YbvKaXPJo_gdgl5WYTW1mhBmnIIBpjkA"
    window_title = "Chrome"
    example_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'baseline_images', 'freeze_example.png')
    function_type = "freeze"

    result = analyze_screenshot(window_title, example_image_path, api_key, function_type)
    print(result)