from datetime import datetime
import random
from flask import jsonify
from database.models import (
    db,
    User,
    Library,
    LibraryFactoid,
    LibraryQuestion,
    LibraryRoomState,
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


def initialize_room_states(user_id, library_id, commit=False):
    library = Library.query.get(library_id)
    if not library:
        return None

    room_names = library.room_names
    center_index = len(room_names) // 2

    room_states = []
    for index, room_name in enumerate(room_names):
        state = 0  # Default locked
        if index == center_index:
            state = 1

        # Initialize the current question index randomly between 0 and 3
        current_question_index = random.randint(0, 3)

        if commit:
            room_state = LibraryRoomState(
                user_id=user_id,
                library_id=library_id,
                room_name=room_name,
                state=state,
                current_question_index=current_question_index,
                answered_questions=[],  # Initialize with empty list
            )
            db.session.add(room_state)
        room_states.append(
            {
                "room_name": room_name,
                "state": state,
                "current_question_index": current_question_index,
                "answered_questions": [],
            }
        )

    if commit:
        db.session.commit()

    return room_states


def update_library_room_state(
    user_id,
    library_id,
    room_name,
    new_state,
    answered_questions,
    current_question_index,
):
    try:
        room_state = LibraryRoomState.query.filter_by(
            user_id=user_id, library_id=library_id, room_name=room_name
        ).first()
        if not room_state:
            return jsonify({"message": "Room state not found"}), 404

        room_state.state = new_state
        room_state.answered_questions = answered_questions
        room_state.current_question_index = current_question_index
        db.session.add(room_state)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Room state updated successfully",
                    "room_state": room_state.as_dict(),
                }
            ),
            200,
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

    library_data = library.as_dict()

    room_states = LibraryRoomState.query.filter_by(
        library_id=library_id, user_id=user_id
    ).all()
    if room_states:
        room_states = [room.as_dict() for room in room_states]
    else:
        room_states = initialize_room_states(user_id, library_id, commit=bool(user_id))
        if not room_states:
            return jsonify({"message": "Error initializing room states"}), 500

    library_data["room_states"] = {
        i: {
            "room_name": room["room_name"],
            "state": room["state"],
            "current_question_index": room.get("current_question_index", 0),
            "answered_questions": room.get("answered_questions", []),
        }
        for i, room in enumerate(room_states)
    }

    if user_id:
        existing_completion = LibraryCompletion.query.filter_by(library_id=library_id, user_id=user_id).first()
        if existing_completion:
            library_data["score"] = existing_completion.score

    print(library_data)
    return jsonify(library_data)


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


def mark_current_question_as_answered(user_id, library_id, room_name):
    room_state = LibraryRoomState.query.filter_by(
        user_id=user_id, library_id=library_id, room_name=room_name
    ).first()
    if room_state:
        if room_state.current_question_index not in room_state.answered_questions:
            room_state.answered_questions.append(room_state.current_question_index)
            db.session.commit()


def increment_current_question(user_id, library_id, room_name):
    room_state = LibraryRoomState.query.filter_by(
        user_id=user_id, library_id=library_id, room_name=room_name
    ).first()
    if room_state:
        room_state.current_question_index = (room_state.current_question_index + 1) % 4
        db.session.commit()


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
    content = {factoid.room_name: factoid.factoid_content for factoid in factoids}
    return jsonify({"library_content": content}).json["library_content"], 200

def get_library_settings(library_id):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404
    return library.difficulty, library.language, library.language_difficulty, library.context

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
            if is_complete:
                existing_completion.is_complete = is_complete
            if score > existing_completion.score:
                existing_completion.score = score
                user.experience_points += (score - existing_completion.score)
            else:
                return jsonify({'status': 'success', 'message': 'Existing score higher, no update performed'}), 200
        else:
            completion = LibraryCompletion(library_id=library_id, user_id=user_id, score=score, is_complete=is_complete)
            db.session.add(completion)
            user.experience_points += score

        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Game ended and recorded successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500



# Utility function to convert a model instance to a dictionary
def model_to_dict(model_instance):
    return {
        c.name: getattr(model_instance, c.name)
        for c in model_instance.__table__.columns
    }


# Adding as_dict methods to models
Library.as_dict = lambda self: model_to_dict(self)
LibraryFactoid.as_dict = lambda self: model_to_dict(self)
LibraryQuestion.as_dict = lambda self: model_to_dict(self)
LibraryRoomState.as_dict = lambda self: model_to_dict(self)
LibraryQuestionChoice.as_dict = lambda self: model_to_dict(self)
