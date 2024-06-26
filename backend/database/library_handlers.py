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

def visit_library(user_id, library_id):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404

    # Initialize room states with the center open and adjacent rooms unlocked
    room_names = library.room_names  # Assume this is a 5x5 matrix
    center_x, center_y = len(room_names) // 2, len(room_names[0]) // 2  # Calculate center
    for i in range(len(room_names)):
        for j in range(len(room_names[i])):
            state = 0  # Default locked
            if (i == center_x and j == center_y):
                state = 2  # Opened
            elif (abs(i - center_x) <= 1 and abs(j - center_y) <= 1):
                state = 1  # Unlocked
            room_state = LibraryRoomState(user_id=user_id, library_id=library_id, room_name=room_names[i][j], state=state)
            db.session.add(room_state)
    db.session.commit()

    return get_library(library_id, user_id)

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

def get_library(library_id, user_id=None):
    library = Library.query.get(library_id)
    if not library:
        return jsonify({"message": "Library not found"}), 404

    library_data = library.as_dict()

    if user_id:
        room_states = LibraryRoomState.query.filter_by(library_id=library_id, user_id=user_id).all()
        if not room_states:
            visit_library(user_id, library_id)
            room_states = LibraryRoomState.query.filter_by(library_id=library_id, user_id=user_id).all()
        library_data['room_states'] = {room.room_name: room.state for room in room_states}
    else:
        room_names = library.room_names  # Assuming a flat list of 25 room names
        matrix_size = int(len(room_names) ** 0.5)  # Assume square matrix, calculate size (e.g., 5 for 25 rooms)
        center_index = len(room_names) // 2  # Find the center index (e.g., 12 for 25 rooms)
        center_x, center_y = center_index % matrix_size, center_index // matrix_size
        
        room_states = []
        for index, room_name in enumerate(room_names):
            i, j = index % matrix_size, index // matrix_size
            state = 0  # Default locked
            if index == center_index:
                state = 2  # Opened
            elif abs(i - center_x) <= 1 and abs(j - center_y) <= 1:
                state = 1  # Unlocked
            room_states.append({'room_name': room_name, 'state': state})

        library_data['room_states'] = {room['room_name']: room['state'] for room in room_states}

    return jsonify(library_data)


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
