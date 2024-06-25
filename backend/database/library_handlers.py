from datetime import datetime
from flask import jsonify
from database.models import db, Library, LibraryFactoid, LibraryQuestion, UserLibraryQuestionAnswer, LibraryDoor

def create_library(user_id, library_topic, room_names):
    try:
        library = Library(user_id=user_id, library_topic=library_topic, room_names=room_names)
        db.session.add(library)
        db.session.commit()
        return jsonify({"message": "Library created successfully", "library_id": library.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

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
    
    # Include door states if user_id is provided
    if user_id:
        doors = LibraryDoor.query.filter_by(library_id=library_id).all()
        library_data['doors'] = [{'room_name1': door.room_name1, 'room_name2': door.room_name2, 'state': door.state} for door in doors]
    print(library_data)
    
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

def get_specific_door(user_id, library_id, room_name1, room_name2):
    door = LibraryDoor.query.filter_by(
        user_id=user_id,
        library_id=library_id,
        room_name1=room_name1,
        room_name2=room_name2
    ).first()
    return door




# Utility function to convert a model instance to a dictionary
def model_to_dict(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}

# Adding as_dict methods to models
Library.as_dict = lambda self: model_to_dict(self)
LibraryFactoid.as_dict = lambda self: model_to_dict(self)
LibraryQuestion.as_dict = lambda self: model_to_dict(self)
UserLibraryQuestionAnswer.as_dict = lambda self: model_to_dict(self)
