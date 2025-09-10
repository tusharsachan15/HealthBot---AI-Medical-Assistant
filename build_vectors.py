from utils.rag import build_vector_store

if __name__ == "__main__":
    vector_store = build_vector_store()
    print("Vector store created successfully at data/vector_store/vector_store.pkl")
