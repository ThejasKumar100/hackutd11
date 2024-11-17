import base64
import datetime
from fastapi import FastAPI, Form, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
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
import fitz
from bson.json_util import dumps

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend URL for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()


# MongoDB Database Setup
mongo_cluster_connection_string = os.getenv("MONGO_CLUSTER_CONNECTION_STRING")
client = MongoClient(mongo_cluster_connection_string)
db = client["SwagAwesomeMoney"]
collection = db["Baller"]
customer_collection = db["Customer"]

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
        processed_results = await process_files(files)  # results and corresponding text returned separately since the text is needed for LLM validation

        # After extracting all texts, validate them in a single call
        llm_results = validate_images_with_llm(processed_results)

        # After processing all images, calculate proposed score and limit
        valid_images = [result for result in llm_results if result and result.get("is_valid")]

        proposed_score, proposed_limit = calculate_proposed_credit(valid_images)
        print(f"Proposed credit score: {proposed_score}, Proposed credit limit: {proposed_limit}")

        # Prepare the final response
        response_data = {
            "user_id": user_id,
            "images": llm_results,
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


async def process_files(files: List[UploadFile]) -> List[dict]:
    """
    Process image and PDF files by extracting text and encoding the data.
    Returns a tuple of processed results and a list of extracted texts.
    """
    processed_results = []

    for file in files:
        try:
            # Validate file type
            print(f"Processing file: {file.filename}, Content-Type: {file.content_type}")

            # Handle image files
            if file.content_type in ["image/jpeg", "image/png"]:
                image_bytes = await file.read()
                encoded_image = base64.b64encode(image_bytes).decode("utf-8")  # Encode image data
                print(f"Read {len(image_bytes)} bytes from file: {file.filename}")

                # Extract text from the image bytes
                extracted_text = extract_text_from_image(image_bytes)
                print(f"Extracted text from {file.filename}: {extracted_text[:200]}...")

                processed_results.append({
                    "filename": file.filename,
                    "extracted_text": extracted_text,
                    "data": encoded_image,
                    "is_valid": None,
                    "reason": "temp reason"
                })

            # Handle PDF files
            elif file.content_type == "application/pdf":
                pdf_bytes = await file.read()
                extracted_text = extract_text_from_pdf(pdf_bytes)
                print(f"Extracted text from {file.filename}: {extracted_text[:200]}...")
                pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

                processed_results.append({
                    "filename": file.filename,
                    "extracted_text": extracted_text,
                    "data": pdf_base64,  # stored a bit differently
                    "is_valid": None,
                    "reason": "temp reason"
                })

            else:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

        except Exception as e:
            print(f"Error processing file {file.filename}: {e}")
            processed_results.append({
                "filename": file.filename,
                "extracted_text": None,
                "data": None,
                "is_valid": False,
                "reason": f"Error: {str(e)}",
            })

    return processed_results


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

# Function to extract text from PDF files using PyMuPDF
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    """
    try:
        pdf_document = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
        extracted_text = ""

        # Extract text from each page
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            extracted_text += page.get_text()

        return extracted_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        raise ValueError(f"Failed to extract text from PDF: {e}")

# Function to validate extracted text (using LLM validation)
def validate_images_with_llm(processed_results: List[dict]) -> List[dict]:
    """
    Validate the extracted text from processed_results using the SambaNova LLM API.
    Updates the processed_results list in place with 'is_valid' and 'reason' fields.
    """
    if not SAMBANOVA_API_KEY:
        raise HTTPException(status_code=500, detail="API key not found in environment variables")

    instructions = (
        "You are validating a financial statement extracted from an image for a credit application. "
        "For this particular financial statement, ensure it meets these criteria: 1) All mandatory fields are present (e.g., date, amount). "
        "2) Numerical values are within reasonable ranges. 3) The format matches standard financial documents. "
        "When validating, consider the possibility of fraudulent or inaccurate data, and provide a reason for rejection. "
        "However, note that the data format may be given the benefit of the doubt, as the text is extracted from images and/or PDFs and thus does not line up perfectly with raw text. "
        "Return a JSON object with 'is_valid' (boolean), 'reason' (string), and any additional metadata. "
        "Return only the JSON object, do not include code, text, or any other information, do not use markdown."
    )

    for result in processed_results:
        extracted_text = result.get("extracted_text")
        
        # Skip validation if no extracted text
        if not extracted_text:
            result["is_valid"] = False
            result["reason"] = "No extracted text available for validation."
            continue
        
        try:
            response = SAMBANOVA_CLIENT.chat.completions.create(
                model='Llama-3.2-11B-Vision-Instruct',
                messages=[{"role": "system", "content": instructions}, 
                          {"role": "user", "content": extracted_text}],
                temperature=0.1,
                top_p=0.1
            )

            # Log the raw response for debugging
            print(f"Raw response from LLM API for {result['filename']}: {response}")

            # Parse and clean the LLM response
            parsed_response = parse_llm_response(response)

            # Update the result in place
            result["is_valid"] = parsed_response.get("is_valid", False)
            result["reason"] = parsed_response.get("reason", "No reason provided.")
        
        except Exception as e:
            print(f"Error during LLM validation for {result['filename']}: {e}")
            result["is_valid"] = False
            result["reason"] = f"Validation failed due to an error: {str(e)}"

    return processed_results  # Returning for consistency, though updates are in place.


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
    valid_entries = [image["extracted_text"] for image in validated_images if image["is_valid"]]

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
    print(f"Proposed credit response: {content}")
    return content.get("proposed_score", 0), content.get("proposed_limit", 0)


# Placeholder function to save data to the database
def save_to_database(data: dict):
    # Example of saving to the database (PostgreSQL or MongoDB)
    mongo_data = collection.insert_one(data)
    print("MongoDB _id Inserted", mongo_data.inserted_id)
    pass

# Get Applications Endpoints (For Admin Dashboard and Decision Screens)
# Database: SwagAwesomeMoney, Collection: Baller

@app.get("/all-apps/")
def get_all_apps():
    all_apps_data = dumps(collection.find({}))
    return all_apps_data

@app.get("/pending-apps/")
def get_pending_apps():
    pending_apps_data = dumps(collection.find({"is_approved": None}))
    return pending_apps_data

@app.get("/completed-apps/")
def get_completed_apps():
    completed_apps_data = dumps(collection.find({ "$or": [ {"is_approved": True}, {"is_approved": False} ]}))
    return completed_apps_data

# Applications for Specific User
@app.get("/user-apps/{user_id}")
def get_user_apps(user_id):
    user_apps_data = dumps(collection.find({"user_id": user_id}))
    return user_apps_data

# Endpoints for Nabil
# Database: SwagAwesomeMoney, Collection: Customer (customer_collection)

# Uses query parameters (user_id is auth0 id)
@app.post("/new-customer/")
def insert_new_customer(user_id: str, name: str, email: str, phone: str, address: str):
    json_data = {"user_id": user_id, "name": name, "email": email, "phone": phone, "address": address}
    mongo_data = customer_collection.insert_one(json_data)
    print("MongoDB Customer with user_id Inserted", user_id)

# user_id is the auth0 id
@app.get("/customer/{user_id}")
def get_customer_data(user_id):
    customer_data = dumps(customer_collection.find({"user_id": user_id}))
    return customer_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)