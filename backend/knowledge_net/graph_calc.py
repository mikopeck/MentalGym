import numpy as np

from openapi import get_embeddings
from database.db_handlers import get_user_info

def get_graph_data(user_id):
    # # Completed Lessons (40)
    # completed_lessons = [
    #     "Introduction to Classical Mechanics: Newton's Laws",
    #     "Exploring Quantum Theory: Basics and Applications",
    #     "The Fundamentals of Thermodynamics: Heat and Energy",
    #     "Electricity and Magnetism: Understanding Electromagnetic Fields",
    #     "The Wonders of Light: Optics and Wave Theory",
    #     "Advanced Calculus: Differential Equations and Applications",
    #     "Introduction to Astrophysics: Stars and Galaxies",
    #     "The Chemical Bond: Fundamentals of Molecular Interaction",
    #     "Organic Chemistry: Structures, Bonds, and Reactions",
    #     "Biology of Cells: Structure and Function",
    #     "Human Anatomy: Exploring the Musculoskeletal System",
    #     "Environmental Science: Ecosystems and Biodiversity",
    #     "Introduction to Psychology: Understanding the Mind",
    #     "Foundations of Sociology: Society and Culture",
    #     "World History: Ancient Civilizations to Modern Times",
    #     "Understanding Economics: Markets and States",
    #     "Political Science: Governments and Policies",
    #     "Philosophy: Ethics, Logic, and Existence",
    #     "Literature Analysis: Themes and Techniques",
    #     "Creative Writing: Crafting Compelling Narratives",
    #     "Basic Programming: Introduction to Python",
    #     "Web Development: HTML, CSS, and JavaScript",
    #     "Data Science: Statistics and Machine Learning",
    #     "Artificial Intelligence: Concepts and Applications",
    #     "Robotics: Design and Programming Basics",
    #     "Engineering Principles: Design and Analysis",
    #     "Physics of Sound: Acoustics and Music",
    #     "Renewable Energy: Solar and Wind Power",
    #     "Aerospace Engineering: Principles of Flight",
    #     "Civil Engineering: Building and Infrastructure",
    #     "Medical Science: Diseases and Treatments",
    #     "Nursing Essentials: Patient Care and Ethics",
    #     "Pharmacology: Drugs and Their Effects",
    #     "Veterinary Science: Animal Health and Welfare",
    #     "Nutrition Science: Diet and Health",
    #     "Physical Education: Fitness and Wellness",
    #     "Art History: Renaissance to Contemporary",
    #     "Painting Techniques: Styles and Mediums",
    #     "Sculpture: Form, Technique, and Expression",
    #     "Music Theory: Harmony and Composition"
    # ]

    # # Active Lessons (8)
    # active_lessons = [
    #     "Film Studies: Analysis and Criticism",
    #     "Theater Arts: Performance and Production",
    #     "Dance: Techniques and Cultural Styles",
    #     "Photography: Capturing Light and Moments",
    #     "Graphic Design: Visual Communication and Branding",
    #     "Game Design: Mechanics and Storytelling",
    #     "Cybersecurity Fundamentals: Protecting Digital Assets",
    #     "Cloud Computing: Technologies and Services"
    # ]

    # # Completed Challenges (12)
    # completed_challenges = [
    #     "Master Quantum Mechanics Challenge",
    #     "Thermodynamics Expert Challenge",
    #     "Electromagnetism Solver Challenge",
    #     "Optics and Light Master Challenge",
    #     "Advanced Calculus Problem Solver",
    #     "Astrophysics Explorer Challenge",
    #     "Molecular Interaction Specialist",
    #     "Organic Chemistry Reaction Expert",
    #     "Cell Biology Mastery Challenge",
    #     "Musculoskeletal Anatomy Expert",
    #     "Environmental Ecosystem Guardian",
    #     "Psychology Fundamentals Explorer"
    # ]

    # # Active Challenges (4)
    # active_challenges = [
    #     "Renewable Energy Innovator Challenge",
    #     "Flight Dynamics Challenge",
    #     "Infrastructure Design Challenge",
    #     "Digital Asset Cybersecurity Challenge"
    # ]

    # # Mock user data as per the as_dict function
    # user_data = {
    #     "profile": None,
    #     "active_challenges": active_challenges, # lists of names 
    #     "completed_challenges": completed_challenges,
    #     "active_lessons": active_lessons,
    #     "completed_lessons": completed_lessons,
    #     "latest_action": None
    # }

    user_data = get_user_info(user_id)

    # Concatenating all strings from lessons and challenges
    all_strings = user_data['completed_lessons'] + user_data['active_lessons'] + \
                user_data['completed_challenges'] + user_data['active_challenges']

    # Retrieve embeddings for all strings
    embeddings = get_embeddings(all_strings)
    similarities = calculate_cosine_similarities(embeddings)
    
    edges = calculate_edges(similarities)
    graph_data = compose_data(user_data, edges)

    return graph_data

