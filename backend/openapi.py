import openai
import time

#### settings ####
max_retries=10
delay=10

def generate_response(messages, functions = None, function_call = "none"):
    for attempt in range(max_retries):
        try:
            if functions:
                print("Requesting AI response: ", messages, functions)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    functions=functions,
                    function_call=function_call,
                    temperature=0.1
                )
                print(response)
                return response
            else:
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
