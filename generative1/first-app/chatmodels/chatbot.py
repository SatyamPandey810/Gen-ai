from langchain_ollama import ChatOllama
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

SYSTEM_PROMPT = "You are a coding Ai agent"
EXIT_WORDS = ["exit", "quit", "bye"]

# Personas shown as choices in the Streamlit UI (app.py).
# To add a new one, just add another entry here.
PERSONAS = {
    "Coding": {
        "emoji": "💻",
        "title": "Coding Agent",
        "tagline": "Bugs, code, architecture. Jo bhi poochho.",
        "accent": "#2F6FED",
        "prompt": SYSTEM_PROMPT,
        "welcome": "Namaste! Main tumhara coding agent hoon. Code, bug ya design, kuch bhi share karo.",
    },
    "Funny": {
        "emoji": "🎭",
        "title": "Funny Agent",
        "tagline": "Jawab milega, hasi ke saath.",
        "accent": "#F29A0B",
        "prompt": "You are a funny Ai agent",
        "welcome": "Namaste! Main tumhara funny AI agent hoon. Aaj kya poochna hai?",
    },
    "Teacher": {
        "emoji": "📚",
        "title": "Teacher",
        "tagline": "Kuch bhi simple steps mein samjhega.",
        "accent": "#16A07A",
        "prompt": "You are a strict but kind teacher. Explain everything in simple steps with small examples.",
        "welcome": "Hello! Aaj kya seekhna hai? Topic batao, main step by step samjhaunga.",
    },
    "Friend": {
        "emoji": "🤝",
        "title": "Friend",
        "tagline": "Bina judge kiye, dil se baat.",
        "accent": "#E0508A",
        "prompt": "You are a calm and supportive friend. Reply in short, warm sentences.",
        "welcome": "Hey! Bolo, kya chal raha hai?",
    },
    "Sarcastic": {
        "emoji": "😏",
        "title": "Sarcastic Agent",
        "tagline": "Taane milenge, par jawab sahi.",
        "accent": "#7A5AF8",
        "prompt": "You are a sarcastic assistant who still gives correct and useful answers.",
        "welcome": "Oh wow, ek aur sawal. Chalo, poocho.",
    },
    "Desi Dost": {
        "emoji": "🧢",
        "title": "Desi Dost",
        "tagline": "Pure Hinglish mein yaari.",
        "accent": "#E4692B",
        "prompt": "Tum ek desi dost ho jo hamesha Hinglish (Hindi + English mix) mein baat karta hai.",
        "welcome": "Aur bhai, kya haal hai? Bol, kya scene hai?",
    },
}

model = ChatOllama(model="llama3.2")


def new_history(prompt=SYSTEM_PROMPT):
    """Fresh conversation with the given system prompt."""
    return [SystemMessage(content=prompt)]


# ---------- Terminal version (same as before) ----------
if __name__ == "__main__":
    messages = new_history()

    while True:
        prompt = input("You: ")

        messages.append(HumanMessage(content=prompt))
        if prompt.lower() in EXIT_WORDS:
            print("AI: Goodbye!")
            break

        response = model.invoke(messages)
        messages.append(AIMessage(content=response.content))
        print("Bot :", response.content)

    print(messages)