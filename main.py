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
    result = graph.invoke(initial_state)
    print("\n" + "="*50)
    print("\n✅ 최종 답변:\n")
    print(result["current_answer"])
    print(f"\n(총 {result['loop_count']}회 loop)")


if __name__ == "__main__":
    main()
