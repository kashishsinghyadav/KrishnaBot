import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load Bhagavad Gita JSON Data
with open("gita_data.json", "r", encoding="utf-8") as f:
    gita_data = json.load(f)

# Initialize Hugging Face Embedding Model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Prepare Data for FAISS
verse_texts = []
verse_mappings = []
for chapter, verses in gita_data.items():
    for verse_num, verse_text in verses.items():
        verse_texts.append(f"{chapter} - {verse_num}: {verse_text}")
        verse_mappings.append((chapter, verse_num, verse_text))

# Debug: Check if verse_texts is populated
print(f"Total Verses Loaded: {len(verse_texts)}")
if not verse_texts:
    raise ValueError("No verses found! Check your gita_data.json file.")

# Convert Verses to Embeddings
embeddings = model.encode(verse_texts)

# Debug: Check embedding shape
if embeddings is None or len(embeddings) == 0:
    raise ValueError("Embeddings failed! No data encoded.")

print(f"Embeddings Shape: {embeddings.shape}")

# Ensure embeddings is in the correct format for FAISS
embeddings = np.array(embeddings).astype("float32")

# Create FAISS Index & Store Embeddings
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS Index
faiss.write_index(index, "gita_faiss.index")

# Save Verse Mappings
with open("verse_mappings.json", "w", encoding="utf-8") as f:
    json.dump(verse_mappings, f, indent=4, ensure_ascii=False)

print("Verses stored in FAISS successfully!")
