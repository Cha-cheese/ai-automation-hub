def calendar_agent(user_input: str):

    try:

        return {
            "status": "created",
            "event_link": None
        }

    except Exception as e:

        return {
            "status": "error",
            "error": str(e)
        }