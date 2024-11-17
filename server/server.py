import base64
import datetime
from fastapi import FastAPI, Form, HTTPException, File, UploadFile
from typing import List, Tuple
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
SAMBANOVA_CLIENT = OpenAI(
        base_url="https://api.sambanova.ai/v1",
        api_key=SAMBANOVA_API_KEY
    )

# Define the LLM response model for type checking
class ApplicationResponse(BaseModel):
    user_id: str
    images: dict
    proposed_score: int
    proposed_limit: int
    is_approved: bool = None

@app.post("/upload-images/")
async def upload_images(
    files: List[UploadFile] = File(...),  # a list of pictures uploaded from the user
    user_id: str = Form(...),
):
    print(f"Received user_id: {user_id}, Number of files: {len(files)}")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    try:
        # Process images
        processed_results, extracted_texts = await process_images(files)  # results and corresponding text returned separately since the text is needed for LLM validation

        # After extracting all texts, validate them in a single call
        llm_results = validate_images_with_llm(extracted_texts)

        # Assign the validation results to the corresponding files
        for idx, result in enumerate(processed_results):
            if result["extracted_text"]:  # if we have extracted text, then we can assign the validation results
                validation = llm_results[idx]
                
                # Log the raw LLM response for debugging
                print(f"LLM validation response for file {result['filename']}: {validation}")
                
                # Ensure the response contains 'is_valid' and 'reason' keys
                # Ensure the response contains 'is_valid' and 'reason' keys
        if "is_valid" in validation and "reason" in validation:
            result["is_valid"] = validation["is_valid"]
            result["reason"] = validation["reason"]
            result["data"] = validation["data"]  # Ensure `data` is properly assigned
        else:
            # Handle the case where LLM response is not as expected
            result["is_valid"] = False
            result["reason"] = "LLM response format is incorrect or missing necessary fields."
            result["data"] = None  # Ensure `data` is set to `None` in case of error
            print(f"Error: Missing expected keys in LLM response for {result['filename']}")

        # After processing all images, calculate proposed score and limit
        valid_images = [result for result in processed_results if result and result.get("is_valid")]

        proposed_score, proposed_limit = calculate_proposed_credit(valid_images)
        print(f"Proposed credit score: {proposed_score}, Proposed credit limit: {proposed_limit}")

        # Prepare the final response
        response_data = {
            "user_id": user_id,
            "images": processed_results,
            "proposed_score": proposed_score,
            "proposed_limit": proposed_limit,
            "is_approved": None,  # Will be set by admin
            "submitted_at": datetime.datetime.now()
        }

        print("Saving to database...")
        save_to_database(response_data)

        if valid_images:
            # If at least one valid image, we confirm submission was successful
            return {"status": "success", "message": "Your application was successfully submitted for review."}
        else:
            # If no valid images, notify the user without giving specifics on failure
            return {"status": "failure", "message": "Your application could not be processed. Please try again."}

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the images, please try again with new images.")


