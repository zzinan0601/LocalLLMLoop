from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes import answer_node, judge_node, should_loop


def build_graph():

    builder = StateGraph(GraphState)

    # 노드 등록
    builder.add_node("answer", answer_node)
    builder.add_node("judge",  judge_node)

    # 시작점 설정
    builder.set_entry_point("answer")

    # 엣지 연결
    builder.add_edge("answer", "judge")  # 답변 → 판단 (항상)

    # 판단 → 분기 (loop or 종료)
    builder.add_conditional_edges(
        "judge",
        should_loop,
        {
            "answer" : "answer",  # NO  → 답변 노드로
            "end"    : END,       # YES → 종료
        }
    )

    return builder.compile()
