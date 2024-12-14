import numpy as np
import re

from openapi import get_embeddings
from database.db_handlers import user_knowledge_net_info
from knowledge_net.math_utils import calculate_cosine_similarities

def get_graph_data(user_id):
    user_data = user_knowledge_net_info(user_id)

    # Concatenating all strings from lessons and libraries
    all_strings = [lesson['name'] for lesson in user_data['completed_lessons']] + \
              [lesson['name'] for lesson in user_data['active_lessons']] + \
              [library['topic'] for library in user_data['completed_libraries']] + \
              [library['topic'] for library in user_data['active_libraries']] + \
              user_data['offered_lessons']

    print(all_strings)
    # Retrieve embeddings for all strings
    embeddings = get_embeddings(sanitize(all_strings))
    similarities = calculate_cosine_similarities(embeddings)
    
    edges = calculate_edges(similarities)
    graph_data = compose_data(user_data, edges)

    return graph_data

###### priv ######

def calculate_edges(similarities):
    num_nodes = similarities.shape[0]
    base_threshold = 0.3
    threshold_increase_per_edge = 0.16

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
        if similarity >= thresholds[i] or similarity >= thresholds[j]:
            # Calculate scaled similarity
            scaled_similarity = 0.1 + 0.9 * (similarity - base_threshold) / (1 - base_threshold)
            final_edges.append((i, j, scaled_similarity * scaled_similarity))

            # Update edge counts and thresholds for involved nodes
            edge_counts[i] += 1
            edge_counts[j] += 1
            thresholds[i] = base_threshold + edge_counts[i] * threshold_increase_per_edge
            thresholds[j] = base_threshold + edge_counts[j] * threshold_increase_per_edge

    return final_edges


def compose_data(user_data, edges):
    """
    Compose the graph data from user data and edges.

    :param user_data: A dictionary containing user's lessons and libraries data.
    :param edges: A list of tuples representing the edges in the graph.
    :return: A dictionary representing the graph with nodes and edges.
    """
    graph_data = {"nodes": [], "edges": []}

    # Combine all items into a single list for easy indexing, with IDs for those that have them
    all_items = []
    for category_key in ['completed_lessons', 'active_lessons', 'completed_libraries', 'active_libraries']:
        for item in user_data[category_key]:
            item_data = {
                "name": item['name'] if 'name' in item else item['topic'],
                "category": category_key[:-1],  # Removes the plural 's'
                "id": item.get('id')  # Adds the ID if present
            }
            all_items.append(item_data)

    # Add offered lessons and libraries without IDs
    for lesson in user_data['offered_lessons']:
        all_items.append({"name": lesson, "category": "offered_lesson"})

    # Adding nodes with their categories and IDs
    for item in all_items:
        graph_data['nodes'].append(item)

    # Adding edges with similarity strength
    for edge in edges:
        node1_index, node2_index, similarity = edge
        # Ensure the indices are within the range of all_items
        if 0 <= node1_index < len(all_items) and 0 <= node2_index < len(all_items):
            graph_data['edges'].append({
                "from": all_items[node1_index]['name'],
                "to": all_items[node2_index]['name'],
                "similarity": similarity
            })

    return graph_data

def sanitize(lessons):
    # Expanded list of words to remove, including some variations
    removal_list = [
        "advanced", "introduction", "basic", "basics",
        "fundamental", "fundamentals", "beginner", "intermediate",
        "intro", "essentials", "core", "effective"
    ]

    # Regular expression pattern to match any of the words in removal_list
    pattern = re.compile(r'\b(' + '|'.join(removal_list) + r')\b', re.IGNORECASE)

    # Sanitize the list by removing the specified words
    sanitized_lessons = [pattern.sub('', lesson).strip() for lesson in lessons]
    
    return sanitized_lessons