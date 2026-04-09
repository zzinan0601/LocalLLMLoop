from graph.state import GraphState
from llm.ollama_client import llm
from prompts.templates import ANSWER_PROMPT, ANSWER_IMPROVE_PROMPT, JUDGE_PROMPT

MAX_LOOP = 3  # 최대 루프 횟수


# ── 답변 노드 ──────────────────────────────────────────
def answer_node(state: GraphState) -> GraphState:

    question       = state["question"]
    current_answer = state.get("current_answer", "")
    loop_count     = state.get("loop_count", 0)

    # 첫 번째면 기본 프롬프트 / 이후엔 개선 프롬프트
    if not current_answer:
        prompt = ANSWER_PROMPT.format(question=question)
    else:
        prompt = ANSWER_IMPROVE_PROMPT.format(
            question       = question,
            current_answer = current_answer,
        )

    print(f"\n[답변 노드] loop {loop_count + 1}회차 답변 생성 중...")
    response = llm.invoke(prompt)

    return {
        **state,
        "current_answer" : response.content,
        "loop_count"     : loop_count + 1,
    }


# ── 판단 노드 ──────────────────────────────────────────
def judge_node(state: GraphState) -> GraphState:

    question       = state["question"]
    current_answer = state["current_answer"]
    loop_count     = state["loop_count"]

    # 최대 횟수 도달 시 강제 종료
    if loop_count >= MAX_LOOP:
        print(f"\n[판단 노드] 최대 루프({MAX_LOOP}회) 도달 → 종료")
        return {**state, "is_good": True}

    prompt   = JUDGE_PROMPT.format(
        question       = question,
        current_answer = current_answer,
    )
    response = llm.invoke(prompt)
    result   = response.content.strip().upper()

    is_good = "GOOD" in result
    print(f"\n[판단 노드] 판단 결과: {result} → {'종료' if is_good else 'loop 재시도'}")

    return {**state, "is_good": is_good}


# ── 분기 함수 (Conditional Edge) ───────────────────────
def should_loop(state: GraphState) -> str:
    if state["is_good"]:
        return "end"
    return "answer"  # 답변 노드로 되돌아감
