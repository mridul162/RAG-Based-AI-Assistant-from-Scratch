from api.database.session import (
    SessionLocal
)

from api.repositories.conversation_repository import (
    ConversationRepository
)

from api.services.conversation_service import (
    ConversationService
)


def main():

    db = SessionLocal()

    try:

        repository = (
            ConversationRepository(db)
        )

        service = (
            ConversationService(
                repository
            )
        )

        phone_number = (
            "8801712345678"
        )

        # -----------------------------------------
        # SAVE USER MESSAGE
        # -----------------------------------------

        service.save_user_message(

            phone_number=phone_number,

            content=(
                "Tell me about Kholisha Honey."
            )
        )

        # -----------------------------------------
        # SAVE ASSISTANT MESSAGE
        # -----------------------------------------

        service.save_assistant_message(

            phone_number=phone_number,

            content=(
                "Kholisha Honey is a raw "
                "Sundarbans honey."
            )
        )

        # -----------------------------------------
        # GET HISTORY
        # -----------------------------------------

        history = (
            service.get_recent_history(

                phone_number=phone_number
            )
        )

        print("\nConversation History\n")

        for message in history.messages:

            print(
                f"{message.role}: "
                f"{message.content}"
            )

        # -----------------------------------------
        # CLEAR HISTORY
        # -----------------------------------------

        service.clear_history(
            phone_number
        )

        history = (
            service.get_recent_history(
                phone_number
            )
        )

        print(
            f"\nMessages after clear: "
            f"{len(history.messages)}"
        )

    finally:

        db.close()


if __name__ == "__main__":

    main()