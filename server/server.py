from fastapi import FastAPI, Form, HTTPException, File, UploadFile
from typing import List
from pydantic import BaseModel
import cv2
import pytesseract
import numpy as np
import uuid
import requests
import uvicorn
import os
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from dotenv import load_dotenv
import os
import io
from pymongo import MongoClient
from PIL import Image
import json

app = FastAPI()
load_dotenv()


# MongoDB Database Setup
mongo_cluster_connection_string = os.getenv("MONGO_CLUSTER_CONNECTION_STRING")
client = MongoClient(mongo_cluster_connection_string)
db = client["SwagAwesomeMoney"]
collection = db["Baller"]

# Testing Database
def test_database():
    # Initial Query Test Data
    print("Initial data below if any")
    results = collection.find({})
    for document in results:
        print("initial document", document)

    # Insert Test Data
    testing_data = {"name": "Emily", "group": "capybara"}
    testing_insert = collection.insert_one(testing_data)
    print("Testing Insert Object", testing_insert)
    print("Testing Insert _id", testing_insert.inserted_id)

    # Query Test Data
    results = collection.find({"name": "Emily", "group": "capybara"})
    for document in results:
        print("added document", document)

    # Remove Test Data
    collection.delete_many({"name": "Emily", "group": "capybara"})

    # Query Test Data to Check Removal
    test_removal_flag = True
    results = collection.find({"name": "Emily", "group": "capybara"})
    for document in results:
        print("remaining document", document)
        test_removal_flag = False
    if test_removal_flag:
        print("Document successfully removed.")
    else:
        print("ERROR: Document not removed.")

# Comment Out If Needed
#test_database()

SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")

# Define the LLM response model for type checking
class ApplicationResponse(BaseModel):
    application_id: str
    user_id: str
    images: dict
    proposed_score: int
    proposed_limit: int
    is_approved: bool = None

@app.post("/upload-images/")
async def upload_images(
    files: List[UploadFile] = File(...),
    user_id: str = Form(...)
):
    print(f"Received user_id: {user_id}, Number of files: {len(files)}")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    processed_results = []
    application_id = str(uuid.uuid4())  # Generate a unique application ID

    try:
        for file in files:
            try:
                # Validate file type
                print(f"Processing file: {file.filename}, Content-Type: {file.content_type}")
                if file.content_type not in ["image/jpeg", "image/png"]:
                    raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

                # Read image bytes
                image_bytes = await file.read()
                print(f"Read {len(image_bytes)} bytes from file: {file.filename}")

                # Extract text from the image
                extracted_text = extract_text_from_image(image_bytes)
                print(f"Extracted text from {file.filename}: {extracted_text[:100]}...")  # Log first 100 chars

                # Send the extracted text to the LLM for validation and score generation
                llm_result = validate_extracted_text_with_llm([extracted_text])
                print(f"LLM result for {file.filename}: {llm_result}")

                # Extract data from LLM response
                images_data = llm_result.get("images", {})
                image_key = list(images_data.keys())[0]  # Assuming single image per request
                image_result = images_data[image_key]

                processed_results.append({
                    "filename": file.filename,
                    "is_valid": image_result.get("is_valid"),
                    "reason": image_result.get("reason", ""),
                    "extracted_text": extracted_text
                })

            except Exception as e:
                print(f"Error processing file {file.filename}: {e}")
                processed_results.append({
                    "filename": file.filename,
                    "is_valid": False,
                    "reason": f"Error: {str(e)}",
                    "extracted_text": None
                })

        # After processing all images, prepare the final response
        response_data = {
            "application_id": application_id,
            "user_id": user_id,
            "images": processed_results,
            "proposed_score": None,   # Update based on actual logic
            "proposed_limit": None,  # Update based on actual logic
            "is_approved": None  # Will be set by admin
        }

        # Save to database and retrieve the inserted document's _id
        inserted_doc = save_to_database(response_data)
        response_data["_id"] = str(inserted_doc["_id"])

        return response_data

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the images.")



def preprocess_image(image_bytes):
    # convert bytes to an OpenCV image
    image = np.array(Image.open(io.BytesIO(image_bytes)))

    # convert to grayscale
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # increase contrast
    # contrast_image = cv2.equalizeHist(gray_image)
    # _, thresh_image = cv2.threshold(contrast_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return image

# Function to extract text from images using OpenCV and pytesseract
def extract_text_from_image(image_bytes: bytes) -> str:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Extract text from image
    extracted_text = pytesseract.image_to_string(img)

    # Clean the extracted text: Join lines with a space to avoid multiple entries
    cleaned_text = " ".join(extracted_text.splitlines())

    return cleaned_text

