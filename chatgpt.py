import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODE = "tutor"
TEMPERATURE = "basic"
history = []
SYSTEM_PROMPT_TUTOR = "You are a patient and encouraging tutor who explains concepts clearly and checks for understanding."
SYSTEM_PROMPT_COACH = "You are a motivational coach who gives direct, energetic advice and pushes the user to take action."
SYSTEM_PROMPT_SUMMARY = ("Your job is to summarize a conversation into a single concise paragraph that can be used as context"
                         " for future messages. Capture all important facts, names, and topics discussed.")

def print_banner():
    print("\n=== ChatGPT Command Line Interface ===")
    print(f"Mode: {MODE}  |  Temp: {TEMPERATURE}")
    print("Commands: /tutor  /coach  /basic  /creative  /removelast  /compact  /quit")
    print("-" * 50)

def main():
    print_banner()

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            handle_command(user_input)
        else:
            handle_message(user_input)

def handle_command(cmd):
    global MODE, TEMPERATURE

    if cmd == "/tutor":
        if MODE == "tutor":
            print("→ Already in tutor mode.")
        else:
            MODE = "tutor"
            print("→ Switched to tutor mode.")

    elif cmd == "/coach":
        if MODE == "coach":
            print("→ Already in coach mode.")
        else:
            MODE = "coach"
            print("→ Switched to coach mode.")

    elif cmd == "/basic":
        if TEMPERATURE == "basic":
            print("→ Already in basic mode.")
        else:
            TEMPERATURE = "basic"
            print("→ Switched to basic mode (temp: 0.3).")

    elif cmd == "/creative":
        if TEMPERATURE == "creative":
            print("→ Already in creative mode.")
        else:
            TEMPERATURE = "creative"
            print("→ Switched to creative mode (temp: 0.9).")

    elif cmd == "/quit":
        print("Goodbye!")
        exit()

    elif cmd == "/removelast":
        if len(history) < 2:
            print("→ Nothing to remove.")
        else:
            history.pop()
            history.pop()
            print("→ Last exchange removed.")

    elif cmd == "/compact":
        if not history:
            print("→ Nothing to compact.")
        else:
            print("→ Compacting history...")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.3,
                messages=[
                             {"role": "system", "content": SYSTEM_PROMPT_SUMMARY},
                         ] + history + [
                             {"role": "user", "content": "Please summarize our conversation so far into one concise paragraph I can use as context going forward."}
                         ]
            )

            summary = response.choices[0].message.content

            history.clear()
            history.append({"role": "assistant", "content": f"Context from previous conversation: {summary}"})

            print("→ Done! History compacted into a summary.")

    else:
        print(f"→ Unknown command: {cmd}")


def handle_message(text):
    temp = 0.3 if TEMPERATURE == "basic" else 0.9

    history.append({"role": "user", "content": text})

    system_prompt = SYSTEM_PROMPT_TUTOR if MODE == "tutor" else SYSTEM_PROMPT_COACH

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=temp,
        messages=[{"role": "system", "content": system_prompt}] + history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    print(f"\nGPT: {reply}\n")


if __name__ == "__main__":
    main()
