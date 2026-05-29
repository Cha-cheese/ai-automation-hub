from app.agents.llm import call_ai


def automation_graph(state):

    user_input = state.get("user_input", "")

    result = call_ai(user_input)

    return {
        "result": result,
        "intent": "success"
    }

@app.post("/automate")
def automate(req: AutomateReq, authorization: str = Header(None)):

    try:

        if not authorization:
            return {"error": "missing token"}

        user = verify_token(authorization)

        if not user:
            return {"error": "unauthorized"}

        result = automation_graph({"user_input": req.message})

        return result

    except Exception as e:

        return {
            "error": "safe_fallback",
            "detail": str(e)
        }