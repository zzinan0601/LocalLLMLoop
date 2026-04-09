# local-llm-loop

로컬 LLM(Ollama)으로 복합 질문을 loop 방식으로 반복 판단하여 답변 품질을 높이는 프로젝트

---

## 📁 프로젝트 구조

```
local-llm-loop/
│
├── main.py                     # 실행 진입점
├── requirements.txt            # 필요 패키지 목록
│
├── graph/
│   ├── state.py                # 상태 정의
│   ├── nodes.py                # 답변 / 판단 노드
│   └── graph.py                # 그래프 조립 및 분기 설정
│
├── llm/
│   └── ollama_client.py        # Ollama LLM 연결 설정
│
└── prompts/
    └── templates.py            # 프롬프트 템플릿 모음
```

---

## ⚙️ 실행 흐름

```
질문 입력
    ↓
[답변 노드] LLM이 답변 생성 (이전 답변 있으면 개선)
    ↓
[판단 노드] 답변이 충분한가?
    ├─ NO  → 답변 노드로 되돌아감 (최대 3회)
    └─ YES → 최종 답변 출력
```

---

## 🛠️ 사전 준비

### 1. Ollama 설치
- Ollama 공식 사이트에서 Windows 설치파일 다운로드
- 설치 후 실행 확인
```bash
ollama --version
```

### 2. 모델 다운로드
- 폐쇄망 환경이라면 외부망에서 사전에 pull 후 내부망으로 이동
```bash
ollama pull qwen2.5:7b
```
- 다른 모델 사용 시 `llm/ollama_client.py` 에서 `model` 값 변경

### 3. Ollama 서버 실행 확인
```bash
ollama serve
```
- 기본 주소: `http://localhost:11434`
- 서버가 실행 중이어야 LLM 호출 가능

---

## 📦 패키지 설치

```bash
pip install -r requirements.txt
```

### 폐쇄망 환경 (오프라인 설치)
외부망에서 패키지를 미리 다운로드 후 내부망으로 이동

```bash
# 외부망에서 다운로드
pip download -r requirements.txt -d ./wheelhouse

# 내부망에서 설치
pip install --no-index --find-links=./wheelhouse -r requirements.txt
```

---

## ▶️ 실행

```bash
python main.py
```

실행 후 터미널에 질문을 입력하면 됩니다.

---

## 🔧 설정 변경

| 항목 | 파일 | 변수 |
|------|------|------|
| 모델 변경 | `llm/ollama_client.py` | `model` |
| Ollama 주소 변경 | `llm/ollama_client.py` | `base_url` |
| 최대 루프 횟수 변경 | `graph/nodes.py` | `MAX_LOOP` |
| 프롬프트 수정 | `prompts/templates.py` | 각 템플릿 |

---

## 💡 실행 예시

```
질문을 입력하세요: 양자컴퓨터란 무엇이고 어디에 쓰이나요?

==================================================

[답변 노드] loop 1회차 답변 생성 중...
[판단 노드] 판단 결과: BAD → loop 재시도

[답변 노드] loop 2회차 답변 생성 중...
[판단 노드] 판단 결과: GOOD → 종료

==================================================

✅ 최종 답변:

양자컴퓨터는 ...

(총 2회 loop)
```

---

## 📋 개발 환경

- OS : Windows
- IDE : VS Code
- Python : 3.10 이상 권장
- 네트워크 : 폐쇄망 (오프라인)
