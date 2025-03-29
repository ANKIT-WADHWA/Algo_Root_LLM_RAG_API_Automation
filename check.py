import chromadb

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./function_db")
collection = chroma_client.get_or_create_collection(name="functions")

# Get all stored function IDs
stored_functions = collection.get()

# Print stored function IDs
print("Stored function IDs:", stored_functions["ids"])
