from typing import TypedDict

class GraphState(TypedDict):
    question       : str   # 원본 질문 (변하지 않음)
    current_answer : str   # 현재 답변 (loop마다 갱신)
    loop_count     : int   # 현재 루프 횟수
    is_good        : bool  # 판단 결과
