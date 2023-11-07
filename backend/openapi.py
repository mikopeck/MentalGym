import openai
import time

#### settings ####
max_retries=10
delay=10

TOKEN_CAP = 500
LESSON_TOKENS = 1000

GPT3_5 = "gpt-3.5-turbo"
GPT4 = "gpt-4"

def generate_response(user_id, messages, functions = None, function_call = "none", model = GPT3_5, tokens=TOKEN_CAP):
    for attempt in range(max_retries):
        try:
            if functions:
                print(f"Requesting {model} response {tokens}: \n{messages}\n--FNS:{functions}")
                response = openai.ChatCompletion.create(
                    user=str(user_id),
                    model=model,
                    messages=messages,
                    functions=functions,
                    function_call=function_call,
                    temperature=0.1,
                    max_tokens=tokens
                )
                print(response)
                return response
            else:
                print("Requesting AI response: ", messages)
                response = openai.ChatCompletion.create(
                    user=str(user_id),
                    model=model,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=tokens
                )
                print(response)
                return response
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    else:
        print("Max retries reached. Unable to generate response.")
        return None

def moderate(user_input):
    response = openai.Moderation.create(input=user_input)
    output = response["results"][0]
    violation = output["flagged"]
    return violation, output