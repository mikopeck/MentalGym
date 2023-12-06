import json
from datetime import datetime

import functions as fns
import roles as roles
import database.db_handlers as db
import message_handler as mh
from utils import extract_single_emoji, remove_emojis, remove_emojis_except_first
from openapi import generate_response, GPT4, LESSON_TOKENS

function_max_retries = 5
passing_grade = 60
profile_limit = 16
    
def gather_profile(user_id):
    messages = mh.prepare_session_messages(user_id)
    function = [fns.Profile]
    function_call = "auto"

    # Force profile if message limit
    if len(db.get_recent_messages(user_id)) == db.history_limit:
        mh.update_system_role(user_id, roles.ProfileCreate)
        messages = mh.prepare_session_messages(user_id)
        function_call = {"name": function[0]['name']}

    for attempt in range(function_max_retries):
        response = generate_response(user_id, messages, function, function_call)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            return response, None
        
        profile_data = try_get_object(fns.Profile, response_message)
        if profile_data:
            db.set_profile(user_id, json.dumps(profile_data))
            mh.update_system_role(user_id, roles.SuggestContent)
            return suggest_content(user_id, False, False)
                 
    print("ERROR: failed function!! defaulting to no functions...")
    mh.update_system_role(user_id, roles.ProfileGather)
    messages = mh.prepare_session_messages(user_id)
    return generate_response(user_id, messages), None

def suggest_content(user_id, set_challenge = False, set_lesson = True):
    messages = mh.prepare_session_messages(user_id)
    if not set_challenge and not set_lesson:
        response = generate_response(user_id, messages)
        identify_content(user_id, response["choices"][0]["message"]['content'])
        return response, None

    functions = [fns.Lesson]
    if set_challenge:
        functions += [fns.Challenge]
    function_call = "auto"

    for attempt in range(function_max_retries):
        response = generate_response(user_id, messages, functions, function_call)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            identify_content(user_id, response_message['content'])
            return response, None
        
        challenge_data = try_get_object(fns.Challenge, response_message)
        if challenge_data:
            challenge_emoji = extract_single_emoji(challenge_data.get('challenge_emoji'))
            if challenge_emoji:
                challenge_name = remove_emojis_except_first(challenge_emoji + challenge_data.get('challenge_name'))
            else:
                challenge_name = remove_emojis_except_first(challenge_data.get('challenge_name'))
            db.add_challenge(user_id, challenge_name)
            mh.update_system_role(user_id, roles.AfterContent)
            return after_content(user_id)

        lesson_data = try_get_object(fns.Lesson, response_message)
        if lesson_data:
            lesson_emoji = extract_single_emoji(lesson_data.get('lesson_emoji'))
            if lesson_emoji:
                lesson_name = remove_emojis_except_first(lesson_emoji + lesson_data.get('lesson_name'))
            else:
                lesson_name = remove_emojis_except_first(lesson_data.get('lesson_name'))
            lesson_id = db.add_lesson(user_id, lesson_name)
            db.add_action(user_id, "Continue...")
            mh.update_system_role(user_id, roles.LessonCreate, lesson_id)
            return lesson_create(user_id, lesson_id, lesson_name)
            
    print("ERROR: failed function!! defaulting to no functions...")
    response = generate_response(user_id, messages)
    identify_content(user_id, response["choices"][0]["message"]['content'])
    return response, None

def after_content(user_id):
    return generate_response(user_id, mh.prepare_session_messages(user_id)), None

def challenge_progress(user_id, challenge_id):
    messages = mh.prepare_session_messages(user_id, challenge_id=challenge_id)
    functions = [fns.ChallengeCompletion]
    function_call = "auto"

    for attempt in range(function_max_retries):
        response = generate_response(user_id, messages, functions, function_call)
        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            completion = try_get_object(fns.ChallengeCompletion, response_message)
            if completion:
                if completion.get('completion') == True:
                    db.update_challenge(user_id, challenge_id)
                    db.add_completion_message(user_id, challenge_id=challenge_id)
                    mh.update_system_role(user_id, roles.AfterContent)
                    return None
                else:
                    print("failed completion- respond without completion function")
                    return generate_response(user_id, messages)
        else:
            print("no completion - word response")
            return response
    print("incorrect challenge completion function use, defaulting to no function") 
    return generate_response(user_id, messages)

def lesson_create(user_id, lesson_id, lesson_name = None):
    if not lesson_name:
        lesson_name = db.get_user_lesson_name(user_id, lesson_id)
    profile = db.get_profile(user_id)
    ##### TODO: generate improved tutor #####
    if not db.get_tutor(user_id):
        tutor_create_message = mh.create_message(mh.system_message(user_id, roles.TutorCreate), profile)
        # TODO: model=GPT4 for paid users
        response = generate_response(user_id, tutor_create_message, tokens=LESSON_TOKENS)
        db.set_tutor(user_id, response['choices'][0]['message']['content'])

    lesson_msgs = mh.prepare_session_messages(user_id, limit=2)+mh.prepare_session_messages(user_id, lesson_id)+mh.user_message("Lesson topic: "+lesson_name)
    return generate_response(user_id, lesson_msgs, tokens=LESSON_TOKENS), lesson_id # TODO: for paid model=GPT4