###### priv ######

def cosine_similarity(vecA, vecB):
    vectorA = np.array(vecA['embedding'])
    vectorB = np.array(vecB['embedding'])

    dot_product = np.dot(vectorA, vectorB)
    normA = np.linalg.norm(vectorA)
    normB = np.linalg.norm(vectorB)
    return dot_product / (normA * normB)

def calculate_cosine_similarities(embeddings):
    num_embeddings = len(embeddings)
    similarities = np.zeros((num_embeddings, num_embeddings))

    for i in range(num_embeddings):
        for j in range(i, num_embeddings):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            similarities[i, j] = sim
            similarities[j, i] = sim

    return similarities

def calculate_edges(similarities):
    num_nodes = similarities.shape[0]
    base_threshold = 0.8
    threshold_increase_per_edge = 0.05

    # Initialize thresholds and edge counts for each node
    thresholds = np.full(num_nodes, base_threshold)
    edge_counts = np.zeros(num_nodes, dtype=int)

    # Create a list of all possible edges with their similarities
    potential_edges = [(i, j, similarities[i, j]) for i in range(num_nodes) for j in range(i+1, num_nodes)]
    # Sort the list based on similarities in descending order
    potential_edges.sort(key=lambda x: x[2], reverse=True)

    final_edges = []

    for i, j, similarity in potential_edges:
        # Check if both nodes can still form an edge
        if similarity >= thresholds[i] and similarity >= thresholds[j]:
            # Calculate scaled similarity
            scaled_similarity = 0.1 + 0.9 * (similarity - base_threshold) / (1 - base_threshold)
            final_edges.append((i, j, scaled_similarity * scaled_similarity))

            # Update edge counts and thresholds for involved nodes
            edge_counts[i] += 1
            edge_counts[j] += 1
            thresholds[i] = min(base_threshold + edge_counts[i] * threshold_increase_per_edge, 1)
            thresholds[j] = min(base_threshold + edge_counts[j] * threshold_increase_per_edge, 1)

    return final_edges


def compose_data(user_data, edges):
    """
    Compose the graph data from user data and edges.

    :param user_data: A dictionary containing user's lessons and challenges data.
    :param edges: A list of tuples representing the edges in the graph.
    :return: A dictionary representing the graph with nodes and edges.
    """
    graph_data = {"nodes": [], "edges": []}

    # Combine all items into a single list for easy indexing
    all_items = user_data['completed_lessons'] + user_data['active_lessons'] + \
                user_data['completed_challenges'] + user_data['active_challenges']

    # Adding nodes with their categories
    for item in all_items:
        category = "completed_lesson" if item in user_data['completed_lessons'] else \
                   "active_lesson" if item in user_data['active_lessons'] else \
                   "completed_challenge" if item in user_data['completed_challenges'] else \
                   "active_challenge"
        graph_data['nodes'].append({
            "name": item,
            "category": category
        })

    # Adding edges with similarity strength
    for edge in edges:
        node1_index, node2_index, similarity = edge
        graph_data['edges'].append({
            "from": all_items[node1_index],
            "to": all_items[node2_index],
            "similarity": similarity
        })

    return graph_data
