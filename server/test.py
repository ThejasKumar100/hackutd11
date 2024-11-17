import os
import requests

SERVER_URL = "http://localhost:8000/upload-images/"

def send_files_to_server(file_paths, user_id):
    """
    Send a list of files (images or PDFs) to the server for validation.
    """
    # Prepare files for upload
    files = []
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        # Determine content type based on file extension
        if file_path.endswith(".png"):
            content_type = "image/png"
        elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            content_type = "image/jpeg"
        elif file_path.endswith(".pdf"):
            content_type = "application/pdf"
        else:
            print(f"Unsupported file type for {filename}. Only .png, .jpeg, .jpg, and .pdf are supported.")
            continue
        
        files.append(("files", (filename, open(file_path, "rb"), content_type)))
    
    if not files:
        print("No valid files to upload.")
        return None
    
    # Include user_id as form data
    data = {"user_id": user_id}

    try:
        # Send POST request to server
        response = requests.post(SERVER_URL, data=data, files=files)
        response.raise_for_status()  # Raise an error for non-200 responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error communicating with the server: {e}")
        if e.response:
            print(f"Server responded with: {e.response.text}")
        return None

if __name__ == "__main__":
    # Example test setup
    file_dir = "./test_files"  # Directory with images and PDFs
    user_id = "test_user_123"  # Replace with the appropriate test user ID
    file_paths = [os.path.join(file_dir, file) for file in os.listdir(file_dir) if file.endswith((".png", ".jpg", ".jpeg", ".pdf"))]

    if not file_paths:
        print("No valid files found in the directory.")
    else:
        print(f"Loaded {len(file_paths)} file(s) from {file_dir}.")
        response = send_files_to_server(file_paths, user_id)
        if response:
            print("Server response:")
            print(response)
        else:
            print("Failed to get a valid response from the server.")
