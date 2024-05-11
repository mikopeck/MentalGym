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
        
        profile_data = fns.try_get_object(fns.Profile, response_message)
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
    function_call = "auto"

    for attempt in range(function_max_retries):
        response = generate_response(user_id, messages, functions, function_call)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            identify_content(user_id, response_message['content'])
            return response, None

        lesson_data = fns.try_get_object(fns.Lesson, response_message)
        if lesson_data:
            lesson_emoji = extract_single_emoji(lesson_data.get('lesson_emoji'))
            if lesson_emoji:
                lesson_name = remove_emojis_except_first(lesson_emoji + lesson_data.get('lesson_name'))
            else:
                lesson_name = remove_emojis_except_first(lesson_data.get('lesson_name'))
            created, lesson_id = db.add_lesson(user_id, lesson_name)
            if not created:
                return None, lesson_id
            db.add_action(user_id, "Continue...")
            mh.update_system_role(user_id, roles.LessonCreate, lesson_id)
            return lesson_create(user_id, lesson_id, lesson_name)
            
    print("ERROR: failed function!! defaulting to no functions...")
    response = generate_response(user_id, messages)
    identify_content(user_id, response["choices"][0]["message"]['content'])
    return response, None

def after_content(user_id):
    response = generate_response(user_id, mh.prepare_session_messages(user_id))
    return response, None

def lesson_create(user_id, lesson_id, lesson_name = None):
    if not lesson_name:
        lesson_name = db.get_lesson_name(lesson_id)
        #if lesson name already exists, navigate to that lesson
    profile = db.get_profile(user_id)
    ##### TODO: generate improved tutor #####
    if not db.get_tutor(user_id):
        tutor_create_message = mh.create_message(mh.system_message(user_id, roles.TutorCreate), profile)
        # TODO: model=GPT4 for paid users
        response = generate_response(user_id, tutor_create_message, tokens=LESSON_TOKENS)
        db.set_tutor(user_id, response['choices'][0]['message']['content'])

    lesson_msgs = mh.prepare_session_messages(user_id, lesson_id)+mh.user_message("Lesson topic: "+lesson_name)
    return generate_response(user_id, lesson_msgs, tokens=LESSON_TOKENS, model= GPT4), lesson_id # TODO: for paid model=GPT4

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
    messages = mh.prepare_session_messages(user_id, lesson_id) 
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
    
    try:
        data = json.loads(answer_msg)
        if 'score' in data and 'answers' in data:
            score = data['score']
            answers = data['answers']

            print("Score:", score)
            print("Answers:", answers)
        else:
            print("Error: Invalid data received.")
            return None, lesson_id
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON.")
        return None, lesson_id
    
    if score == 100:
        db.remove_score_from_answer(user_id, answer_msg)
        feedback_msg = json.dumps({"score": score, "answers": answers})
        db.complete_quiz_message(user_id, lesson_id, feedback_msg+" | ")
        db.update_lesson(user_id, lesson_id, datetime.utcnow())
        db.add_completion_message(user_id, lesson_id=lesson_id)
        return None, lesson_id
        
    messages = mh.prepare_session_messages(user_id, lesson_id) 
    response = generate_response(user_id, messages)
    db.remove_score_from_answer(user_id, answer_msg)
    feedback_msg = json.dumps({"score": score, "answers": answers})
    db.complete_quiz_message(user_id, lesson_id, feedback_msg+" | ")
    return response, lesson_id

#### private ####

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

    content_data = fns.try_get_object(fns.Content, response_message)
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
