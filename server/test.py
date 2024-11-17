import os
import requests

SERVER_URL = "http://localhost:8000/upload-images/"

def send_images_to_server(image_paths, user_id):
    """
    Send a list of image files to the server for validation.
    """
    # Prepare files for upload
    files = [
        ("files", (os.path.basename(image_path), open(image_path, "rb"), "image/png" if image_path.endswith(".png") else "image/jpeg"))
        for image_path in image_paths
    ]
    
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
    image_dir = "./test_images"
    user_id = "test_user_123"  # Replace with the appropriate test user ID
    image_paths = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith((".png", ".jpg", ".jpeg"))]

    if not image_paths:
        print("No valid images found in the directory.")
    else:
        print(f"Loaded {len(image_paths)} image(s) from {image_dir}.")
        response = send_images_to_server(image_paths, user_id)
        if response:
            print("Server response:")
            print(response)
        else:
            print("Failed to get a valid response from the server.")
