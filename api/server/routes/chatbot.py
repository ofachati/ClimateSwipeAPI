from fastapi import APIRouter
from pydantic import BaseModel
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from gensim import corpora, models, similarities
from spellchecker import SpellChecker
import os

def read_jsonl_file(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)
    with open(filepath, 'r') as f:
        data = [json.loads(line) for line in f]
    return data

data = read_jsonl_file('claims.jsonl')

# Flatten the data to extract all evidences
evidences = []
for item in data:
    for evidence in item["evidences"]:
        evidences.append((evidence["evidence"], evidence["evidence_label"], evidence["article"], evidence["evidence_id"]))

# Extract evidence texts for vectorization
evidence_texts = [evidence[0] for evidence in evidences]

# Initialize and fit TF-IDF vectorizer to evidences
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(evidence_texts)

# Convert evidences to a list of tokenized words
evidence_tokenized = [evidence.split() for evidence in evidence_texts]

# Build the dictionary and corpus for evidences
dictionary = corpora.Dictionary(evidence_tokenized)
corpus = [dictionary.doc2bow(evidence) for evidence in evidence_tokenized]

# Build the TF-IDF model for evidences
tfidf_model = models.TfidfModel(corpus)

# Compute TF-IDF matrix for the entire corpus of evidences
corpus_tfidf = tfidf_model[corpus]

# Build the index for soft cosine similarity for evidences
index = similarities.SparseMatrixSimilarity(corpus_tfidf, num_features=len(dictionary))


def find_closest_evidence(user_input, similarity_threshold=0.1):  # Example threshold
  user_vec_bow = dictionary.doc2bow(user_input.split())
  user_vec_tfidf = tfidf_model[user_vec_bow]
  soft_cos_similarity = index[user_vec_tfidf]
  max_similarity = np.max(soft_cos_similarity)

  if max_similarity < similarity_threshold:
    return None, None  # Indicate no close evidence found

  closest_index = np.argmax(soft_cos_similarity)
  closest_evidence, _, _, evidence_id = evidences[closest_index]
  article_name = evidence_id.split(":")[0].replace(" ", "_")
  wikipedia_url = f"https://en.wikipedia.org/wiki/{article_name}"
  return closest_evidence, wikipedia_url


router = APIRouter()
spell = SpellChecker()


class ChatMessage(BaseModel):
  message: str

@router.post("/")
async def chat_with_bot(user_message: ChatMessage):
    try:
        corrected_message = " ".join([spell.correction(word) for word in user_message.message.split()])
        closest_evidence, wikipedia_url = find_closest_evidence(corrected_message)

        if closest_evidence is None:  # Check if no evidence meets the threshold
            # Adjusted response for no relevant evidence found
            return {
                "message": "Sorry, I couldn't find any information related to your query. 😔",
                "source_name": None,
                "source_link": None
            }

        # Use the evidence ID as the source name
        evidence_id = evidences[np.argmax(index[dictionary.doc2bow(corrected_message.split())])][3]
        article_name = evidence_id.split(":")[0].replace(" ", "_")

        # Construct and return the response object
        return {
            "message": closest_evidence,
            "source_name": evidence_id,
            "source_link": wikipedia_url
        }
    except Exception as e:
        # Adjusted catch-all response to match the new object structure
        return {
            "message": "Sorry, I am still a simple AI.. I am not capable of answering this question 😔.",
            "source_name": None,
            "source_link": None
        }
