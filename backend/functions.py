Profile = {
    "name": "create_profile",
    "description": "Create a profile for the user. Also use if the user would like to move on to learning or setting challenges.",
    "parameters": {
        "type": "object",
        "properties": {
# general
            "identity": {
                "type": "string",
                "description": "The users preferred names, nicknames, or the designation they feel most connected to.",
            },
            # "language": {
            #     "type": "string",
            #     "description": "The users preferred language - never ask for this, but assume from the language the user uses.",
            # },

# personal
            "prior_knowledge": {
                "type": "string",
                "description": "Prior knowledge and level. For example: Basic spanish, intermediate algebra, advanced geology.",
            },
            "interests": {
                "type": "string",
                "description": "Personal interests which can make learning more engaging if used to tailor examples and explanations.",
            },
            "motivation": {
                "type": "string",
                "description": "What motivates the user to set and attempt challenges and learn.",
            },

# learning
            "study_habits": {
                "type": "string",
                "description": "Any habits which help the user study like: highlighting and note-taking, review and preview, spaced repetition, Use of Analogies and real-world examples.",
            },
            "pacing": {
                "type": "string",
                "description": "Some may require a slower, more detailed explanation, while others prefer quick summaries.",
            },
            "feedback_style": {
                "type": "string",
                "description": "Type, frequency, and tone of feedback. Some students thrive on positive reinforcement, while others might need constructive criticism.",
            },
            "learning_goals": {
                "type": "string",
                "description": "The user's specific objectives or what they aim to achieve with the tutoring. For example: 'Pass the math exam', 'Become fluent in Spanish'."
            },
        },
        "required": []
    },
}

Lesson = {
    "name": "start_lesson",
    "description": "When a user wants to start a lesson being offered. The user must agree to an offer to start this lesson.",
    "parameters": {
        "type": "object",
        "properties": {
            "lesson_name": {
                "type": "string",
                "description": "A concise but complete description of the lesson to start.",
            },
            "lesson_emoji": {
                "type": "string",
                "description": "One emoji which represents the lesson topic.",
            },
        },
        "required": ["lesson_name","lesson_emoji"],
    },
}

Challenge = {
    "name": "accept_challenge",
    "description": "When a user wants to set a challenge for themselves. The user must agree to an offer to accept this challenge.",
    "parameters": {
        "type": "object",
        "properties": {
            "challenge_name": {
                "type": "string",
                "description": "A concise but complete description of the challenge.",
            },
            "challenge_emoji": {
                "type": "string",
                "description": "One emoji which represents the challenge topic.",
            }
        },
        "required": ["challenge_name", "challenge_emoji"],
    },
}

Content = {
    "name": "offered_content",
    "description": "Returns any lessons or challenges being offered.",
    "parameters": {
        "type": "object",
        "properties": {
            "lesson_names": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "One emoji and a concise but complete descriptions of the lessons offered.",
            },
            "challenge_names": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "One emoji and a concise but complete descriptions of the challenges offered.",
            },
        },
        "required": [],
    },
}


Grade = {
    "name": "grade_quiz",
    "description": "Give the user a score based on their answers to the quiz. A score of 0 would mean the user has answered every question incorrectly.",
    "parameters": {
        "type": "object",
        "properties": {
            "score": {
                "type": "integer",
                "description": "A score between 0 and 100 where 100 means all questions were answered correctly.",
                "minimum": 0,
                "maximum": 100
            }
        },
        "required": ["score"],
    },
}

ChallengeCompletion = {
    "name": "complete_challenge",
    "description": "Used when a user has completed the challenge.",
    "parameters": {
        "type": "object",
        "properties": {
            "completion": {
                "type": "boolean",
                "description": "Has the user really completed the challenge?"
            }
        },
        "required": ["completion"],
    },
}

LessonToQuiz = {
    "name": "lesson_to_quiz",
    "description": "Used when a user wants to continue to a quiz.",
    "parameters": {
        "type": "object",
        "properties": {
            "continue": {
                "type": "boolean",
                "description": "Does the user want to continue? Should always be true if this method is called."
            }
        },
        "required": ["continue"],
    },
}