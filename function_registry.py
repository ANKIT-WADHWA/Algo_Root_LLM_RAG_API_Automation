import chromadb
import inspect
import automation_functions
from sentence_transformers import SentenceTransformer

# ✅ Load Sentence Transformer model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./function_db")
collection = chroma_client.get_or_create_collection(name="functions")

# ✅ Clear previous function entries to avoid duplication
existing_ids = collection.get()["ids"]
if existing_ids:
    collection.delete(ids=existing_ids)

# ✅ Automatically fetch available functions from automation.py
FUNCTIONS = {
    name: func.__doc__ or "No description available"
    for name, func in inspect.getmembers(automation, inspect.isfunction)
}

# ✅ Store function embeddings in ChromaDB
for function_name, description in FUNCTIONS.items():
    embedding = embedding_model.encode(description).tolist()
    collection.add(
        ids=[function_name],
        embeddings=[embedding],
        metadatas=[{"description": description}]
    )

print("✅ Function embeddings stored successfully!")
