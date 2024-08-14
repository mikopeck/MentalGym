import os
import requests
from azure.storage.blob import BlobServiceClient

from openapi import get_image
from database.library_handlers import update_library_image, get_library_details

# Initialize the BlobServiceClient
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "library-images"

def download_image(image_url):
    print("Downloading image...")
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def upload_file_to_blob(file_content, file_name):
    print("Uploading file to Azure Blob Storage...")
    print(connect_str)
    print(container_name)
    print(file_name)
    print(blob_service_client)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    print(blob_client)
    blob_client.upload_blob(file_content)
    print(blob_client.url)
    return blob_client.url

def get_guide_description(guide):
    if guide == "Bubbles":
        return "cheerful blue otter with a shiny, sleek fur and smile, playing with bubbles,"
    elif guide == "Irona":
        return "strict red fox with sharp eyes, a stern expression, wearing a black suit, pointing at something,"
    elif guide == "Sterling":
        return "gray horse with a strong, muscular build and a well-kept mane, standing tall with a confident posture in a proffessors coat and with square glasses,"
    else: #"Azalea"
        return "purple octopus with gracefully flowing tentacles, beckoning you to join,"

def generate_images_task(id):
    details_response, details_status = get_library_details(id)
    if details_status != 200:
        return details_response
    
    details = details_response.json
    topic = details['topic']
    guide = details['guide']
    difficulty = details['difficulty']
    guide_description = get_guide_description(guide)
        
    image_url = get_image(f"Pixel-art style game backdrop of a room with many decorations about: {topic}. A {guide_description} is next to a lone bookshelf amidst the decorations. The contents seem to be of {difficulty} difficulty and all about {topic}.")
    if not image_url:
        return "Failed to get image"
    print(image_url)

    # Download the image from the URL
    image_content = download_image(image_url)
    if not image_content:
        return "Failed to download image"
        
    # Define a unique name for the blob using the given ID
    blob_name = f"{id}.jpeg"

    # Upload the image content to Azure Blob Storage
    blob_url = upload_file_to_blob(image_content, blob_name)

    # Update url in db
    update_library_image(id, blob_url)
    print("updated")
    return "Success"