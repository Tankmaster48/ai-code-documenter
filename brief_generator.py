import os, time
from openai import OpenAI

# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

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

    func_content = get_func()

    messages.append(
        {"role" : "user", "content" : DOCUMENTATION_PROMPT.format(func_content=func_content)}
    )

    return llm_call(messages)


def llm_call(messages):
    completion = client.chat.completions.create(
        model="Qwen/Qwen3-32B-AWQ",
        messages=messages,
    )

    return completion.choices[0].message.content
    
if __name__ == '__main__':
    main()
