from datetime import datetime
from flask import jsonify
from database.models import db, Library, LibraryFactoid, LibraryQuestion, UserLibraryQuestionAnswer, LibraryRoomState

def create_library(user_id, library_topic, room_names):
    try:
        library = Library(user_id=user_id, library_topic=library_topic, room_names=room_names)
        db.session.add(library)
        db.session.commit()
        return jsonify({"message": "Library created successfully", "library_id": library.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

def initialize_room_states(user_id, library_id, commit=False):
    library = Library.query.get(library_id)
    if not library:
        return None

    room_names = library.room_names
    matrix_size = int(len(room_names) ** 0.5)
    center_index = len(room_names) // 2
    center_x, center_y = center_index % matrix_size, center_index // matrix_size

    room_states = []
    for index, room_name in enumerate(room_names):
        i, j = index % matrix_size, index // matrix_size
        state = 0  # Default locked
        if index == center_index:
            state = 2  # Opened
        elif abs(i - center_x) + abs(j - center_y) <= 1 :
            state = 1  # Unlocked

        if commit:
            room_state = LibraryRoomState(user_id=user_id, library_id=library_id, room_name=room_name, state=state)
            db.session.add(room_state)
        room_states.append({'room_name': room_name, 'state': state})

    if commit:
        db.session.commit()
    
    return room_states

def get_library(library_id, user_id=None):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404

    library_data = library.as_dict()
    
    room_states = LibraryRoomState.query.filter_by(library_id=library_id, user_id=user_id).all()
    if room_states:
        room_states = [room.as_dict() for room in room_states]
    else:
        room_states = initialize_room_states(user_id, library_id, commit=bool(user_id))
        if not room_states:
            return jsonify({"message": "Error initializing room states"}), 500
        
    library_data['room_states'] = {room['room_name']: room['state'] for room in room_states}
    return jsonify(library_data)


def add_factoid_to_library(library_id, room_name, factoid_content):
    try:
        factoid = LibraryFactoid(library_id=library_id, room_name=room_name, factoid_content=factoid_content)
        db.session.add(factoid)
        db.session.commit()
        return jsonify({"message": "Factoid added successfully", "factoid_id": factoid.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

def add_question_to_factoid(factoid_id, question_text):
    try:
        question = LibraryQuestion(factoid_id=factoid_id, question_text=question_text)
        db.session.add(question)
        db.session.commit()
        return jsonify({"message": "Question added successfully", "question_id": question.id}), 201
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

def answer_question(user_id, question_id, answered=True):
    try:
        answer = UserLibraryQuestionAnswer.query.filter_by(user_id=user_id, question_id=question_id).first()
        if not answer:
            answer = UserLibraryQuestionAnswer(user_id=user_id, question_id=question_id, answered=answered)
        else:
            answer.answered = answered
            answer.answered_at = datetime.utcnow() if answered else None
        db.session.add(answer)
        db.session.commit()
        return jsonify({"message": "Answer status updated successfully", "answer_id": answer.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

def get_user_answers(user_id):
    answers = UserLibraryQuestionAnswer.query.filter_by(user_id=user_id).all()
    return jsonify([answer.as_dict() for answer in answers])

def get_user_answer_for_question(user_id, question_id):
    answer = UserLibraryQuestionAnswer.query.filter_by(user_id=user_id, question_id=question_id).first()
    if answer:
        return jsonify(answer.as_dict())
    else:
        return jsonify({"message": "Answer not found"}), 404



# Utility function to convert a model instance to a dictionary
def model_to_dict(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}

# Adding as_dict methods to models
Library.as_dict = lambda self: model_to_dict(self)
LibraryFactoid.as_dict = lambda self: model_to_dict(self)
LibraryQuestion.as_dict = lambda self: model_to_dict(self)
UserLibraryQuestionAnswer.as_dict = lambda self: model_to_dict(self)
LibraryRoomState.as_dict = lambda self: model_to_dict(self)
