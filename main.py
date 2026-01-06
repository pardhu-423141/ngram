from read import tokenize_text
from train import train
import pickle

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
        print(context_len,context)
        if context in grams[context_len]:
            next_words = grams[context_len][context]
            word = max(next_words, key=next_words.get)
            return "." if word == "</s>" else word

    # Unigram fallback
    unigram = grams[0]
    word = max(unigram, key=unigram.get)
    return "." if word == "</s>" else word

def test():
    n = int(input("No of sentences: "))
    print(grams[4][('the','day','was','very')])
    print(grams[1][('very')])
    for _ in range(n):
        s = input()
        tokenized = tokenize_text(s)
        tokens = tokenized[0][:-1]     
        next_word = find_next_word(tokens)
        print(s + " " + next_word)

if __name__ == "__main__":
    do_train = 0
    extract()
    if do_train:
        train()
    test()
