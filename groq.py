import pandas as pd
import requests
import PyPDF2


def get_chat_completions(api_key, messages, model="gpt-4-turbo"): #gpt-4-turbo, llama3-70b-8192

    url = "https://api.openai.com/v1/chat/completions" #https://api.openai.com/v1/chat/completions, https://api.groq.com/openai/v1/chat/completions
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {
        "model": model,
        "messages": messages,
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        # "stream": False,
        "stop": None,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")

def get_excel_data():   
    excel_file = "company.xlsx"
    df = pd.read_excel(excel_file)
    return df.to_markdown(index=False)

def get_pdf_data():
    with open("colgate.pdf", 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

if __name__ == "__main__":
    # Example usage:
    api_key = ""
    prompt = f"Summarize the following text based on 'Priority' and 'Description' column strictly in 50 words. summerize in order  of priority for all :\n {get_excel_data()}"
    # print(prompt)
    messages = [
        # {
        #     "role": "system",
        #     "content": "response in json"
        # },
        {"role": "user", "content": prompt}
    ]
    response = get_chat_completions(api_key, messages)
    print(response["choices"][0]["message"]["content"])
