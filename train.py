from read import build_tokenized_corpus
from collections import Counter, defaultdict
import pickle
import os

def train():
    os.makedirs("ngrams", exist_ok=True)

    
    tokenized = build_tokenized_corpus("jane_austen_book_ids.txt")

    unigrams = Counter()
    bigrams = defaultdict(Counter)
    trigrams = defaultdict(Counter)
    fourgrams = defaultdict(Counter)
    fivegrams = defaultdict(Counter)

    for sentence in tokenized:
        n = len(sentence)
        for i in range(n):
            unigrams[sentence[i]] += 1

            if i + 1 < n:
                bigrams[(sentence[i],)][sentence[i+1]] += 1
            if i + 2 < n:
                trigrams[(sentence[i], sentence[i+1])][sentence[i+2]] += 1
            if i + 3 < n:
                fourgrams[(sentence[i], sentence[i+1], sentence[i+2])][sentence[i+3]] += 1
            if i + 4 < n:
                fivegrams[(sentence[i], sentence[i+1], sentence[i+2], sentence[i+3])][sentence[i+4]] += 1

    
    pickle.dump(unigrams, open("ngrams/unigrams.pkl", "wb"))
    pickle.dump(bigrams, open("ngrams/bigrams.pkl", "wb"))
    pickle.dump(trigrams, open("ngrams/trigrams.pkl", "wb"))
    pickle.dump(fourgrams, open("ngrams/fourgrams.pkl", "wb"))
    pickle.dump(fivegrams, open("ngrams/fivegrams.pkl", "wb"))

    print("N-gram counts saved successfully.")
