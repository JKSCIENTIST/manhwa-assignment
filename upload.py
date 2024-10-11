import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv('S:/manhwa_Assignment/.env')

# Azure Blob Storage details from the .env file

connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_STORAGE_CONTAINER')

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Function to sanitize blob name
def sanitize_blob_name(blob_name):
    # Replace invalid characters with underscores or other valid characters
    blob_name = re.sub(r'[^a-zA-Z0-9\-_\.]', '_', blob_name)
    return blob_name

# Function to upload a file to Azure Blob Storage
def upload_image(file_path):
    # Sanitize the blob name (file name)
    blob_name = sanitize_blob_name(os.path.basename(file_path))
    blob_client = container_client.get_blob_client(blob_name)
    
    try:
        # Check if the blob already exists
        blob_properties = blob_client.get_blob_properties()
        print(f"The image '{blob_name}' already exists in the container.")
        
        # Ask if the user wants to replace it
        replace = input(f"Do you want to replace the existing image '{blob_name}'? (y/n): ").lower()
        
        if replace == 'y':
            # Upload the image (replace the existing one)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"The image '{blob_name}' has been replaced.")
        else:
            print(f"The image '{blob_name}' was not replaced.")
    
    except Exception as e:
        # If the blob doesn't exist, upload it
        print(f"Uploading new image: {blob_name}")
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f"The image '{blob_name}' has been uploaded successfully.")

# Function to upload all images in a folder
def upload_images_in_folder(folder_path):
    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file is an image
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            print(f"Processing file: {file_name}")
            upload_image(file_path)
        else:
            print(f"Skipping non-image file: {file_name}")

# Example: Upload all images from a folder
folder_path = r'S:\manhwa_Assignment\static\images'  # Change this to your image folder path
upload_images_in_folder(folder_path)
