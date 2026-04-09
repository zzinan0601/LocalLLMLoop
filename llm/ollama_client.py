from langchain_ollama import ChatOllama

# Ollama 서버 주소 및 모델 설정
# 모델명은 ollama pull 로 받은 이름으로 변경하세요
llm = ChatOllama(
    model       = "qwen2.5:7b",
    base_url    = "http://localhost:11434",
    temperature = 0.7,
)