def lesson_guide(user_id, lesson_id):
    messages = mh.prepare_session_messages(user_id, lesson_id) 
    functions = [fns.LessonToQuiz]
    function_call = "auto"

    response = generate_response(user_id, messages, functions, function_call)
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        mh.update_system_role(user_id, roles.QuizCreate, lesson_id)
        return quiz_create(user_id, lesson_id)
    return response, lesson_id

def quiz_create(user_id, lesson_id):
    messages = mh.prepare_quiz_messages(user_id, lesson_id) 
    function = [fns.CreateQuiz]
    function_call = {"name": function[0]['name']}

    for attempt in range(function_max_retries):
        response = generate_response(user_id, messages, function, function_call)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            continue
        
        quiz_data = extract_valid_quiz_questions(response_message)
        if quiz_data:
            return mh.quiz_to_message(quiz_data), lesson_id

    # Couldn't create json quiz, default wildquiz
    return generate_response(user_id, messages), lesson_id

def quiz_feedback(user_id, lesson_id):
    answer_msg = db.get_latest_message_by_role(user_id, "user")

    print(answer_msg)
    if "Score:" in answer_msg and "Answers:" in answer_msg:
        print("scored")
    else:
        print("Error: no quiz score.")
        return None, lesson_id
    
    parts = answer_msg.split(" | ")
    score_part = parts[0]  # "Score: [score]%"
    answers_part = parts[1]  # "Answers: [answers]"

    score = score_part.split(": ")[1]
    answer_msg = answers_part.split(": ")[1]
    if score == "100%":
        db.remove_score_from_answer(user_id, answer_msg)
        db.complete_quiz_message(user_id, lesson_id, score)
        db.update_lesson(user_id, lesson_id, datetime.utcnow())
        db.add_completion_message(user_id, lesson_id=lesson_id)
        return None, lesson_id
        
    messages = mh.prepare_session_messages(user_id, lesson_id) 
    response = generate_response(user_id, messages)
    db.remove_score_from_answer(user_id, answer_msg)
    db.complete_quiz_message(user_id, lesson_id, score)
    return response, lesson_id

#### private ####

def try_get_object(fcn, response_message):
    if response_message["function_call"]["name"] == fcn['name']:
        profile_args = json.loads(response_message["function_call"]["arguments"])
        
        # Extract required keys from the function definition
        required_keys = fcn['parameters']['required']

        # Check if all required keys are present and have non-empty values
        all_required_present = all(key in profile_args and (profile_args[key] is not None and (profile_args[key] or profile_args[key] == 0)) for key in required_keys)

        if all_required_present:
            # Extract all keys (both required and optional) for parameters
            all_keys = list(fcn['parameters']['properties'].keys())

            # Filter profile arguments to only include valid keys
            return {k: profile_args.get(k) for k in all_keys if profile_args.get(k) is not None}
        else:
            return None

    return None

def extract_valid_quiz_questions(quiz_response):
    try:
        quiz_data = json.loads(quiz_response["function_call"]["arguments"])
        valid_questions = {}
        valid_count = 0

        # Validate and add each question if valid
        for i in range(1, 6):
            question_key = f"question_{i}"
            
            # Check if the question object exists and is a dictionary
            if question_key in quiz_data and isinstance(quiz_data[question_key], dict):
                question = quiz_data[question_key]

                if i <= 3:  # For the first three questions
                    required_props = ["text", "correct_choice", "wrong_choices"]
                    if all(prop in question and question[prop] for prop in required_props) and \
                       isinstance(question["wrong_choices"], list) and len(question["wrong_choices"]) == 3:
                        valid_questions[question_key] = question
                        valid_count += 1
                else:  # For the last two questions
                    required_props = ["text", "answer"]
                    if all(prop in question and question[prop] is not None for prop in required_props) and \
                       isinstance(question["answer"], bool):
                        valid_questions[question_key] = question
                        valid_count += 1

        return valid_questions if valid_count >= 3 else None
    except (json.JSONDecodeError, KeyError):
        return None
    
def identify_content(user_id, message):
    system_msg = mh.system_message(user_id, roles.IdentifyContent)
    messages = mh.create_message(system_msg, message)
    function = [fns.Content]
    function_call = {"name": function[0]['name']}

    response = generate_response(user_id, messages, function, function_call)
    response_message = response["choices"][0]["message"]
    if not response_message.get("function_call"):
        print("No content suggested...")
        return

    content_data = try_get_object(fns.Content, response_message)
    if content_data:
        lesson_descriptions = content_data.get("lesson_descriptions", [])
        challenge_descriptions = content_data.get("challenge_descriptions", [])

        for lesson_obj in lesson_descriptions:
            lesson_text = remove_emojis(lesson_obj.get("lesson_name", "")).strip()
            lesson_emoji = lesson_obj.get("lesson_emoji", "")
            print(lesson_emoji)
            if lesson_emoji == "\",": # so many hax please help
                lesson_emoji = "🤔"
            lesson_name = remove_emojis_except_first(lesson_emoji+lesson_text)
            action_text = f"Start lesson: {lesson_name}"
            db.add_action(user_id, action_text)

        for challenge_obj in challenge_descriptions:
            challenge_text = remove_emojis(challenge_obj.get("challenge_name", "")).strip()
            challenge_emoji = challenge_obj.get("challenge_emoji", "")
            print(challenge_emoji)
            if challenge_emoji == "\",":
                challenge_emoji = "⛰️"
            challenge_name = remove_emojis_except_first(challenge_emoji+challenge_text)
            action_text = f"Accept challenge: {challenge_name}"
            db.add_action(user_id, action_text)
