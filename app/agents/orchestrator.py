from app.agents.llm import build_gemini_llm
from app.tools.tools import get_emails, send_slack, create_calendar_event

llm = build_gemini_llm()


def automation_graph(state):

    user_input = state["user_input"]

    # 🧠 STEP 1: INTENT DETECTION
    intent_prompt = f"""
    Classify this request:
    - email
    - slack
    - calendar
    - general

    Input: {user_input}
    """

    intent = str(llm.invoke(intent_prompt)).lower()

    state["intent"] = intent

    # 🧠 STEP 2: ROUTING

    if "email" in intent:
        result = get_emails()

    elif "slack" in intent:
        result = send_slack(user_input)

    elif "calendar" in intent:
        result = create_calendar_event(user_input)

    else:
        result = llm.invoke(user_input)

    state["final_response"] = str(result)

    return state