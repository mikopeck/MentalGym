import openai

def generate_response(messages):
    print("Requesting AI response: ",messages)
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            top_p=0.1
        )
    print(response)
    return response

def append_assistant_response(session, response):
        ai_message = response['choices'][0]['message']['content']

        session['messages'].append(
            {
                "role": "assistant",
                "content": ai_message
            }
        )

def append_user_message