async def process_images(files: List[UploadFile]) -> Tuple[List[dict], List[str]]:
    """
    Process images by extracting text and encoding the image.
    Returns a tuple of processed results and a list of extracted texts.
    """
    processed_results = []
    extracted_texts = []

    # loop through eaach provided files and extract the text and file information, set up for LLM validation
    for idx, file in enumerate(files):
        try:
            # Validate file type
            print(f"Processing file: {file.filename}, Content-Type: {file.content_type}")
            if file.content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

            # Read image bytes
            image_bytes = await file.read()
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")  # Encode image data
            print(f"Read {len(image_bytes)} bytes from file: {file.filename}")

            # Extract text from the image bytes
            extracted_text = extract_text_from_image(image_bytes)
            print(f"Extracted text from {file.filename}: {extracted_text[:200]}...")  # log the first 200 characters

            # Accumulate the extracted text
            extracted_texts.append(extracted_text)

            # Add the file info to the processed results, without LLM validation yet
            processed_results.append({
                "filename": file.filename,
                "extracted_text": extracted_text,
                "image_data": encoded_image,
                "is_valid": None,  # Will be filled later
                "reason": ""  # Will be filled later
            })

        except Exception as e:
            print(f"Error processing file {file.filename}: {e}")
            processed_results.append({
                "filename": file.filename,
                "is_valid": False,
                "reason": f"Error: {str(e)}",
                "extracted_text": None,
                "image_data": None
            })

    return processed_results, extracted_texts


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
def validate_images_with_llm(extracted_texts: List[str]) -> List[dict]:
    """
    Validate the extracted text using the SambaNova LLM API. Returns a list of validation results with the format {is_valid, reason, data}.
    """
    if not SAMBANOVA_API_KEY:
        raise HTTPException(status_code=500, detail="API key not found in environment variables")

    instructions = (
        "You are validating a financial statement extracted from an image for a credit application. "
        "For this particular financial statement, ensure it meets these criteria: 1) All mandatory fields are present (e.g., date, amount). "
        "2) Numerical values are within reasonable ranges. 3) The format matches standard financial documents. "
        "When validating, consider the possibility of fraudulent or inaccurate data, and provide a reason for rejection."
        "However, note that the data format may be given the benefit of the doubt, as the text is extracted from images and thus does not line up perfectly."
        "Return a JSON object with 'is_valid' (boolean), 'reason' (string), and any additional metadata."
        "Return only the JSON object, do not include code, text, or any other information, do not use markdown."
    )

    validated_images = []
    for extracted_text in extracted_texts:
        try:
            response = SAMBANOVA_CLIENT.chat.completions.create(
                model='Llama-3.2-11B-Vision-Instruct',
                messages=[{"role": "system", "content": instructions}, 
                          {"role": "user", "content": extracted_text}],
                temperature=0.1,
                top_p=0.1
            )
            
            # Log the raw response for debugging
            print(f"Raw response from LLM API: {response}")
            
            # Parse and clean the LLM response
            parsed_response = parse_llm_response(response)

            validated_images.append({
                "is_valid": parsed_response.get("is_valid", False),
                "reason": parsed_response.get("reason", ""),
                "data": extracted_text
            })

        except Exception as e:
            print(f"Error during LLM validation: {e}")
            validated_images.append({
                "is_valid": False,
                "reason": f"Error: {str(e)}",
                "data": extracted_text
            })

    return validated_images



def parse_llm_response(response):
    try:
        # Convert the ChatCompletion object to a dictionary if it's not already
        if hasattr(response, "to_dict"):
            response = response.to_dict()
            # print("Converted ChatCompletion to dictionary")

        # Debug: Print the converted response
        # print(f"Converted response: {response}")

        # Check that the response contains `choices`
        if "choices" not in response or not response["choices"]:
            raise HTTPException(status_code=500, detail="Response is missing 'choices'")

        # Extract the content field from the first choice
        content = response["choices"][0]["message"].get("content")
        if not content:
            raise HTTPException(status_code=500, detail="Response content is missing")

        # Clean the markdown formatting if present (assuming it's in JSON markdown format)
        if content.startswith('```json\n'):
            content = content[len('```json\n'):].strip()  # Strip the opening markdown block
        if content.endswith('```'):
            content = content[:-3].strip()  # Strip the closing markdown block

        # Parse the content as JSON
        try:
            parsed_response = json.loads(content)
            print(f"Parsed response content: {parsed_response}")
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Invalid JSON in response content: {str(e)}")

        # Check for the necessary fields in the parsed response (for validation)
        if "is_valid" not in parsed_response or "reason" not in parsed_response:
            raise HTTPException(status_code=500, detail="Invalid response format: missing 'is_valid' or 'reason'")

        return parsed_response

    except Exception as e:
        print(f"Error during LLM response parsing: {e}")
        raise HTTPException(status_code=500, detail=f"Error during LLM response parsing: {str(e)}")

def calculate_proposed_credit(validated_images: List[dict]) -> dict:
    """
    Calculate the proposed credit score and credit limit using only valid entries.
    Returns a dictionary with 'proposed_score' and 'proposed_limit'.
    """
    valid_entries = [image["data"] for image in validated_images if image["is_valid"]]

    if not valid_entries:
        return {
            "proposed_score": 0,  # Default or error state
            "proposed_limit": 0,  # Default or error state
        }

    instructions = (
        "You are tasked with determining a proposed credit score and limit based on valid financial data entries. "
        "Analyze the data and return a JSON object with 'proposed_score' and 'proposed_limit'."
        "The proposed score should be an integer between 300 and 850, representing your estimation for the user's credit score."
        "The proposed limit should be an integer representing your estimation for the user's monthly credit limit, minimum 1000."
        "For additional context, the user does not have any existing credit history, and is an individual with limited access to traditional banks."
        "Return only the JSON object, do not include code, text, or any other information, do not use markdown."
    )

    response = SAMBANOVA_CLIENT.chat.completions.create(
        model='Llama-3.2-11B-Vision-Instruct',
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": json.dumps(valid_entries)}
        ],
        temperature=0.1,
        top_p=0.1
    )

    content = json.loads(response.choices[0].message.content)

    return content.get("proposed_score", 0), content.get("proposed_limit", 0)


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