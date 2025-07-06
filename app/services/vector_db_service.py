import faiss
import numpy as np
import os
import json

VECTOR_DIM = 384 
INDEX_PATH = "app/vector_db/faiss_index.bin"
META_PATH = "app/vector_db/metadata.jsonl"

os.makedirs("app/vector_db", exist_ok=True)

if os.path.exists(INDEX_PATH):
    try:
        index = faiss.read_index(INDEX_PATH)
    except:
        print("인덱스 손상 감지, 새로 생성")
        index = faiss.IndexFlatL2(VECTOR_DIM)
else:
    index = faiss.IndexFlatL2(VECTOR_DIM)

metadata = []
if os.path.exists(META_PATH):
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = [json.loads(line) for line in f]


def add_vector(vector: list, meta: dict):
    vec_np = np.array([vector], dtype="float32")
    index.add(vec_np)
    metadata.append(meta)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")


def search_vector(query_vector: list, top_k=3):
    vec_np = np.array([query_vector], dtype="float32")
    D, I = index.search(vec_np, top_k)

    results = []
    for idx in I[0]:
        if idx < len(metadata):
            results.append(metadata[idx])

    return results

def get_index():
    return index

def get_all_articles():
    return metadata