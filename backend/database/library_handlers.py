from datetime import datetime
from flask import jsonify
from database.models import (
    db,
    User,
    Library,
    LibraryFactoid,
    LibraryQuestion,
    LibraryQuestionChoice,
    LibraryCompletion
)


def create_library(
    user_id, library_topic, room_names, difficulty, language, language_difficulty
):
    try:
        library = Library(
            user_id=user_id,
            library_topic=library_topic,
            room_names=room_names,
            difficulty=difficulty,
            language=language,
            language_difficulty=language_difficulty,
        )
        db.session.add(library)
        db.session.commit()
        return (
            jsonify(
                {"message": "Library created successfully", "library_id": library.id}
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

def get_library_id(library_topic, difficulty, language, language_difficulty):
    try:
        library = Library.query.filter_by(
            library_topic=library_topic,
            difficulty=difficulty,
            language=language,
            language_difficulty=language_difficulty,
        ).first()

        if not library:
            return None

        return library.id

    except Exception as e:
        print(f"Error fetching library: {str(e)}")
        return None


def get_library(library_id, user_id=None):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404

    library.clicks += 1
    db.session.commit()

    library_data = library.as_dict()
    library_data["tutorial"] = True #default
    if user_id:
        existing_completion = LibraryCompletion.query.filter_by(library_id=library_id, user_id=user_id).first()
        if existing_completion:
            library_data["score"] = existing_completion.score

        any_completion = LibraryCompletion.query.filter_by(user_id=user_id, is_complete=True).first()
        print(any_completion)
        if any_completion:
            library_data["tutorial"] = False

    library_data["clicks"] = library.clicks
    return jsonify(library_data)

def get_library_details(library_id):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404

        # Fetch required details
        details = {
            'topic': library.library_topic,
            'guide': library.guide,
            'difficulty': library.difficulty
        }
        return jsonify(details), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_library_room_contents(library_id, room_name, factoids):
    responses = []
    for item in factoids["factoids"]:
        factoid_content = item["factoid_text"]
        question_data = item["question"]

        # Add factoid to library
        factoid_response, status_code = add_factoid_to_library(
            library_id, room_name, factoid_content
        )
        if status_code != 201:
            return factoid_response
        factoid_id = factoid_response.json["factoid_id"]

        # Add question to factoid
        question_text = question_data["text"]
        correct_choice = question_data["correct_choice"]
        wrong_choices = question_data["wrong_choices"]
        question_response, status_code = add_question_to_factoid(
            factoid_id, question_text, correct_choice, wrong_choices
        )
        if status_code != 201:
            return question_response
        responses.append(
            {
                "factoid_response": factoid_response.json,
                "question_response": question_response.json,
            }
        )

    return jsonify(status="success", data=responses)


def retrieve_library_room_contents(library_id, room_name):
    factoids = LibraryFactoid.query.filter_by(
        library_id=library_id, room_name=room_name
    ).all()
    if len(factoids) < 4:
        return None

    room_contents = []
    for factoid in factoids:
        questions = []
        for question in factoid.questions:
            question_choices = question.choices.all() if question.choices else []
            wrong_choices = [
                choice.choice_text
                for choice in question_choices
                if not choice.is_correct
            ]
            correct_choice = next(
                (
                    choice.choice_text
                    for choice in question_choices
                    if choice.is_correct
                ),
                None,
            )
            questions.append(
                {
                    "question_text": question.question_text,
                    "correct_choice": correct_choice,
                    "wrong_choices": wrong_choices,
                }
            )
        room_contents.append(
            {"factoid_text": factoid.factoid_content, "questions": questions}
        )

    return {"room_name": room_name, "factoids": room_contents}


def add_factoid_to_library(library_id, room_name, factoid_content):
    try:
        factoid = LibraryFactoid(
            library_id=library_id, room_name=room_name, factoid_content=factoid_content
        )
        db.session.add(factoid)
        db.session.commit()
        return (
            jsonify(
                {"message": "Factoid added successfully", "factoid_id": factoid.id}
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400


def add_question_to_factoid(factoid_id, question_text, correct_choice, wrong_choices):
    try:
        question = LibraryQuestion(
            factoid_id=factoid_id,
            question_text=question_text,
            correct_choice=correct_choice,
        )
        db.session.add(question)
        db.session.flush()  # Flush to get the question_id before commit

        # Add choices to the question
        add_choices_to_question(question.id, correct_choice, wrong_choices)

        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Question and choices added successfully",
                    "question_id": question.id,
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400


def get_factoid(factoid_id):
    factoid = LibraryFactoid.query.get(factoid_id)
    if factoid:
        return jsonify(factoid.as_dict())
    else:
        return jsonify({"message": "Factoid not found"}), 404


def get_question(question_id):
    question = LibraryQuestion.query.get(question_id)
    if question:
        return jsonify(question.as_dict())
    else:
        return jsonify({"message": "Question not found"}), 404


def add_choices_to_question(question_id, correct_choice, wrong_choices):
    try:
        # Add correct choice
        correct = LibraryQuestionChoice(
            question_id=question_id, choice_text=correct_choice, is_correct=True
        )
        db.session.add(correct)

        # Add wrong choices
        for choice in wrong_choices:
            wrong = LibraryQuestionChoice(
                question_id=question_id, choice_text=choice, is_correct=False
            )
            db.session.add(wrong)

        db.session.commit()
        return jsonify({"message": "Choices added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

def get_library_room_names(library_id):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404
    return jsonify({"room_names": library.room_names}).json["room_names"], 200


def get_library_content(library_id):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404
    
    factoids = LibraryFactoid.query.filter_by(library_id=library_id).all()
    content_list = []
    
    for factoid in factoids:
        factoid_content = f"Factoid: {factoid.factoid_content}\n"
        questions = LibraryQuestion.query.filter_by(factoid_id=factoid.id).all()
        
        for question in questions:
            question_content = f"Question: {question.question_text}\n"
            factoid_content += question_content
        
        content_list.append(factoid_content)
    full_content = "\n".join(content_list)
    
    return jsonify({"library_content": full_content}), 200

def get_library_settings(library_id):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404
    return library.difficulty, library.language, library.language_difficulty, library.context

def get_library_topic(library_id):
    library = Library.query.get(library_id)
    return library.library_topic

def is_center_room(library_id, room_name):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404
    return room_name == library.library_topic

def update_game_end(user_id, library_id, score, is_complete):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        existing_completion = LibraryCompletion.query.filter_by(library_id=library_id, user_id=user_id).first()
        if existing_completion:
            if is_complete and not existing_completion.is_complete:
                existing_completion.is_complete = is_complete
                existing_completion.completion_date = datetime.utcnow()
            if score > existing_completion.score:
                existing_completion.score = score
                user.experience_points += (score - existing_completion.score)
        else:
            completion = LibraryCompletion(library_id=library_id, user_id=user_id, score=score, is_complete=is_complete)
            db.session.add(completion)
            user.experience_points += score

        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Game ended and recorded successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

def get_libraries_info(user_id=None):
    top_liked_libraries = Library.query.order_by(Library.likes.desc()).limit(40).all()
    latest_libraries = Library.query.order_by(Library.id.desc()).limit(40).all()

    top_liked_dicts = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in top_liked_libraries]
    latest_dicts = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in latest_libraries]

    response_data = {
        'most_liked': top_liked_dicts,
        'latest': latest_dicts
    }

    if user_id is not None:
        my_libraries = Library.query.filter_by(user_id=user_id).order_by(Library.id.desc()).limit(40).all()
        my_dicts = [model_to_dict(library, exclude=['room_names', 'factoids']) for library in my_libraries]
        response_data['mine'] = my_dicts

    return jsonify(response_data)

def like_library(library_id):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        
        library.likes += 1
        db.session.commit()
        return jsonify({'message': 'Like added successfully', 'likes': library.likes}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def has_default_image(library_id):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        
        has_default = library.image_url == Library.DEFAULT_IMAGE_URL
        return jsonify({'has_default_image': has_default}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_library_image(library_id, image_url):
    try:
        library = Library.query.get(library_id)
        if library is None:
            return jsonify({'error': 'Library not found'}), 404
        
        library.image_url = image_url
        db.session.commit()
        return jsonify({'message': 'Image updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# UTILSSSS 
        
# Utility function to convert a model instance to a dictionary
def model_to_dict(model_instance, exclude=None):
    exclude = exclude or []
    return {
        c.name: getattr(model_instance, c.name)
        for c in model_instance.__table__.columns
        if c.name not in exclude
    }

# Adding as_dict methods to models
Library.as_dict = lambda self: model_to_dict(self)
LibraryFactoid.as_dict = lambda self: model_to_dict(self)
LibraryQuestion.as_dict = lambda self: model_to_dict(self)
LibraryQuestionChoice.as_dict = lambda self: model_to_dict(self)
