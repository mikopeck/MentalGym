from datetime import datetime, timedelta
from sqlalchemy import func, extract
from database.models import db, LibraryCompletion, Lesson

def get_line_graph_data(user_id):
    # Query the database for lessons completed by day, month, and year
    lessons_over_time = db.session.query(
        extract('day', Lesson.completion_date).label('day'),
        extract('month', Lesson.completion_date).label('month'),
        extract('year', Lesson.completion_date).label('year'),
        func.count(Lesson.id).label('lessons_count')
    ).filter_by(user_id=user_id).group_by(
        extract('day', Lesson.completion_date),
        extract('month', Lesson.completion_date),
        extract('year', Lesson.completion_date)
    ).all()

    # Query the database for completed libraries with their scores
    libraries_over_time = db.session.query(
        extract('day', LibraryCompletion.completion_date).label('day'),
        extract('month', LibraryCompletion.completion_date).label('month'),
        extract('year', LibraryCompletion.completion_date).label('year'),
        func.sum(LibraryCompletion.score).label('total_score')
    ).filter_by(user_id=user_id, is_complete=True).group_by(
        extract('day', LibraryCompletion.completion_date),
        extract('month', LibraryCompletion.completion_date),
        extract('year', LibraryCompletion.completion_date)
    ).all()

    if not lessons_over_time and not libraries_over_time:
        return None
    
    # Initialize a dictionary to store data for each date
    merged_data = {}

    # Add lessons data to merged_data
    for day, month, year, lessons_count in lessons_over_time:
        if day is None or month is None or year is None:
            continue
        date_key = datetime(year, month, day)
        if date_key not in merged_data:
            merged_data[date_key] = {"exp": 0}
        merged_data[date_key]["exp"] += lessons_count * 100  # 100 EXP per lesson

    # Add library data to merged_data
    for day, month, year, total_score in libraries_over_time:
        if day is None or month is None or year is None:
            continue
        date_key = datetime(year, month, day)
        if date_key not in merged_data:
            merged_data[date_key] = {"exp": 0}
        merged_data[date_key]["exp"] += total_score  # Add score as EXP for completed libraries

    # Prepare the final dataset
    data = [{"date": key.strftime('%Y-%m-%d'), "exp": value["exp"]} for key, value in merged_data.items()]
    data = sorted(data, key=lambda x: x["date"])
    dates = [item['date'] for item in data]
    exp_values = [item['exp'] for item in data]
    cumulative_exp = [sum(exp_values[:i+1]) for i in range(len(exp_values))]

    return {
        "labels": dates,
        "backgroundColor": '#84b2e0',
        "datasets": [{
            "label": "Experience🌟",
            "data": cumulative_exp,
            "backgroundColor": '#84b2e0',
            "borderColor": '#84b2e0',
        }]
    }

def get_total_user_exp(user_id):
    total_lessons_exp = db.session.query(
        func.count(Lesson.id).label('lessons_count')
    ).filter_by(user_id=user_id).scalar() or 0

    # Each completed lesson counts as 100 EXP
    total_lessons_exp *= 100

    total_libraries_exp = db.session.query(
        func.sum(LibraryCompletion.score).label('total_score')
    ).filter_by(user_id=user_id, is_complete=True).scalar() or 0

    total_exp = total_lessons_exp + total_libraries_exp

    return total_exp

def get_active_and_completed(user_id, total_lessons, total_librarys):
    active_lessons = db.session.query(func.count(Lesson.id)).filter_by(user_id=user_id, completion_date=None).scalar()
    completed_lessons = total_lessons - active_lessons

    active_librarys = db.session.query(func.count(LibraryCompletion.id)).filter_by(user_id=user_id, is_complete=False).scalar()
    completed_librarys = total_librarys - active_librarys

    return active_lessons, completed_lessons, active_librarys, completed_librarys

def get_percent_completed(completed_lessons, total_lessons, completed_librarys, total_librarys):
    percent_completed_lessons = round((completed_lessons / total_lessons) * 100, 2) if total_lessons else 0
    percent_completed_librarys = round((completed_librarys / total_librarys) * 100, 2) if total_librarys else 0

    return percent_completed_lessons, percent_completed_librarys

def get_content_per_day(user_id):
    lessons_per_day = db.session.query(Lesson.completion_date, func.count(Lesson.id)).filter_by(user_id=user_id).group_by(Lesson.completion_date).all()
    librarys_per_day = db.session.query(LibraryCompletion.completion_date, func.count(LibraryCompletion.id)).filter_by(user_id=user_id, is_complete=True).group_by(LibraryCompletion.completion_date).all()

    return dict(lessons_per_day), dict(librarys_per_day)

def get_streak(user_id):
    max_streak = 0
    current_streak = 0
    today = datetime.now()
    last_date = today
    lessons_per_day, librarys_per_day = get_content_per_day(user_id)

    lessons_dates = {k: v for k, v in lessons_per_day.items() if k is not None}
    librarys_dates = {k: v for k, v in librarys_per_day.items() if k is not None}

    combined_dates = sorted(set(lessons_dates) | set(librarys_dates))

    for date in combined_dates:
        if date.date() == (last_date + timedelta(days=1)).date():
            current_streak += 1
        elif last_date.date() == date.date():
            continue
        else:
            current_streak = 1
        max_streak = max(max_streak, current_streak)
        last_date = date

    if last_date.date() != today.date():
        current_streak = 0

    return max_streak, current_streak

def get_stats(user_id):
    total_lessons = db.session.query(func.count(Lesson.id)).filter_by(user_id=user_id).scalar()
    total_librarys = db.session.query(func.count(LibraryCompletion.id)).filter_by(user_id=user_id).scalar()

    active_lessons, completed_lessons, active_librarys, completed_librarys = get_active_and_completed(user_id, total_lessons, total_librarys)
    percent_completed_lessons, percent_completed_librarys = get_percent_completed(completed_lessons, total_lessons, completed_librarys, total_librarys)
    max_streak, current_streak = get_streak(user_id)

    data = {
        "totalCompleted": completed_lessons + completed_librarys,
        "totalLessons": total_lessons,
        "activeLessons": active_lessons,
        "completedLessons": completed_lessons,
        "totalLibrarys": total_librarys,
        "activeLibrarys": active_librarys,
        "completedLibrarys": completed_librarys,
        "percentCompletedLessons": percent_completed_lessons,
        "percentCompletedLibrarys": percent_completed_librarys,
        "maxStreak": max_streak,
        "currentStreak": current_streak,
    }

    return data