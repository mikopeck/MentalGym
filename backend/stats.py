from models import db, Challenge, Lesson
from sqlalchemy import func, extract
from collections import defaultdict

def get_pie_chart_data(user_id):
    # Fetch lessons by topic
    lessons_by_topic = db.session.query(
        func.substr(Lesson.lesson_name, 1, 1).label('emoji'),
        func.count(Lesson.id).label('count')
    ).filter_by(user_id=user_id).group_by(
        func.substr(Lesson.lesson_name, 1, 1)
    ).all()

    # Fetch challenges by topic
    challenges_by_topic = db.session.query(
        func.substr(Challenge.challenge_name, 1, 1).label('emoji'),
        func.count(Challenge.id).label('count')
    ).filter_by(user_id=user_id).group_by(
        func.substr(Challenge.challenge_name, 1, 1)
    ).all()

    # Combine lesson and challenge counts by emoji
    topic_counts = defaultdict(int)
    for item in lessons_by_topic + challenges_by_topic:
        topic_counts[item.emoji] += item.count

    # Sort topics by count in descending order and take the top 5
    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
    top_5_topics = sorted_topics[:5]
    other_count = sum([count for _, count in sorted_topics[5:]])
    
    # If there are more than 5 topics, add the 6th "Others" category
    if other_count > 0:
        top_5_topics.append(('Others', other_count))

    labels = [emoji for emoji, _ in top_5_topics]
    data_values = [count for _, count in top_5_topics]
    backgroundColors = ['#FF6347', '#FFD700', '#32CD32', '#1E90FF', '#FF4500', '#C71585']

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
    return transform_to_chartjs_format(data)

def transform_to_chartjs_format(data):
    dates = [item['date'] for item in data]
    lessons = [item['lessons'] for item in data]
    challenges = [item['challenges'] for item in data]

    return {
        "labels": dates,
        "datasets": [{
            "label": "Lessons",
            "data": lessons
        }, {
            "label": "Challenges",
            "data": challenges
        }]
    }

from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta

def get_stats(user_id):
    # Previous stats
    total_lessons = db.session.query(func.count(Lesson.id)).filter_by(user_id=user_id).scalar()
    total_challenges = db.session.query(func.count(Challenge.id)).filter_by(user_id=user_id).scalar()
    pie_data = get_pie_chart_data(user_id)
    combined_data = list(zip(pie_data['labels'], pie_data['datasets'][0]['data']))
    sorted_combined_data = sorted(combined_data, key=lambda x: x[1], reverse=True)[:5]
    top_topics = {label: value for label, value in sorted_combined_data}

    # Active vs Completed
    active_lessons = db.session.query(func.count(Lesson.id)).filter_by(user_id=user_id, completion_date=None).scalar()
    completed_lessons = total_lessons - active_lessons

    active_challenges = db.session.query(func.count(Challenge.id)).filter_by(user_id=user_id, completion_date=None).scalar()
    completed_challenges = total_challenges - active_challenges

    # % Completed
    percent_completed_lessons = (completed_lessons / total_lessons) * 100 if total_lessons else 0
    percent_completed_challenges = (completed_challenges / total_challenges) * 100 if total_challenges else 0

    # Content Completed per Day
    lessons_per_day = db.session.query(Lesson.completion_date, func.count(Lesson.id)).filter_by(user_id=user_id).group_by(Lesson.completion_date).all()
    challenges_per_day = db.session.query(Challenge.completion_date, func.count(Challenge.id)).filter_by(user_id=user_id).group_by(Challenge.completion_date).all()

    # Streak Calculation
    streak = 0
    current_streak = 0
    today = datetime.now().date()
    last_date = today

    combined_dates = sorted(list(set([l[0] for l in lessons_per_day if l[0] is not None] + [c[0] for c in challenges_per_day if c[0] is not None])))
    for date in combined_dates:
        if date == last_date - timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1
        streak = max(streak, current_streak)
        last_date = date

    # Other stats
    total_unique_topics = len(pie_data['labels'])
    
    data = {
        "totalContent": total_lessons + total_challenges,
        "topTopics": top_topics,
        "totalLessons": total_lessons,
        "activeLessons": active_lessons,
        "completedLessons": completed_lessons,
        "totalChallenges": total_challenges,
        "activeChallenges": active_challenges,
        "completedChallenges": completed_challenges,
        "percentCompletedLessons": percent_completed_lessons,
        "percentCompletedChallenges": percent_completed_challenges,
        "lessonsPerDay": dict(lessons_per_day),
        "challengesPerDay": dict(challenges_per_day),
        "streak": streak,
        "totalUniqueTopics": total_unique_topics
    }

    return data
