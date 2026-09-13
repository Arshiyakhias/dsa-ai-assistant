import os
from dotenv import load_dotenv
from openai import OpenAI


# Load the API key from .env
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Test text
text = """
An algorithm is an explicit sequence of instructions,
performed on data, to accomplish a desired objective.
"""


# Create an embedding for the text
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)


# Get the embedding vector
embedding = response.data[0].embedding


# Display the result
print("Embedding created successfully!")
print("Number of dimensions:", len(embedding))

print("First 10 values:")
print(embedding[:10])