import os
import logging
import inspect
import chromadb
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import automation_functions  # Importing function file
from code_generator import generate_code  # Ensure this file exists

# ✅ Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Load Sentence Transformer model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./function_db")
collection = chroma_client.get_or_create_collection(name="functions")

# ✅ Fetch available functions dynamically
def get_available_functions():
    """Retrieves all available functions in automation_functions.py."""
    return {name: func for name, func in inspect.getmembers(automation_functions, inspect.isfunction)}

ALLOWED_FUNCTIONS = get_available_functions()
logging.info(f"✅ Loaded Functions: {list(ALLOWED_FUNCTIONS.keys())}")

# ✅ Function to clear old function records and store new ones in ChromaDB
def clear_and_store_functions():
    function_names = list(ALLOWED_FUNCTIONS.keys())  # Get function names
    
    # ✅ Delete old embeddings
    try:
        existing_records = collection.get()["ids"]
        if existing_records:
            collection.delete(ids=existing_records)  # Delete old embeddings
            logging.info(f"🗑️ Deleted {len(existing_records)} old records from ChromaDB.")
    except Exception as e:
        logging.warning(f"⚠️ No existing records found to delete: {str(e)}")

    # ✅ Encode and store new functions
    function_embeddings = embedding_model.encode(function_names).tolist()
    collection.add(ids=function_names, embeddings=function_embeddings)
    
    logging.info(f"🔄 Stored {len(function_names)} functions in the database.")

# ✅ Run function at startup
clear_and_store_functions()

# ✅ Session Memory for Context Retention
session_memory = {}

# ✅ API Request Models
class FunctionRequest(BaseModel):
    prompt: str
    session_id: str
    params: dict = None  # ✅ Optional parameters for function execution

class MultiFunctionRequest(BaseModel):
    prompts: list[str]
    session_id: str

# ✅ Similarity Threshold for Function Matching
SIMILARITY_THRESHOLD = 0.45

# ✅ Retrieve Best Matching Function
def retrieve_best_function(prompt: str, session_id: str):
    """Retrieve the best function using similarity search and session history."""
    embedding = embedding_model.encode(prompt).tolist()

    # Store session history
    session_memory.setdefault(session_id, [])
    if prompt not in session_memory[session_id]:
        session_memory[session_id].append(prompt)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=1,
        include=["distances"]
    )

    if not results or not results["ids"] or not results["ids"][0]:
        logging.warning("⚠️ No matching function found in the database.")
        return None

    best_match_id = results["ids"][0][0]
    best_match_score = results["distances"][0][0]

    logging.info(f"🔍 Best match: {best_match_id} (Score: {best_match_score})")

    if best_match_score > SIMILARITY_THRESHOLD:
        logging.warning("⚠️ No function meets the similarity threshold.")
        return None  

    return best_match_id

# ✅ Secure Function Execution
def execute_function(function_name: str, params: dict = None):
    """Executes the matched function with optional parameters."""
    try:
        if function_name not in ALLOWED_FUNCTIONS:
            logging.error(f"⛔ Unauthorized function access attempt: {function_name}")
            raise ValueError("Unauthorized function access")

        # Execute function with optional parameters
        if params:
            result = ALLOWED_FUNCTIONS[function_name](**params)
        else:
            result = ALLOWED_FUNCTIONS[function_name]()

        return result if result else "Executed Successfully"
    
    except TypeError as e:
        logging.error(f"⚠️ Error: Function {function_name} requires parameters. {str(e)}")
        return f"Error: Function {function_name} requires parameters."
    except Exception as e:
        logging.error(f"❌ Error executing function {function_name}: {str(e)}")
        return str(e)

# ✅ API Endpoint for Single Execution
@app.post("/execute")
async def execute(request: FunctionRequest):
    logging.info(f"📩 Received request: {request.prompt}, Session ID: {request.session_id}")
    
    function_name = retrieve_best_function(request.prompt, request.session_id)
    if not function_name:
        raise HTTPException(status_code=404, detail="No matching function found")

    output = execute_function(function_name, request.params)  # ✅ Pass parameters
    generated_code = generate_code(function_name)

    response = {
        "function": function_name,
        "output": output,
        "code": generated_code,
        "session_history": session_memory.get(request.session_id, [])
    }

    logging.info(f"✅ Executed: {function_name}, Output: {output}")
    return response

# ✅ API Endpoint for Multi-Step Execution
@app.post("/execute_multiple")
async def execute_multiple(request: MultiFunctionRequest):
    logging.info(f"📩 Received multiple prompts: {request.prompts}, Session ID: {request.session_id}")

    results = []
    for prompt in request.prompts:
        function_name = retrieve_best_function(prompt, request.session_id)
        if function_name:
            output = execute_function(function_name)
            generated_code = generate_code(function_name)
            results.append({
                "function": function_name,
                "output": output,
                "code": generated_code
            })
        else:
            results.append({
                "function": None,
                "output": "No matching function found",
                "code": None
            })

    return {
        "session_history": session_memory.get(request.session_id, []),
        "results": results
    }

# ✅ Run API
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
