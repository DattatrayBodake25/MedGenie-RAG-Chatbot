# medgenie-rag-chatbot
MedGenie is a powerful RAG-based chatbot that delivers accurate medical answers by retrieving relevant documents from a Pinecone index and leveraging Google Gemini AI for response generation. It helps users with medical queries by combining real-time data and generative AI for precise and context-aware answers. Perfect for healthcare applications!

# MediGenie - Medical RAG Chatbot

MediGenie is an end-to-end Retrieval-Augmented Generation (RAG) based chatbot designed to provide accurate, document-based answers to medical queries. It uses Pinecone for vector storage and retrieval, and Google Gemini (Flash 1.5) for generating answers based on the retrieved context. The system is built using FastAPI and integrates with various libraries such as LangChain, HuggingFace, and Pinecone.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation and Setup](#installation-and-setup)
    - [Clone the Repository](#clone-the-repository)
    - [Install Dependencies](#install-dependencies)
    - [Set Up Environment Variables](#set-up-environment-variables)
5. [Run the Application](#run-the-application)
6. [API Endpoints](#api-endpoints)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

MediGenie answers medical queries by retrieving relevant documents and generating answers using advanced natural language processing (NLP) techniques. The system is designed to efficiently index, search, and generate accurate responses for medical-related queries using a combination of document-based retrieval and generative AI.

## Features

- **Document-based Answer Generation**: Uses a set of medical documents indexed in Pinecone to answer questions.
- **Medical Knowledge Base**: Built using the MedQuad dataset and can be updated with new medical documents as needed.
- **FastAPI Backend**: The server is built using FastAPI to handle requests efficiently.
- **Google Gemini (Flash 1.5)**: Utilizes Google Gemini for generating context-aware answers.
- **User-friendly Interface**: A frontend for users to interact with the chatbot.

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **Pinecone**: Vector database for storing and retrieving document embeddings.
- **LangChain**: Framework for managing NLP workflows.
- **HuggingFace Embeddings**: Used to generate document embeddings for search.
- **Google Gemini (Flash 1.5)**: AI model used for generating answers based on the retrieved context.
- **Docker**: Containerization (if applicable for deployment).
- **JavaScript, HTML, CSS**: For the frontend interface.

## Installation and Setup

### Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/DattatrayBodake25/medgenie-rag-chatbot.git
cd medgenie-rag-chatbot
```

## Install Dependencies
Install the required Python packages using pip. It's recommended to create a virtual environment before proceeding.
- Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

- Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```

- On Linux/macOS:
```bash
source venv/bin/activate
```

- Install the dependencies:
```bash
pip install -r requirements.txt
```

## Set Up Environment Variables
Create a .env file in the root of the project and add your Pinecone and Google Gemini API keys. Example:
```bash
PINECONE_API_KEY=your_pinecone_api_key
GEMINI_API_KEY=your_google_gemini_api_key
```

Make sure to replace the placeholders with your actual API keys.

## Run the Application
- Start the FastAPI application by running:
```bash
uvicorn backend.main:app --reload
```

This will start the server at http://127.0.0.1:8000. The --reload option allows you to make changes and automatically reload the server.

- Open frontend/index.html in your browser to interact with the chatbot.

## API Endpoints
### The backend exposes two main endpoints:

- 1. /retrieve
### Method: POST

Description: This endpoint retrieves relevant documents based on the query.

### Request Body:

```json
{
  "query": "Your medical query here",
  "top_k": 5
}
```

### Response:

```json
{
  "query": "Your medical query here",
  "retrieved_docs": [
    "Document content 1",
    "Document content 2",
    "Document content 3"
  ]
}
```

- 2. /answer
### Method: POST

Description: This endpoint generates an answer based on the retrieved documents.

Request Body:

```json
{
  "query": "Your medical query here",
  "top_k": 5
}
```

Response:

```json
{
  "answer": "Generated answer based on the retrieved context."
}
```

## Testing
To test the chatbot, simply run the FastAPI server and access the frontend. You can interact with the chatbot and ask medical-related questions. For non-medical greetings like "Hi", "Hello", etc., the chatbot will respond accordingly without attempting to perform a document search.

## Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request. Ensure that your code is well-tested and documented.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

markdown
Copy code

### Explanation of Sections:

1. **Introduction**: Describes what the project is and its purpose.
2. **Features**: Lists out the main features of the chatbot.
3. **Technologies Used**: A brief list of the technologies integrated into the project.
4. **Installation and Setup**: Guides the user through setting up the project on their local machine.
5. **Run the Application**: Explains how to run the backend API and access the frontend.
6. **API Endpoints**: Documents the two main endpoints (`/retrieve` and `/answer`) and how to use them.
7. **Testing**: Explains how users can test the chatbot.
8. **Contributing**: Provides information for potential contributors.
9. **License**: Mentions the license for the project.

This structure should give a clear understanding of the project, how to set it up, and how to co
