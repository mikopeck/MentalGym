import json

Profile = {
    "name": "create_profile",
    "description": "Create a profile for the user. Also use if the user would like to move on to learning.",
    "parameters": {
        "type": "object",
        "properties": {
# general
            "identity": {
                "type": "string",
                "description": "The users preferred names, nicknames, or the designation they feel most connected to.",
            },
            "language": {
                "type": "string",
                "description": "The users preferred language - never ask for this, but assume from the language the user replies in.",
            },

# personal
            "education_level": {
                "type": "string",
                "description": "Prior knowledge and education. For example: Just started school, starting university next year , completed basic education __ years ago, pursuing a PhD in theoretical physics.",
            },

            "interests": {
                "type": "string",
                "description": "Personal interests which can make learning more engaging if used to tailor examples and explanations.",
            },
            # "motivation": {
            #     "type": "string",
            #     "description": "What motivates the user to set and attempt challenges and learn.",
            # },

# learning
            # "study_habits": {
            #     "type": "string",
            #     "description": "Any habits which help the user study like: highlighting and note-taking, review and preview, spaced repetition, Use of Analogies and real-world examples.",
            # },
            # "pacing": {
            #     "type": "string",
            #     "description": "Some may require a slower, more detailed explanation, while others prefer quick summaries.",
            # },
            # "feedback_style": {
            #     "type": "string",
            #     "description": "Type, frequency, and tone of feedback. Some students thrive on positive reinforcement, while others might need constructive criticism.",
            # },
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
    "description": "When a user wants to start a lesson being offered. The user must agree to an offer to start this specific lesson.",
    "parameters": {
        "type": "object",
        "properties": {
            "lesson_name": {
                "type": "string",
                "description": "A concise but complete description of the lesson to start. Up to 12 words.",
            },
            "lesson_emoji": {
                "type": "string",
                "description": "A single, valid Unicode emoji representing the lesson topic. Must be within standard Unicode emoji ranges.",
            },
        },
        "required": ["lesson_name","lesson_emoji"],
    },
}

Content = {
    "name": "offered_content",
    "description": "Returns descriptions and emojis for any lessons being offered.",
    "parameters": {
        "type": "object",
        "properties": {
            "lesson_descriptions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "lesson_name": {
                            "type": "string",
                            "description": "A concise but complete description of the lesson. Up to 12 words."
                        },
                        "lesson_emoji": {
                            "type": "string",
                            "description": "A single, valid Unicode emoji representing the lesson topic. Must be within standard Unicode emoji ranges."
                        }
                    },
                    "required": ["lesson_name", "lesson_emoji"]
                },
                "description": "An array of objects, each containing a name and an emoji representing the topic of the lessons offered."
            },
        },
        "required": [],
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

CreateQuiz = {
    "name": "create_quiz",
    "description": "Create a quiz with a set of questions. The first three questions will each have one correct choice and three wrong choices, followed by two true/false questions.",
    "parameters": {
        "type": "object",
        "properties": {
            "question_1": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text of the first question."
                    },
                    "correct_choice": {
                        "type": "string",
                        "description": "The correct choice for the first question."
                    },
                    "wrong_choices": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "The three wrong choices for the first question."
                    }
                },
                "required": ["text", "correct_choice", "wrong_choices"]
            },
            "question_2": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text of the second question."
                    },
                    "correct_choice": {
                        "type": "string",
                        "description": "The correct choice for the second question."
                    },
                    "wrong_choices": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "The three wrong choices for the second question."
                    }
                },
                "required": ["text", "correct_choice", "wrong_choices"]
            },
            "question_3": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text of the third question."
                    },
                    "correct_choice": {
                        "type": "string",
                        "description": "The correct choice for the third question."
                    },
                    "wrong_choices": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "minItems": 3,
                        "maxItems": 3,
                        "description": "The three wrong choices for the third question."
                    }
                },
                "required": ["text", "correct_choice", "wrong_choices"]
            },
            "question_4": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text of the fourth question, which is a true/false question."
                    },
                    "answer": {
                        "type": "boolean",
                        "description": "The correct answer to the fourth question. True for 'True', False for 'False'."
                    }
                },
                "required": ["text", "answer"]
            },
            "question_5": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text of the fifth question, which is a true/false question."
                    },
                    "answer": {
                        "type": "boolean",
                        "description": "The correct answer to the fifth question. True for 'True', False for 'False'."
                    }
                },
                "required": ["text", "answer"]
            },
        },
        "required": ["question_1", "question_2", "question_3", "question_4", "question_5"]
    },
}

