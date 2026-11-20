from .chatbot import DiabetesChatbot


def main():
    bot = DiabetesChatbot()
    print("Diabetes info assistant (educational only, not medical advice). Type 'quit' to exit.\n")
    while True:
        try:
            msg = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if msg.lower() in {"quit", "exit"}:
            break
        if not msg:
            continue
        result = bot.respond("cli", msg)
        print(f"\nBot: {result['answer']}")
        if result["sources"]:
            print("Sources: " + "; ".join(result["sources"]))
        print()


if __name__ == "__main__":
    main()
