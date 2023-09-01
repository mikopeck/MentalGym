import openai
import time

def generate_response(messages, max_retries=10, delay=10):
    for attempt in range(max_retries):
        try:
            print("Requesting AI response: ", messages)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.2
            )
            print(response)
            return response
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    else:
        print("Max retries reached. Unable to generate response.")
        return None
    
def append_assistant_response(session, response):
    ai_message = response['choices'][0]['message']['content']

    session['messages'].append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )

def create_message(system_message, user_message):
    return [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

def initialize_session(session):
    session.setdefault('actions', [])
    session.setdefault('achievements', [])
    session['messages'].append(
        {
            "role": "assistant",
            "content": "Hello! I'm Azalea, and I'm here to help you grow and achieve your goals. Is there anything you like to learn about today?"
        }
    )