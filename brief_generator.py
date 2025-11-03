import os, time

import ollama

model = "gpt-oss:20b"

SYSTEM_PROMPT = "You are a documentation writer who writes documentation for the Named-Data Networking Go codebase"
DOCUMENTATION_PROMPT = """{func_content}

Understand the logic and semantics of this function. Then, write a brief one sentence description of what this function does for documentation.

Example: Constructs an unsigned Data packet with given name and empty Content.
"""

def main():
    import func_fetch
    while True:
        func_code = get_func()
        brief = generate_func_brief(func_code)
        print(brief)
        
def get_func(func_name: str = None, func_class: str = None):
    if not func_name:
        func_name = input("Function name as Class.Function if method has name reused, or just Function if not: ")

    if '.' in func_name:
        func_class = func_name.split('.')[0]
        func_name = func_name.split('.')[1]

    code = func_fetch.fetch_func(func_name, func_class)    
    
    return code

def generate_func_brief(func_code):
    messages = [
        {"role" : "system", "content" : SYSTEM_PROMPT}
    ]

    messages.append(
        {"role" : "user", "content" : DOCUMENTATION_PROMPT.format(func_content=func_code)}
    )

    return llm_call(messages)


def llm_call(messages):
    response = ollama.chat(model, messages=messages).message.content

    return response
    
if __name__ == '__main__':
    main()
