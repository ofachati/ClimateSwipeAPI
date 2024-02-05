# routes/chatbot.py

from fastapi import APIRouter
from pydantic import BaseModel
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spellchecker import SpellChecker

# Function to read JSONL file
def read_jsonl_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# Load the data
data = read_jsonl_file('claims.jsonl')

# Extract claims for vectorization
claims = [item["claim"] for item in data]

# Initialize and fit TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(claims)

# Function to find the cl  bbosest claim
def find_closest_claim(user_input):
  # Vectorize the user input
  user_vec = vectorizer.transform([user_input])

  # Calculate cosine similarity
  cos_similarity = cosine_similarity(user_vec, tfidf_matrix)

  # Find the index of the highest similarity score
  closest_index = cos_similarity.argmax()

  # Retrieve the corresponding claim and its label
  closest_claim = data[closest_index]["claim"]
  closest_label = data[closest_index]["claim_label"]

  evidence_sentences = []
  source_references = []
  for evidence in data[closest_index]['evidences']:
    #if evidence['evidence_label'] == "SUPPORTS":
      evidence_sentences.append(evidence['evidence'])
      source_references.append(f"{evidence['article']}:{evidence['evidence_id'].split(':')[1]}")

    # Joining the sentences and sources
  evidences_str = "\n".join(evidence_sentences)
  sources_str = ", ".join(source_references)

  # Concatenating the final string with evidences followed by the sources
  final_str = f"{evidences_str}\nSources: {sources_str}"
  #closest_evidence = data[closest_index]["evidence"]
  return closest_claim, closest_label,final_str

# Example user input
#user_input = "Are polar bears increasing in number?"
#closest_claim, closest_label = find_closest_claim(user_input)
#print(f"Closest Match: {closest_claim}\nLabel: {closest_label}\n ")


router = APIRouter()
spell = SpellChecker()


class ChatMessage(BaseModel):
    message: str

@router.post("/")
async def chat_with_bot(user_message: ChatMessage):
    try:
        # Correct spelling
        corrected_message = " ".join([spell.correction(word) for word in user_message.message.split()])
        # Now use the corrected message to find the closest claim
        closest_claim, closest_label ,evidences= find_closest_claim(corrected_message)
        print(f"Corrected User Message: {corrected_message}")
        print(f"Closest Match: {closest_claim}\nLabel: {closest_label}\n")
        return {"message": f"{evidences}"}
    except Exception as e:
        print(f"An error occurred: {e}")
        # Return a custom error message
        return {"message": "I am not capable of answering this question right now."}