# Function to validate extracted text (using LLM validation)
def validate_extracted_text_with_llm(extracted_texts: List[str]) -> dict:
    """
    Send extracted text to Sambanova API for validation and credit score generation.
    The extracted text is passed to the model along with context.
    """
    
    if not SAMBANOVA_API_KEY:
        raise HTTPException(status_code=500, detail="API key not found in environment variables")

    instructions = (
        "You are an assistant validating and processing financial statements for a credit application. "
        "You will receive a list of texts, where each entry corresponds to financial details extracted from a single image. "
        "Your task is to validate each entry individually and return the results in the following JSON format:\n"
        "The response should be an object with the following structure:\n"
        "1. 'images' (object): An object where each key corresponds to an image identifier (e.g., 'image1', 'image2') and the value is an object containing:\n"
        "    - 'data' (string): The picture embedded code (binary or encoded data).\n"
        "    - 'is_valid' (boolean): Whether the extracted information from the image is valid.\n"
        "    - 'reason' (string): A short explanation if the text is invalid or additional context if valid.\n"
        "2. 'proposed_score' (integer): An estimated credit score between 300 and 850, calculated based only on the valid entries.\n"
        "3. 'proposed_limit' (integer): An estimated monthly credit limit in USD, calculated based only on the valid entries.\n\n"
        "Your output should be a single JSON object, containing:\n"
        "- 'images': An object with the keys for each image and the associated validation data.\n"
        "- 'proposed_score' and 'proposed_limit': Estimated values based on valid entries.\n"
        "Your output should ONLY include the JSON structure described above. Do not include any Python code, explanations, or other text."
    )

    # send the request to the Sambanova API
    sambaNovaClient = OpenAI(
        base_url="https://api.sambanova.ai/v1", 
        api_key=SAMBANOVA_API_KEY
    )

    response = sambaNovaClient.chat.completions.create(
        model='Llama-3.2-11B-Vision-Instruct',
        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": "\n".join(extracted_texts)}
            ],
        temperature =  0.1,
        top_p = 0.1
    )

    print(response.choices[0].message.content)

    parsed_result = parse_llm_response(response)

    return parsed_result

def parse_llm_response(response):
    try:
        # Convert the ChatCompletion object to a dictionary if necessary
        if hasattr(response, "to_dict"):
            response = response.to_dict()
            print("Converted ChatCompletion to dictionary")

        # Debug: Print the converted response
        # print(f"Converted response: {response}")

        # Check that the response contains `choices`
        if "choices" not in response or not response["choices"]:
            raise HTTPException(status_code=500, detail="Response is missing 'choices'")

        # Extract the `content` field from the first choice
        content = response["choices"][0]["message"].get("content")
        if not content:
            raise HTTPException(status_code=500, detail="Response content is missing")

        # Parse the `content` as JSON
        try:
            parsed_response = json.loads(content)
            print(f"Parsed response content: {parsed_response}")
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Invalid JSON in response content: {str(e)}")

        # Check for 'images' key in the parsed response
        if "images" not in parsed_response:
            raise HTTPException(status_code=500, detail="Invalid response format: missing 'images' key")

        images = parsed_response["images"]
        print(f"Parsed images: {images}")

        # Validate that each image entry has the correct structure
        for image_id, image_data in images.items():
            if not isinstance(image_data, dict):
                raise HTTPException(status_code=500, detail=f"Invalid structure for image {image_id}")

            # Ensure each image has the necessary fields
            if 'data' not in image_data or 'is_valid' not in image_data or 'reason' not in image_data:
                raise HTTPException(status_code=500, detail=f"Missing expected fields in {image_id} data")

        # Ensure 'proposed_score' and 'proposed_limit' exist at the top level and handle null values
        proposed_score = parsed_response.get('proposed_score')
        proposed_limit = parsed_response.get('proposed_limit')

        if proposed_score is not None and not isinstance(proposed_score, int):
            raise HTTPException(status_code=500, detail="Invalid 'proposed_score' value")
        if proposed_limit is not None and not isinstance(proposed_limit, int):
            raise HTTPException(status_code=500, detail="Invalid 'proposed_limit' value")

        return parsed_response

    except Exception as e:
        print(f"Error processing LLM response: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing LLM response: {str(e)}")



# Placeholder function to save data to the database
def save_to_database(data: dict):
    # Example of saving to the database (PostgreSQL or MongoDB)
    mongo_data = collection.insert_one(data)
    print("MongoDB _id Inserted", mongo_data.inserted_id)
    pass

# Get Applications Endpoints

@app.get("/all-apps/")
def get_all_apps():
    all_apps_data = collection.find({})
    return all_apps_data

@app.get("/pending-apps/")
def get_pending_apps():
    pending_apps_data = collection.find({"is_approved": None})
    return pending_apps_data

@app.get("/completed-apps/")
def get_completed_apps():
    completed_apps_data = collection.find({ "$or": [ {"is_approved": True}, {"is_approved": False} ]})
    return completed_apps_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)