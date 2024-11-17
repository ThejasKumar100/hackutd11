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
import openai
from dotenv import load_dotenv
import os
from pymongo import MongoClient

app = FastAPI()

# SAMBANOVA_API_KEY = os.environ.get("SAMBANOVA_API_KEY")
SAMBANOVA_API_KEY = load_dotenv()

# MongoDB Database Setup
load_dotenv()
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
test_database()

# Define the LLM response model for type checking
class ApplicationResponse(BaseModel):
    application_id: str
    user_id: str
    images: dict
    proposed_score: int
    proposed_limit: int
    is_approved: bool = None

# Function to extract text from images using OpenCV and pytesseract
def extract_text_from_image(image_bytes: bytes) -> str:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    preprocessed_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)[1]
    extracted_text = pytesseract.image_to_string(preprocessed_img)
    return extracted_text

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
        "Your task is to validate each entry individually and provide results in a JSON array format. "
        "For each entry, return the following fields:\n"
        "1. index (integer): The index of the text in the input list.\n"
        "2. is_valid (boolean): Whether the text meets validation requirements.\n"
        "3. reason (string): A short explanation if the text is invalid or additional context if valid.\n"
        "4. proposed_score (integer): An estimated credit score between 300 and 850.\n"
        "5. proposed_limit (integer): An estimated monthly credit limit in USD.\n\n"
        "Return a JSON object with a key `results`, containing an array of validation results for all inputs."
    )

    # Prepare the query and context for Sambanova API
    query = {
        "messages": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": {"texts": extracted_texts}}
        ],
        "model": "Llama-3.2-11B-Vision-Instruct",
        "temperature": 0.1,
        "top_p": 0.1
    }

    # Send the request to the Sambanova API
    response = requests.post(
        f"https://api.sambanova.ai/v1/chat/completions/create",
        headers={"Authorization": f"Bearer {SAMBANOVA_API_KEY}"},
        json=query
    )

    # Check if the response was successful
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Error communicating with Sambanova API: {response.text}")

    # Parse the response
    result = response.json()
    response_content = result.get("choices", [{}])[0].get("message", {}).get("content", "")

    try:
        # Attempt to parse the content into JSON
        parsed_result = eval(response_content)  # Using eval for quick prototyping; switch to `json.loads` for safety
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse LLM response: {response_content}")

    # Validate the response structure
    if "results" not in parsed_result:
        raise HTTPException(status_code=500, detail="LLM response missing expected 'results' field")

    # Return the parsed results
    return parsed_result

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
            # Validate file type
            print(f"Processing file: {file.filename}, Content-Type: {file.content_type}")
            if file.content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

            try:
                # Read image bytes
                image_bytes = await file.read()
                print(f"Read {len(image_bytes)} bytes from file: {file.filename}")

                # Extract text from the image
                extracted_text = extract_text_from_image(image_bytes)
                print(f"Extracted text from {file.filename}: {extracted_text[:100]}...")  # Log first 100 chars

                # Send the extracted text to the LLM for validation and score generation
                llm_result = validate_extracted_text_with_llm([extracted_text])
                print(f"LLM result for {file.filename}: {llm_result}")

                # Process the LLM response and format the output
                processed_results.append({
                    "filename": file.filename,
                    "is_valid": llm_result["results"][0].get("is_valid"),
                    "reason": llm_result["results"][0].get("reason", ""),
                    "extracted_text": extracted_text
                })

            except Exception as e:
                print(f"Error processing file {file.filename}: {e}")
                raise HTTPException(status_code=500, detail=f"Error processing file {file.filename}: {str(e)}")

        # After processing all images, prepare the final response
        response_data = {
            "application_id": application_id,
            "user_id": user_id,
            "images": processed_results,
            "proposed_score": llm_result["results"][0].get("proposed_score"),
            "proposed_limit": llm_result["results"][0].get("proposed_limit"),
            "is_approved": None  # Will be set by admin
        }

        save_to_database(response_data)

        return response_data

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the images.")

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