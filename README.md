# EasyTeller for HackUTD XI

This project is a web application designed to assist with credit and loan applications for customers with a lack of reportable credit history and/or income while tackling the Goldman Sachs and SambdaNova challenges at HackUTD XI

## Background

### Problem

When a user wants to apply for a loan but doesn't have anextensive credit history, it's difficult for banks to guage trustworthiness to approve loan applications. Similarly, it's difficult for banks to determine a credit score for first-time credit users. These issues are compounded in a variety of situations, such as when a customer primarly uses cash or lives far from a physical bank location. As a result, it can be difficult for customers who struggle to gain access to traditional banking services to gain financial assistance, while also ensuring that the bank can filter out fradulent claims.

### Our Solution

EasyTeller allows users to use alternative financial documents (such as rent receipts, car payments, utilities and other bills, etc.) to help demonstrate a proof of income to banks, while providing an easy pipeline of data to facilitate this interaction. Furthermore, AI-powered analytics make this process simplified for auditors to approve loan and credit requests using these documents.

### How It Works

1. User Submission

- Users sign in to the app and apply for a credit card or loan
- They upload their government ID and financial statements

2. Document Processing

- The server processes each uploaded file:
  - Images (PNG/JPG) are scanned using the OpenCV library for text extraction
  - PDFs are parsed using the Fitz library
- The extracted text and images are sent to the SambaNova Cloud API for validation. The AI model checks for:
  - Coherence and legibility
  - Fraud indicators, such as unusual formatting

3. Validation and Analysis:

- The AI validates each document, marking it as valid or invalid with reasons provided
- Valid documents are bundled together for an additional analysis to perform consistency checks, ensuring details like names and income levels align across submissions

4. Credit or Loan Assessment:

- For credit card applications, the system estimates a credit score and monthly credit limit
- For loan applications, a suggested maximum loan amount is calculated
- All results are stored in MongoDB, and the application is marked as pending

5. Auditor Review:

- Admin users access the app's portal to review pending applications
- Auditors can:
  - View submitted files and model analyses
  - Make manual adjustments to estimates if needed
  - Approve or reject applications

Just as banks employ a final screening process where a real human verifies checks submitted digitally, EasyTeller also includes a final level of human validation. This ensures that auditors can review the AI-generated analyses, verify the authenticity of documents, and make informed decisions to approve or reject applications. By combining AI-powered automation with human oversight, the app balances efficiency with accuracy and reliability

## Technologies Used

### Frontend

- Framework: SvelteKit
- Language: TypeScript
- Features: Modular components for handling authentication, file uploads, and user/admin interactions, with intuitive routing for seamless navigation throughout the app's pages

### Backend

- Framework: FastAPI
- Language: Python
- Features: Endpoints for user data management, file processing, and credit application handling. Also features integration with the SambaNova Cloud API for AI-powered financial analysis on validated text/files
- Additional Tools: Tesseract OCR is used for text extraction from uploaded images, and MongoDB is used for storing user data, document validation results, and credit applications

## Installation

### Prerequisies

1. Node.js (for the packages utilized by the frontend using npm)
2. Python
3. Tesseract OCR (installed locally, installation instructions [here](https://github.com/tesseract-ocr/tesseract#installation))

### Steps

1. Clone the repo

```
git clone https://github.com/ThejasKumar100/hackutd11
cd hackutd11
```

2. Frontend Setup

```
npm install
cd FE
cd webApp
npm install
npm run dev
```

3. Backend Setup

```
cd server
pip install -r requirements.txt
python server.py
```

4. Tesseract Installation

- Ensure Tesseract is installed and accessible in your system's PATH
- Verify using the following command

```
tesseract --version
```

5. Database Setup

- Ensure that MongoDB is accessible by updating the backend configuration to connect to your MongoDB instance

## Usage

1. Start the backend server with:

```
python main.py
```

2. Start the frontend client with:

```
npm run dev
```

3. Access the app in your browser at [http://localhost:3000](http://localhost:3000)
4. Create an account and then log in, then feel free to explore the app's features with the provided test files, such as submitting a credit application and monitoring the status of existing applications

## Acknowledgements

Special thanks to Goldman Sachs and SambaNova for providing thought-provoking challenges and inspiring the motivation for the app. Additionally, thank you to the HackUTD organizers for putting together the largest 24hr hackathon in North America!
