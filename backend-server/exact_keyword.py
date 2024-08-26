import os
from together import Together
client = Together(api_key=os.environ['together_api_key'])

def check_keyword_in_response(response_text, keyword):
    # Construct the prompt
    prompt = (
        f"I will provide you with a text and a keyword. "
        f"Your task is to check if the keyword is present in the text (ignore case). "
        f"If the keyword is present, return 'True'. Otherwise, return 'False'.\n\n"
        f"Text: {response_text}\n"
        f"Keyword: {keyword}\n\n"
        f"Please answer with True or False."
    )
    
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    
    model_response = response.choices[0].message.content.strip().lower()
    
    # Interpret the response
    if "true" in model_response:
        return True
    elif "false" in model_response:
        return False
    else:
        return ""
        