ExploreTopic = {
    "name": "generate_lesson_suggestions",
    "description": "Generates three personalized lesson suggestions based on the user's profile and learning history.",
    "parameters": {
        "type": "object",
        "properties": {
            "lesson_suggestions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "lesson_name": {
                            "type": "string",
                            "description": "A concise but complete description of the lesson suggestion. Up to 12 words."
                        },
                        "lesson_emoji": {
                            "type": "string",
                            "description": "A single, valid Unicode emoji representing the lesson topic. Must be within standard Unicode emoji ranges."
                        }
                    },
                    "required": ["lesson_name", "lesson_emoji"]
                },
                "minItems": 3,
                "maxItems": 3,
                "description": "An array of three objects, each containing a name and an emoji representing the topic of the lesson suggestions."
            },
        },
        "required": ["lesson_suggestions"],
    },
}

GenerateLibraryRoomNames = {
    "name": "generate_library_archive_rooms",
    "description": "Generates the room names of a library archive for a given topic.",
    "parameters": {
        "type": "object",
        "properties": {
            "room_names": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "room_name": {
                            "type": "string",
                            "description": "A name for the library room which includes the subtopic description. Up to 12 words."
                        },
                    },
                    "required": ["room_name"]
                },
                "minItems": 24,
                "maxItems": 24,
                "description": "An array of twenty four room names."
            },
        },
        "required": ["room_names"],
    },
}

GenerateLibraryRoom = {
    "name": "generate_library_room",
    "description": "Generates a library room with 4 factoids and corresponding questions. Each factoid is an interesting snippet related to the room's theme. Two factoids have associated multiple-choice questions testing understanding of the factoid, and two factoids have a missing word denoted by an underscore for the user to fill in, each accompanied by multiple-choice options.",
    "parameters": {
        "type": "object",
        "properties": {
            "factoids": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "factoid_text": {
                            "type": "string",
                            "description": "A snippet of an interesting fact related to the library room's theme, up to 200 tokens in length."
                        },
                        "question": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": ["multiple_choice", "fill_in_the_blank"],
                                    "description": "The type of question: 'multiple_choice' or 'fill_in_the_blank'."
                                },
                                "text": {
                                    "type": "string",
                                    "description": "The text of the question. For 'fill_in_the_blank' questions, this must contain an underscore (_) where the answer should go."
                                },
                                "correct_choice": {
                                    "type": "string",
                                    "description": "The correct choice for the question or the correct word/phrase that fills in the blank."
                                },
                                "wrong_choices": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "minItems": 3,
                                    "maxItems": 3,
                                    "description": "Three incorrect choices for the question."
                                }
                            },
                            "required": ["type", "text", "correct_choice", "wrong_choices"]
                        }
                    },
                    "required": ["factoid_text", "question"]
                },
                "minItems": 4,
                "maxItems": 4,
                "description": "An array of four objects, each containing a factoid and its corresponding question."
            }
        },
        "required": ["factoids"]
    }
}


# GenerateLibraryRoom = {
#     "name": "generate_library_room",
#     "description": "Generates a library room with 4 factoids and corresponding multiple-choice questions. Each factoid is an interesting snippet related to the room's theme, and each question tests understanding of its associated factoid.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "factoids": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "factoid_text": {
#                             "type": "string",
#                             "description": "A snippet of an interesting fact related to the library room's theme, up to 200 tokens in length."
#                         },
#                         "question": {
#                             "type": "object",
#                             "properties": {
#                                 "text": {
#                                     "type": "string",
#                                     "description": "The text of the question associated with the factoid."
#                                 },
#                                 "correct_choice": {
#                                     "type": "string",
#                                     "description": "The correct choice for the question."
#                                 },
#                                 "wrong_choices": {
#                                     "type": "array",
#                                     "items": {
#                                         "type": "string"
#                                     },
#                                     "minItems": 3,
#                                     "maxItems": 3,
#                                     "description": "Three incorrect choices for the question."
#                                 }
#                             },
#                             "required": ["text", "correct_choice", "wrong_choices"]
#                         }
#                     },
#                     "required": ["factoid_text", "question"]
#                 },
#                 "minItems": 4,
#                 "maxItems": 4,
#                 "description": "An array of four objects, each containing a factoid and its corresponding multiple-choice question."
#             }
#         },
#         "required": ["factoids"]
#     },
# }


def try_get_object(fcn, response_message):
    if response_message["function_call"]["name"] == fcn['name']:
        thingy = response_message["function_call"]["arguments"]
        profile_args = json.loads(thingy)
        
        # Extract required keys from the function definition
        required_keys = fcn['parameters']['required']

        # Check if all required keys are present and have non-empty values
        all_required_present = all(key in profile_args and (profile_args[key] is not None and (profile_args[key] or profile_args[key] == 0)) for key in required_keys)

        if all_required_present:
            # Extract all keys (both required and optional) for parameters
            all_keys = list(fcn['parameters']['properties'].keys())

            # Filter profile arguments to only include valid keys
            return {k: profile_args.get(k) for k in all_keys if profile_args.get(k) is not None}
        else:
            return None

    return None