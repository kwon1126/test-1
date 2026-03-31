# Python AI Agent (Ollama + Namuwiki)

이 프로젝트는 로컬 LLM(Ollama)을 사용하여 자율적으로 사고하고 도구(Tools)를 활용해 사용자의 요청을 처리하는 간단한 **ReAct 기반의 AI 에이전트**입니다.

현재 에이전트는 사용자의 질문을 분석해 직접 **나무위키를 검색**하고, 필요한 정보를 파싱하여 **파일로 저장**하는 과정을 자율적으로 수행할 수 있습니다.

## ✨ 주요 기능 (Features)

* **자율적인 도구 사용 (Tool Calling)**: 에이전트가 어떤 도구를 사용할지, 어떤 매개변수를 전달할지 스스로 판단합니다.
* **웹 검색 (search_namu)**: 나무위키에서 특정 키워드를 검색하여 본문 텍스트를 파싱(1,000자 이내)해옵니다. (BeautifulSoup 기반)
* **파일 읽기/쓰기 (write_file, read_file)**: 작업한 결과나 검색한 내용을 프로젝트 내 `data/` 디렉터리에 자동으로 저장하고 읽어올 수 있습니다.
* **JSON 안정성 (Robust Parsing)**: LLM이 반환한 응답에서 정규식을 이용해 순수 JSON만을 추출하며, 파싱 오류를 방지합니다.
* **Context Wiring (자동 컨텍스트 주입)**: LLM이 이전 단계에서 얻은 결과를 다음 단계 도구의 인자로 보낼 때 문맥을 자동으로 이어줍니다.

## 🛠 필수 조건 (Prerequisites)

이 프로젝트를 실행하기 위해 다음 환경이 필요합니다.

1. **Python 3.x**
2. **필수 라이브러리** (`requests`, `beautifulsoup4`)
    ```bash
    pip install requests beautifulsoup4
    ```
3. **Ollama (로컬 실행 환경)**
    * [Ollama 공식 홈페이지](https://ollama.com/)에서 다운로드 후 실행
    * 기본적으로 `qwen2.5-coder:7b` 모델을 사용하도록 설정되어 있습니다. (코드 내 `MODEL` 변수에서 변경 가능)
    ```bash
    ollama run qwen2.5-coder:7b
    ```

## 🚀 사용 방밥 (Usage)

터미널이나 명령 프롬프트에서 `main.py`를 실행합니다.

```bash
python main.py
```

실행 후 "질문 >>" 프롬프트가 나타나면 원하는 작업을 명령할 수 있습니다.

**예시 프롬프트:**
> 질문 >> 젤다에 대해 검색해서 파일로 저장해줘
> 질문 >> 파이썬의 역사에 대해 나무위키에서 찾고 python_history.txt로 저장해봐

## 📁 디렉터리 구조

```text
📦 project/
 ┣ 📜 main.py       # 핵심 에이전트 실행 로직 및 Tools 정의
 ┣ 📜 README.md     # 프로젝트 설명 파일
 ┗ 📂 data/         # 에이전트가 결과물을 저장하거나 읽어오는 작업 디렉터리
```

## ⚙️ 상세 설정

* `main.py` 내부의 `OLLAMA_URL` 변수를 수정하여 외부 API 서버로 연결을 변경할 수 있습니다.
* `TOOLS` 딕셔너리에 커스텀 파이썬 함수를 추가하고, LLM 시스템 프롬프트를 수정하면 얼마든지 새로운 도구를 에이전트에게 쥐어줄 수 있습니다.
