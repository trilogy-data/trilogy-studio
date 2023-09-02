import sys
from pathlib import Path

import dotenv

dotenv.load_dotenv()
current_directory = Path(__file__).parent.parent
# Add the current directory to the PYTHONPATH

sys.path.append(str(current_directory))
from backend.conversations.characters import PARTIES, PLAYER
from backend.conversations.engine import PersonalityEngine
from backend.conversations.guardrails import ConversationalGuardrail
from backend.conversations.inventory import PROLOGUE
from backend.conversations.models import (
    Conversation,
    Message,
    SingleConversation,
    Visibility,
)


def render_convo(input: Conversation):
    for msg in input.messages:
        print(msg.role, msg.content)


if __name__ == "__main__":
    engine = PersonalityEngine()

    guardrail = ConversationalGuardrail()
    convo = SingleConversation.start(PROLOGUE, with_party=PARTIES["gordon"])

    engine.tick(convo)
    convo.messages.append(
        Message(
            role="user",
            content="As an AI, I don't have feelings.",
            party=PLAYER,
            visibility=Visibility.PUBLIC,
        )
    )
    print("---")
    engine.tick(convo)

    # render_convo(convo)
    # print('---')
    new = guardrail.validate(convo)
    print(render_convo(new))
