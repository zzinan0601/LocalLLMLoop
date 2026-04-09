from graph.graph import build_graph

def main():
    graph = build_graph()

    question = input("질문을 입력하세요: ")

    # 초기 상태
    initial_state = {
        "question"       : question,
        "current_answer" : "",
        "loop_count"     : 0,
        "is_good"        : False,
    }

    print("\n" + "="*50)

    loop_count = 0

    # stream_mode="messages" → LLM 토큰 단위로 실시간 출력
    for token, metadata in graph.stream(initial_state, stream_mode="messages"):

        # 답변 노드에서 나오는 토큰만 출력
        if metadata.get("langgraph_node") == "answer":

            # 새 루프 시작 시 헤더 출력
            if token.id and loop_count != metadata.get("langgraph_step"):
                loop_count = metadata.get("langgraph_step")
                print(f"\n[답변 생성 중... {loop_count}회차]\n")

            # 토큰 단위로 즉시 출력 (줄바꿈 없이)
            print(token.content, end="", flush=True)

    print("\n" + "="*50)
    print("\n✅ 스트리밍 완료")


if __name__ == "__main__":
    main()
