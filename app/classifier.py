from flask import Flask, request
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    query = data['query']
    classes = data['classes']
    options = data.get('options', {})
    show_reasoning = options.get('show_reasoning', False)
    multilabel = options.get('multilabel', False)

    client = OpenAI()

    response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model = "gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": f"Classify the given text into one or more of the following classes with class IDs:\n"
                f"{classes}"
                "The result should be a json string with the following format:"
                """
                {{
                    "result": ["{THE CLASSIFICATION RESULT CLASS ID}"],
                    "reasoning": "The reasoning behind the classification"
                }}
                """
            },
            {
                "role": "user",
                "content": query
            }
        ],
        response_format={'type':'json_object'},
        temperature=0.0,)

    result = response.choices[0].message.content
    result = json.loads(result)

    assert isinstance(result, dict), f"result is not a dictionary: {result}"
    
    if not show_reasoning:
        result.pop('reasoning', None)
    if not multilabel:
        result['result'] = [result['result'][0]]

    print(f'\n{query}: {result}')

    return result

if __name__ == '__main__':
    app.run(port=8000,debug=True)
