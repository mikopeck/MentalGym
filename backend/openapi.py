import openai
import time
import requests
import json
import os

#### settings ####
max_retries = 5
delay = 3
request_timeout = 60

TOKEN_CAP = 500
LESSON_TOKENS = 1500

GPT3_5 = "gpt-4o-mini"
GPT4 = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-small"

def generate_response(user_id, messages, functions=None, function_call="none", model=GPT3_5, tokens=TOKEN_CAP):
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    for attempt in range(max_retries):
        try:
            data = {
                "user": str(user_id),
                "model": model,
                "messages": messages,
                "temperature": 0.1 if functions else 0.4,
                "max_tokens": tokens
            }

            if functions:
                data["functions"] = functions
                data["function_call"] = function_call
            #     print(f"Requesting {model} response..")
            #     print(f"{functions} mode {function_call}: \n{messages}")
            # else:
            print(f"Requesting {model} response: ", messages)

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=request_timeout
            )

            if response.status_code == 200:
                response_data = response.json()
                print(response_data)
                return response_data
            else:
                print(f"Request failed with status code {response.status_code}: {response.json()}")
                time.sleep(delay)

        except requests.exceptions.Timeout:
            print(f"Request timed out after {request_timeout} seconds. Retrying...")
            time.sleep(delay)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    else:
        print("Max retries reached. Unable to generate response.")
        return None

def moderate(user_input):
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "input": user_input
    }

    print(f"Attempting moderation of {user_input}")
    for attempt in range(max_retries):
        try:
            print(f"(Attempt {attempt + 1}/{max_retries})...")
            response = requests.post(
                "https://api.openai.com/v1/moderations",
                headers=headers,
                data=json.dumps(data),
                timeout=request_timeout
            )

            if response.status_code == 200:
                response_data = response.json()
                output = response_data["results"][0]
                violation = output["flagged"]
                print("Moderation completed successfully.")
                return violation, output
            else:
                print(f"Request failed with status code {response.status_code}. Retrying...")
                time.sleep(delay)

        except requests.exceptions.Timeout:
            print(f"Request timed out after {request_timeout} seconds. Retrying...")
            time.sleep(delay)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    else:
        print("Max retries reached. Unable to complete moderation.")
        return None, None
    

##### EMBEDDINGS #####

def get_embeddings(strings_list):
    print(f"embedding {strings_list}")
    if not strings_list:
        return None
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers=headers,
            json={
                "input": strings_list,
                "model": EMBEDDING_MODEL
            }
        )

        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    

def get_image(prompt):
    # Enhance the prompt 
    system_message = {
        "role": "system",
        "content": "Your task is to reply with a description of a desired image, including scenery, characters, atmosphere, other objects, and any specific styles or themes to match the topic. Feel free to make up the specific decorations and scenery so that it is maximally related to the topic of the library - focus on maybe two or three specific things to include of your own choosing to depict the topic. Reply only with an improved image description."
    }
    user_message = {
        "role": "user",
        "content": prompt
    }
    response = generate_response("system", [system_message, user_message])
    enhanced_prompt = response["choices"][0]["message"]["content"]
    
    # Fal Flux/shnell
    headers = {
        "Authorization": f'Key {os.getenv("FAL_API_KEY")}',
        "Content-Type": "application/json"
    }

    for attempt in range(max_retries):
        try:
            data = {
                "prompt": enhanced_prompt,
                "image_size": "square",
                "num_inference_steps": 4,
                "num_images": 1,
            }

            response = requests.post(
                "https://fal.run/fal-ai/flux/schnell",
                headers=headers,
                data=json.dumps(data),
                timeout=request_timeout
            )

            if response.status_code == 200:
                response_data = response.json()
                print(response_data['images'][0]['url'])
                return response_data['images'][0]['url']
            else:
                print(f"Request failed with status code {response.status_code}: {response.json()}")
                time.sleep(delay)

        except requests.exceptions.Timeout:
            print(f"Request timed out after {request_timeout} seconds. Retrying...")
            time.sleep(delay)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    else:
        print("Max retries reached. Unable to generate image.")
        return None
