import chromadb
from chromadb.utils import embedding_functions
import uuid

# Use ChromaDB's built-in sentence transformer (downloads once, works offline after)
# If that also fails, we fall back to ChromaDB's default embedding
print("Setting up ChromaDB...")

chroma_client = chromadb.Client()

# Use chromadb's default embedding function (no separate download needed!)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

print("ChromaDB ready! ✅")


def get_or_create_collection(collection_name: str = "pdf_chunks"):
    return chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )


def store_chunks(chunks: list[str], collection_name: str = "pdf_chunks"):
    """Convert chunks to embeddings and store in ChromaDB"""

    # Clear old data
    try:
        chroma_client.delete_collection(name=collection_name)
        print("Cleared old collection ✅")
    except:
        pass

    collection = get_or_create_collection(collection_name)

    print(f"Embedding {len(chunks)} chunks... ⏳")

    ids = [str(uuid.uuid4()) for _ in chunks]

    # ChromaDB handles embedding automatically!
    collection.add(
        documents=chunks,
        ids=ids
    )

    print(f"Stored {len(chunks)} chunks ✅")
    return collection


def search_similar_chunks(query: str, collection_name: str = "pdf_chunks", top_k: int = 5) -> list[str]:
    """Find most relevant chunks for a question"""

    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_texts=[query],  # ChromaDB embeds this automatically
        n_results=top_k
    )

    chunks = results["documents"][0]
    print(f"Found {len(chunks)} relevant chunks ✅")
    return chunks