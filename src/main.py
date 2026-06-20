# src/main.py

from config import MODEL
from litellm import completion
from prompts import SYSTEM_PROMPT


def chat(message: str, history: list) -> str:
    history.append({"role": "user", "content": message})
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    
    response = completion(
        model=MODEL["model"],
        api_key=MODEL["api_key"],
        api_base=MODEL["api_base"],
        messages=messages
    )

    answer = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": answer})
    
    return answer


def main():
    print("=== FoxTales AI ===")
    print("Введи 'выход' чтобы завершить\n")
    
    history = []
    
    while True:
        user_input = input("Ты: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ("выход", "exit", "quit"):
            print("Пока!")
            break
        
        print("Думаю...")
        answer = chat(user_input, history)
        print(f"\nИИ: {answer}\n")


if __name__ == "__main__":
    main()