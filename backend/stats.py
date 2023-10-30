from datetime import datetime, timedelta
from models import db, Challenge, Lesson
from sqlalchemy import func, extract
from collections import defaultdict

def get_pie_chart_data(user_id):
    lessons_by_topic = db.session.query(
        func.substr(Lesson.lesson_name, 1, 1).label('emoji'),
        func.count(Lesson.id).label('count')
    ).filter_by(user_id=user_id).group_by(
        func.substr(Lesson.lesson_name, 1, 1)
    ).all()

    challenges_by_topic = db.session.query(
        func.substr(Challenge.challenge_name, 1, 1).label('emoji'),
        func.count(Challenge.id).label('count')
    ).filter_by(user_id=user_id).group_by(
        func.substr(Challenge.challenge_name, 1, 1)
    ).all()

    topic_counts = defaultdict(int)
    for item in lessons_by_topic + challenges_by_topic:
        topic_counts[item.emoji] += item.count

    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
    top_5_topics = sorted_topics[:5]
    other_count = sum([count for _, count in sorted_topics[5:]])
    
    if other_count > 0:
        top_5_topics.append(('Others', other_count))

    labels = [emoji for emoji, _ in top_5_topics]
    data_values = [count for _, count in top_5_topics]
    backgroundColors = ['#b284e0', '#84e0c1','#d8c58c','#9384e0', '#84e0b2', '#84b2e0']

    pie_chart_data = {
        'labels': labels,
        'datasets': [{
            'label': '',
            'data': data_values,
            'backgroundColor': backgroundColors[:len(data_values)],
            'hoverOffset': 4
        }]
    }

    return pie_chart_data

def get_line_graph_data(user_id):
    lessons_over_time = db.session.query(
        extract('day', Lesson.completion_date),
        extract('month', Lesson.completion_date),
        extract('year', Lesson.completion_date),
        func.count(Lesson.id).label('lessons_count')
    ).filter_by(user_id=user_id).group_by(
        extract('day', Lesson.completion_date),
        extract('month', Lesson.completion_date),
        extract('year', Lesson.completion_date)
    ).all()

    challenges_over_time = db.session.query(
        extract('day', Challenge.completion_date),
        extract('month', Challenge.completion_date),
        extract('year', Challenge.completion_date),
        func.count(Challenge.id).label('challenges_count')
    ).filter_by(user_id=user_id).group_by(
        extract('day', Challenge.completion_date),
        extract('month', Challenge.completion_date),
        extract('year', Challenge.completion_date)
    ).all()
    
    merged_data = defaultdict(lambda: {"lessons": 0, "challenges": 0})

    for day, month, year, count in lessons_over_time:
        if day is None or month is None or year is None:
            continue
        date_key = f"{year}-{month:02}-{day:02}"
        merged_data[date_key]["lessons"] = count

    for day, month, year, count in challenges_over_time:
        if day is None or month is None or year is None:
            continue
        date_key = f"{year}-{month:02}-{day:02}"
        merged_data[date_key]["challenges"] = count


    data = [{"date": key, "lessons": value["lessons"], "challenges": value["challenges"]} for key, value in merged_data.items()]
    data = sorted(data, key=lambda x: x["date"])
    dates = [item['date'] for item in data]
    lessons = [item['lessons'] for item in data]
    challenges = [item['challenges'] for item in data]

    return {
        "labels": dates,
        "backgroundColor": '#84b2e0',
        "datasets": [{
            "label": "Lessons",
            "data": lessons,
            "backgroundColor": '#84b2e0',
            "borderColor": '#84b2e0',
        }, {
            "label": "Challenges",
            "data": challenges,
            'backgroundColor':'#84e0b2',
            "borderColor": '#84e0b2',
        }]
    }

def get_top_topics(user_id):
    pie_data = get_pie_chart_data(user_id)
    combined_data = list(zip(pie_data['labels'], pie_data['datasets'][0]['data']))
    sorted_combined_data = sorted(combined_data, key=lambda x: x[1], reverse=True)[:5]
    return {label: value for label, value in sorted_combined_data}

def get_active_and_completed(user_id, total_lessons, total_challenges):
    active_lessons = db.session.query(func.count(Lesson.id)).filter_by(user_id=user_id, completion_date=None).scalar()
    completed_lessons = total_lessons - active_lessons

    active_challenges = db.session.query(func.count(Challenge.id)).filter_by(user_id=user_id, completion_date=None).scalar()
    completed_challenges = total_challenges - active_challenges

    return active_lessons, completed_lessons, active_challenges, completed_challenges

def get_percent_completed(completed_lessons, total_lessons, completed_challenges, total_challenges):
    percent_completed_lessons = (completed_lessons / total_lessons) * 100 if total_lessons else 0
    percent_completed_challenges = (completed_challenges / total_challenges) * 100 if total_challenges else 0

    return percent_completed_lessons, percent_completed_challenges

def get_content_per_day(user_id):
    lessons_per_day = db.session.query(Lesson.completion_date, func.count(Lesson.id)).filter_by(user_id=user_id).group_by(Lesson.completion_date).all()
    challenges_per_day = db.session.query(Challenge.completion_date, func.count(Challenge.id)).filter_by(user_id=user_id).group_by(Challenge.completion_date).all()

    return dict(lessons_per_day), dict(challenges_per_day)

def get_streak(lessons_per_day, challenges_per_day):
    streak = 0
    current_streak = 0
    today = datetime.now().date()
    last_date = today

    lessons_dates = {k: v for k, v in lessons_per_day.items() if k is not None}
    challenges_dates = {k: v for k, v in challenges_per_day.items() if k is not None}

    combined_dates = sorted(set(lessons_dates) | set(challenges_dates))

    for date in combined_dates:
        if date == last_date - timedelta(days=1):
            current_streak += 1
        else:
            if date != today:
                current_streak = 1
        streak = max(streak, current_streak)
        last_date = date

    return streak, current_streak

def get_stats(user_id):
    total_lessons = db.session.query(func.count(Lesson.id)).filter_by(user_id=user_id).scalar()
    total_challenges = db.session.query(func.count(Challenge.id)).filter_by(user_id=user_id).scalar()

    top_topics = get_top_topics(user_id)
    
    active_lessons, completed_lessons, active_challenges, completed_challenges = get_active_and_completed(user_id, total_lessons, total_challenges)
    percent_completed_lessons, percent_completed_challenges = get_percent_completed(completed_lessons, total_lessons, completed_challenges, total_challenges)
    lessons_per_day, challenges_per_day = get_content_per_day(user_id)
    max_streak, current_streak = get_streak(lessons_per_day, challenges_per_day)

    data = {
        "totalCompleted": completed_lessons + completed_challenges,
        "totalLessons": total_lessons,
        "activeLessons": active_lessons,
        "completedLessons": completed_lessons,
        "totalChallenges": total_challenges,
        "activeChallenges": active_challenges,
        "completedChallenges": completed_challenges,
        "percentCompletedLessons": percent_completed_lessons,
        "percentCompletedChallenges": percent_completed_challenges,
        "lessonsPerDay": lessons_per_day,
        "challengesPerDay": challenges_per_day,
        "maxStreak": max_streak,
        "currentStreak": current_streak,
        "topTopics": top_topics,
    }

    return data