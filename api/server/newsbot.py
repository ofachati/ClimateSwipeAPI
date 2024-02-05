import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to read JSONL file
def read_jsonl_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# Load the data
filename = '../claims.jsonl'
data = read_jsonl_file(filename)

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
  closest_evidence = data[closest_index]["evidence"]
  return closest_claim, closest_label

# Example user input
user_input = "Are polar bears increasing in number?"
closest_claim, closest_label = find_closest_claim(user_input)
print(f"Closest Match: {closest_claim}\nLabel: {closest_label}\n ")
