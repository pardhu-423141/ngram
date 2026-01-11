from read import tokenize_text
from train import train
import pickle
import os
from fetch_book_id import fetch
grams = []

def extract():
    files = [
        "ngrams/unigrams.pkl",   
        "ngrams/bigrams.pkl",    
        "ngrams/trigrams.pkl",   
        "ngrams/fourgrams.pkl",  
        "ngrams/fivegrams.pkl"   
    ]
    for file in files:
        with open(file, "rb") as f:
            grams.append(pickle.load(f))

def find_next_word(tokens):
    max_context = min(4, len(tokens))

    for context_len in range(max_context, 0, -1):
        context = tuple(tokens[-context_len:])
        if context in grams[context_len]:
            next_words = grams[context_len][context]
            word = max(next_words, key=next_words.get)
            return "." if word == "</s>" else " "+word

    unigram = grams[0]
    word = max(unigram, key=unigram.get)
    return "." if word == "</s>" else word

def test():
    n = int(input("No of sentences: "))
    
    with open("output.txt", "w", encoding="utf-8") as f:
        for _ in range(n):
            s = input("sentence : ")
            f.write(f"sentence : {s}\n")
            tokenized = tokenize_text(s)
            tokens = tokenized[-1][:-1]     
            next_word = find_next_word(tokens)
            f.write(f"Predicted word : {next_word}\n")
            f.write(f"Output sentence: {s + ("." if next_word == "." else next_word)}\n\n")
            print(s + ("." if next_word == "." else next_word))

if __name__ == "__main__":
    do_train = 0
    if not os.path.isfile("jane_austen_book_ids.txt"):
        print()
        fetch()
    if do_train:
        print("Training the model...")
        train()
    print("Loading the model...")
    extract()
    print("Model loaded.")
    test()
