"""
query_rewrite_service.py

Purpose:
--------
Rewrite conversational follow-up questions into
standalone retrieval-friendly queries.

Responsibilities:
-----------------
- Use conversation history
- Resolve references and pronouns
- Preserve user intent
- Improve retrieval quality

Architecture Philosophy:
------------------------
History-aware retrieval.
Minimal query transformation.
Retriever-first design.
"""

from openai import OpenAI

from api.models.conversation import (
    ConversationHistory
)


# ---------------------------------------------------------
# QUERY REWRITE SERVICE
# ---------------------------------------------------------

class QueryRewriteService:

    """
    Converts follow-up questions into
    standalone retrieval queries.
    """

    # -----------------------------------------------------

    def __init__(
        self,
        model_name: str = "gpt-4.1-mini",
    ):

        self.client = OpenAI()

        self.model_name = model_name

    # -----------------------------------------------------

    def rewrite(
        self,
        query: str,
        history: ConversationHistory,
    ) -> str:

        """
        Rewrite a conversational query into a
        standalone retrieval query.
        """

        conversation_text = (
            self._format_history(
                history
            )
        )

        system_prompt = """
You rewrite user questions for retrieval.

Your goal is to convert follow-up questions
into standalone search queries.

Rules:

1. Preserve the original intent.
2. Use conversation history when needed.
3. Resolve references such as:
   - it
   - this
   - that
   - eta
   - eita
   - ota
   - oita
   - oi product
4. Do not answer the question.
5. Return only the rewritten query.
6. If no rewrite is needed,
   return the original query.
"""

        user_prompt = f"""
Conversation History:

{conversation_text}

Current Query:

{query}

Rewritten Query:
"""

        response = (
            self.client.chat.completions.create(

                model=self.model_name,

                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],

                temperature=0,
            )
        )

        rewritten_query = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return rewritten_query

    # -----------------------------------------------------

    def _format_history(
        self,
        history: ConversationHistory,
    ) -> str:

        if not history.messages:

            return (
                "No previous conversation."
            )

        lines = []

        for message in history.messages:

            lines.append(

                f"{message.role.title()}: "

                f"{message.content}"
            )

        return "\n".join(lines)