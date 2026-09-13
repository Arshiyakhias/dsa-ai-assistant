import json
import os

INPUT_FILE = "data/book.json"
OUTPUT_FILE = "data/chunks.json"

# Load the scraped textbook
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    book = json.load(file)

chunks = []

# Number of words in each chunk
chunk_size = 1000

for chapter in book:

    text = chapter["content"]

    # Convert the chapter text into words
    words = text.split()

    # Create chunks of approximately 1000 words
    for i in range(0, len(words), chunk_size):

        chunk_text = " ".join(words[i:i + chunk_size])

        chunks.append({
            "chunk_id": len(chunks),
            "chapter_number": chapter["chapter_number"],
            "chapter_title": chapter["title"],
            "url": chapter["url"],
            "text": chunk_text
        })

print(f"Created {len(chunks)} chunks.")

# Make sure data folder exists
os.makedirs("data", exist_ok=True)

# Save chunks
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(chunks, file, indent=2, ensure_ascii=False)

print(f"Saved chunks to {OUTPUT_FILE}")