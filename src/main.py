# src/main.py
from config import MODEL
from agent import run_agent
from prompts import SYSTEM_PROMPT  # ← было load_system_prompt

def main():
    print("=== FoxTales AI ===\n")
    
    history = []

    while True:
        user_input = input("Ты: ").strip()
        
        if not user_input:
            continue
        if user_input.lower() in ("выход", "exit", "quit"):
            print("Пока!")
            break

        print("Думаю...")
        answer = run_agent(user_input, history, SYSTEM_PROMPT)  # ← было system_prompt
        print(f"\nИИ: {answer}\n")

if __name__ == "__main__":
    main()