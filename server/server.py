from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import List
from pydantic import BaseModel
import cv2
import pytesseract
import numpy as np
import uuid
import requests
import uvicorn
import os
from dotenv import load_dotenv
from pymongo import MongoClient

app = FastAPI()

# MongoDB Database Setup
load_dotenv()
mongo_cluster_connection_string = os.getenv("MONGO_CLUSTER_CONNECTION_STRING")
client = MongoClient(mongo_cluster_connection_string)
db = client["SwagAwesomeMoney"]
collection = db["Baller"]

# Testing Database

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

# Define the LLM response model for type checking
class ApplicationResponse(BaseModel):
    application_id: str
    user_id: str
    images: dict
    proposed_score: int
    proposed_limit: int
    is_approved: bool = None  # Can be modified by admin later

# Function to extract text from images using OpenCV and pytesseract
def extract_text_from_image(image_bytes: bytes) -> str:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    preprocessed_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)[1]
    extracted_text = pytesseract.image_to_string(preprocessed_img)
    return extracted_text

# Function to validate extracted text (using LLM validation)
def validate_extracted_text_with_llm(extracted_text: str) -> dict:
    """
    Send extracted text to LLM for validation and credit score generation.
    This assumes the LLM endpoint processes the image text and returns validation and scores.
    """
    llm_endpoint = "http://your-llm-api-endpoint"
    context = {"text": extracted_text}

    # Example of sending request to LLM (replace with actual LLM interaction)
    response = requests.post(llm_endpoint, json=context)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error communicating with LLM API")

    return response.json()

# Endpoint to upload multiple images
@app.post("/upload-images/")
async def upload_images(files: List[UploadFile] = File(...), user_id: str = None):
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    processed_results = []
    application_id = str(uuid.uuid4())  # Generate a unique application ID

    for file in files:
        # validate file type
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

        try:
            # Read image bytes
            image_bytes = await file.read()

            # Extract text from the image
            extracted_text = extract_text_from_image(image_bytes)

            # Send the extracted text to the LLM for validation and score generation
            llm_result = validate_extracted_text_with_llm(extracted_text)

            # Process the LLM response and format the output
            processed_results.append({
                "filename": file.filename,
                "is_valid": llm_result.get("is_valid"),
                "reason": llm_result.get("reason", ""),
                "extracted_text": extracted_text
            })

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file {file.filename}: {str(e)}")

    # After processing all images, prepare the final response to store in the database
    response_data = {
        "application_id": application_id,
        "user_id": user_id,
        "images": processed_results,
        "proposed_score": llm_result.get("proposed_score"),
        "proposed_limit": llm_result.get("proposed_limit"),
        "is_approved": None  # Will be set by admin
    }

    # Save the result to the database (stubbed for now)
    # You can implement the database integration later here
    save_to_database(response_data)

    return response_data

# Placeholder function to save data to the database
def save_to_database(data: dict):
    # Example of saving to the database (PostgreSQL or MongoDB)
    mongo_data = collection.insert_one(data)
    print("MongoDB _id Inserted", mongo_data.inserted_id)
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)