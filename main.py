import requests
from bs4 import BeautifulSoup
import json
import os
import re

# ==============================
# 🔧 Ollama 설정
# ==============================
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"

# ==============================
# 🛠 Tool 구현
# ==============================

def search_namu(keyword):
    print(f"[Tool] 나무위키 검색: {keyword}")

    url = f"https://namu.wiki/w/{keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()
        cleaned = text.strip().replace("\n", " ")

        return cleaned[:1000]
    except Exception as e:
        return f"검색 실패: {e}"


def write_file(filename, content):
    print(f"[Tool] 파일 저장: {filename}")

    try:
        os.makedirs("data", exist_ok=True)
        path = os.path.join("data", filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"{filename} 저장 완료"
    except Exception as e:
        return f"파일 저장 실패: {e}"


def read_file(filename):
    print(f"[Tool] 파일 읽기: {filename}")

    try:
        path = os.path.join("data", filename)

        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"파일 읽기 실패: {e}"


TOOLS = {
    "search_namu": search_namu,
    "write_file": write_file,
    "read_file": read_file
}

# ==============================
# 🤖 LLM 호출
# ==============================

def call_llm(messages):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False
        }
    )
    return response.json()["message"]


# ==============================
# 🧠 Agent 핵심 로직
# ==============================

def extract_json(text):
    """LLM 응답에서 JSON만 추출"""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        return None
    return match.group()


def run_agent(user_input):
    messages = [
        {
            "role": "system",
            "content": """
너는 AI 에이전트다.

반드시 JSON 형식으로만 응답해라.

규칙:
- 한 번에 하나의 tool만 호출하라
- 설명 문장 없이 JSON만 출력하라
- 이전 tool 결과를 다음 단계에서 활용하라

사용 가능한 tool:
- search_namu(keyword)
- write_file(filename, content)

응답 형식:

{
  "tool_calls": [
    {
      "name": "search_namu",
      "arguments": {"keyword": "젤다"}
    }
  ]
}

또는

{
  "content": "최종 결과"
}
"""
        },
        {"role": "user", "content": user_input}
    ]

    last_result = ""

    for step in range(5):
        response = call_llm(messages)

        print(f"\n[LLM 응답 {step+1}]")
        print(response["content"])

        # ✅ JSON 추출
        json_str = extract_json(response["content"])

        if not json_str:
            print("❌ JSON 없음 → 종료")
            break

        # ✅ JSON 파싱
        try:
            data = json.loads(json_str)
        except:
            print("❌ JSON 파싱 실패 → 종료")
            break

        # ✅ Tool 처리
        if "tool_calls" in data:
            tool_call = data["tool_calls"][0]

            name = tool_call["name"]
            args = tool_call["arguments"]

            # 이전 결과 자동 삽입
            if "content" in args and args["content"] == "":
                args["content"] = last_result

            print(f"\n[Tool 호출] {name} | args: {args}")

            if name in TOOLS:
                try:
                    result = TOOLS[name](**args)
                except Exception as e:
                    result = f"Tool 실행 오류: {e}"
            else:
                result = "존재하지 않는 tool"

            print(f"[Tool 결과] {result[:200]}...")

            last_result = result

            # 다음 단계로 전달
            messages.append({
                "role": "assistant",
                "content": f"tool_result: {result}"
            })

        elif "content" in data:
            print("\n[최종 결과]")
            print(data["content"])
            break

        else:
            print("❌ 알 수 없는 응답 형식")
            break


# ==============================
# ▶ 실행
# ==============================

if __name__ == "__main__":
    print("✅ AI 에이전트 시작 (종료: exit)\n")

    while True:
        user_input = input("질문 >> ")

        if user_input.lower() == "exit":
            break

        run_agent(user_input)