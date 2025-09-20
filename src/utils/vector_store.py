from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

VECTOR_STORE_PATH = 'faiss_index.bin'
DOCS_PATH = 'vector_docs.pkl'
model = SentenceTransformer('all-MiniLM-L6-v2')


async def ingest_docs(new_docs):
    """Add new documents to the vector store asynchronously."""
    if os.path.exists(DOCS_PATH):
        with open(DOCS_PATH, 'rb') as f:
            docs = pickle.load(f)
    else:
        docs = []
    docs.extend(new_docs)
    embeddings = await asyncio.get_event_loop().run_in_executor(None, model.encode, docs)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    faiss.write_index(index, VECTOR_STORE_PATH)
    with open(DOCS_PATH, 'wb') as f:
        pickle.dump(docs, f)

async def retrieve_similar(query):
    if not os.path.exists(VECTOR_STORE_PATH) or not os.path.exists(DOCS_PATH):
        raise ValueError("Vector store not initialized. Ingest documents first.")
    index = faiss.read_index(VECTOR_STORE_PATH)
    with open(DOCS_PATH, 'rb') as f:
        docs = pickle.load(f)
    q_emb = await asyncio.get_event_loop().run_in_executor(None, model.encode, [query])
    D, I = index.search(np.array(q_emb), k=1)
    return docs[I[0][0]]
