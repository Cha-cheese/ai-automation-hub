from app.core.llm import call_llm


def summarizer_agent(emails):

    prompt = f"""
    Summarize these emails in short form:
    {emails}
    """

    return call_llm(prompt)