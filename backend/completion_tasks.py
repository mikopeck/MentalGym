import json
from datetime import datetime

import functions as fns
import roles as roles
import db_handlers as db
import message_handler as mh

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
        function_call = {"name": function[0]['name']}

    for attempt in range(function_max_retries):
        response = generate_response(messages, function, function_call)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            return response, None
        
        profile_data = try_get_object(fns.Profile, response_message)
        if profile_data:
            db.set_profile(user_id, json.dumps(profile_data))
            mh.update_system_role(user_id, roles.SuggestContent)
            return suggest_content(user_id)
                 
    print("ERROR: failed function!! defaulting to no functions...")
    mh.update_system_role(user_id, roles.ProfileGather)
    return generate_response(messages), None

def suggest_content(user_id, set_challenge = True):
    messages = mh.prepare_session_messages(user_id)
    functions = [fns.Lesson]
    if set_challenge:
        functions += [fns.Challenge]
    function_call = "auto"

    for attempt in range(function_max_retries):
        response = generate_response(messages, functions, function_call)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            identify_content(user_id, response_message['content'])
            return response, None
        
        challenge_data = try_get_object(fns.Challenge, response_message)
        if challenge_data:
            challenge_name = challenge_data.get('challenge_emoji') + " " +challenge_data.get('challenge_name')
            print("adding challenge", challenge_name)
            db.add_challenge(user_id, challenge_name)
            return after_content(user_id)
        
        lesson_data = try_get_object(fns.Lesson, response_message)
        if lesson_data:
            lesson_name = lesson_data.get('lesson_emoji')+" " +lesson_data.get('lesson_name')
            print("adding lesson", lesson_name)
            lesson_id = db.add_lesson(user_id, lesson_name)
            db.add_action(user_id, "Continue...")
            return lesson_create(user_id, lesson_id, lesson_name)
            
    print("ERROR: failed function!! defaulting to no functions...")
    response = generate_response(messages)
    identify_content(user_id, response["choices"][0]["message"]['content'])
    return response, None

def after_content(user_id):
    mh.update_system_role(user_id, roles.AfterContent)
    return generate_response(mh.prepare_session_messages(user_id)), None

def challenge_progress(user_id, challenge_id):
    messages = mh.prepare_session_messages(user_id, challenge_id=challenge_id)
    functions = [fns.ChallengeCompletion]
    function_call = "auto"

    for attempt in range(function_max_retries):
        response = generate_response(messages, functions, function_call)
        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            completion = try_get_object(fns.ChallengeCompletion, response_message)
            if completion:
                if completion.get('completion') == True:
                    db.update_challenge(user_id, challenge_id)
                    db.add_completion_message(user_id, challenge_id=challenge_id)
                    mh.update_system_role(user_id, roles.SuggestContent)
                    return suggest_content(user_id, False), None
                else:
                    print("failed completion- respond without completion function")
                    return generate_response(messages)
        else:
            print("no completion - word response")
            return response
    print("incorrect challenge completion function use, defaulting to no function") 
    return generate_response(messages)

def lesson_create(user_id, lesson_id, lesson_name = None):
    if not lesson_name:
        lesson_name = db.get_user_lesson_name(user_id, lesson_id)
    profile = db.get_profile(user_id)
    ##### TODO: generate improved tutor #####
    if not db.get_tutor(user_id):
        tutor_create_message = mh.create_message(mh.system_message(user_id, roles.TutorCreate), profile)
        response = generate_response(tutor_create_message, model=GPT4, tokens=LESSON_TOKENS)
        db.set_tutor(user_id, response['choices'][0]['message']['content'])

    mh.update_system_role(user_id, roles.LessonCreate, lesson_id)
    return generate_response(mh.prepare_session_messages(user_id, lesson_id)+mh.user_message("Lesson topic: "+lesson_name), model=GPT4, tokens=LESSON_TOKENS), lesson_id

def lesson_guide(user_id, lesson_id):
    messages = mh.prepare_session_messages(user_id, lesson_id) 
    functions = [fns.LessonToQuiz]
    function_call = "auto"

    response = generate_response(messages, functions, function_call)
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        return quiz_create(user_id, lesson_id)
    return response, lesson_id

def quiz_create(user_id, lesson_id):
    return generate_response(mh.prepare_session_messages(user_id, lesson_id), model=GPT4), lesson_id

def quiz_feedback(user_id, lesson_id):
    mh.update_system_role(user_id, roles.QuizGrade, lesson_id)
    messages = mh.prepare_session_messages(user_id, lesson_id) 
    function = [fns.Grade]
    function_call = {"name": function[0]['name']}

    for attempt in range(function_max_retries):
        response = generate_response(messages, function, function_call)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            continue
        
        grade_data = try_get_object(fns.Grade, response_message)
        if grade_data:
            score = grade_data.get("score")
            if score > passing_grade:
                print("lesson success")
                db.update_lesson(user_id, lesson_id, datetime.utcnow())
                db.add_completion_message(user_id, lesson_id=lesson_id)
                return None, lesson_id
            else:
                print("quiz failed")
                mh.update_system_role(user_id, roles.QuizFeedback, lesson_id)
                return generate_response(messages), lesson_id
                    
    print("ERROR: failed grading function!! defaulting to quiz create again...")
    mh.update_system_role(user_id, roles.QuizCreate, lesson_id)
    return quiz_create(user_id, lesson_id)

#### private ####

def try_get_object(fcn: fns,response_message):
    if response_message["function_call"]["name"] == fcn['name']:
        profile_args = json.loads(response_message["function_call"]["arguments"])
        
        # Extract keys for parameters
        keys = list(fcn['parameters']['properties'].keys())
        
        # Filter profile arguments to only include valid keys
        return {k: profile_args.get(k) for k in keys if profile_args.get(k) is not None}
    
def identify_content(user_id, message):
    system_msg = mh.system_message(user_id, roles.IdentifyContent)
    messages = mh.create_message(system_msg, message)
    function = [fns.Content]
    function_call = {"name": function[0]['name']}

    response = generate_response(messages, function, function_call)
    response_message = response["choices"][0]["message"]
    if not response_message.get("function_call"):
        print("No content suggested...")
        return

    content_data = try_get_object(fns.Content, response_message)
    if content_data:
        lessons = content_data.get("lesson_names", [])
        challenges = content_data.get("challenge_names", [])
        for lesson in lessons:
            db.add_action(user_id, "Start lesson: " + lesson)
        for challenge in challenges:
            db.add_action(user_id, "Accept challenge: " + challenge)
