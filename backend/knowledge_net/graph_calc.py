import numpy as np

from openapi import get_embeddings
from database.db_handlers import user_knowledge_net_info

def get_graph_data(user_id):
    user_data = user_knowledge_net_info(user_id)

    # Concatenating all strings from lessons and challenges
    all_strings = [lesson['name'] for lesson in user_data['completed_lessons']] + \
              [lesson['name'] for lesson in user_data['active_lessons']] + \
              [challenge['name'] for challenge in user_data['completed_challenges']] + \
              [challenge['name'] for challenge in user_data['active_challenges']] + \
              user_data['offered_lessons'] + user_data['offered_challenges']

    print(all_strings)
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
    base_threshold = 0.35
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

    # Combine all items into a single list for easy indexing, with IDs for those that have them
    all_items = []
    for category_key in ['completed_lessons', 'active_lessons', 'completed_challenges', 'active_challenges']:
        for item in user_data[category_key]:
            item_data = {
                "name": item['name'],
                "category": category_key[:-1],  # Removes the plural 's'
                "id": item.get('id')  # Adds the ID if present
            }
            all_items.append(item_data)

    # Add offered lessons and challenges without IDs
    for lesson in user_data['offered_lessons']:
        all_items.append({"name": lesson, "category": "offered_lesson"})
    for challenge in user_data['offered_challenges']:
        all_items.append({"name": challenge, "category": "offered_challenge"})

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