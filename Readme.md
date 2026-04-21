# ChatGPT Command Line Interface

A Python program that lets you chat with ChatGPT in the terminal, with support for different modes, temperature settings, and conversation management.

## Setup

1. Clone the repo
2. Install dependencies:
   ```
   pip install openai python-dotenv
   ```
3. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-key-here
   ```
4. Run:
   ```
   py chatgpt.py
   ```

## Commands

| Command | Description |
|---|---|
| `/tutor` | Switch to tutor mode (patient, educational) |
| `/coach` | Switch to coach mode (motivational, direct) |
| `/basic` | Lower temperature — more predictable responses |
| `/creative` | Higher temperature — more imaginative responses |
| `/removelast` | Remove the last exchange from conversation history |
| `/compact` | Summarize the conversation history to save context space |
| `/quit` | Exit the program |

## Notes

- Conversation history is maintained within a session but does not persist after the program exits.
- Never commit your `.env` file — your API key should stay private.
