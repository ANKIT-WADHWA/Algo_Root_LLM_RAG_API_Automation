# 🚀 LLM + RAG-Powered Automation API

## 📌 Overview
This project is a Python-based API service that dynamically retrieves and executes automation functions using **LLM + RAG (Retrieval-Augmented Generation)**. It processes user prompts, maps them to predefined automation functions, and generates executable Python code for function invocation.

## 🛠 Features
- **Function Registry**: Predefined automation functions like opening apps, retrieving system stats, and running shell commands.
- **LLM + RAG for Function Retrieval**: Uses a vector database (ChromaDB) to map user prompts to the best-matching function.
- **Dynamic Code Generation**: Generates Python scripts for execution based on retrieved functions.
- **Session-based Context**: Enhances retrieval accuracy by maintaining session memory.
- **Direct Execution Option**: Allows executing the retrieved function directly from the API.

## 🚀 Installation & Setup
### 1️⃣ Clone the Repository
```sh
$ git clone https://github.com/your-username/AlgoRoot-automation-api.git
$ cd AlgoRoot-automation-api
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
$ pip install -r requirements.txt
```

### 3️⃣ Run the API Server
```sh
$ uvicorn main:app --reload
```

## 📡 API Endpoints
### 🔹 Execute an Automation Function
#### **Request:**
```http
POST /execute
```
##### **Request Body:**
```json
{
  "prompt": "Open calculator",
  "session_id": "user123"
}
```
#### **Response:**
```json
{
  "function": "open_calculator",
  "code": "from automation_functions import open_calculator\ndef main():\n    try:\n        open_calculator()\n        print(\"Calculator opened successfully.\")\n    except Exception as e:\n        print(f\"Error executing function: {e}\")\nif __name__ == \"__main__\":\n    main()",
}
```


## 📷 Screenshots
### 1️⃣ Opening Chrome Browser
![Postman Request](screenshots/1.png)

### 2️⃣ List files and directories in specified path
![Terminal Output](screenshots/2.png)