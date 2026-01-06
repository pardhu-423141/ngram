import requests
import re
import time

# ---------------------------------
# Fetch book text safely
# ---------------------------------
def fetch_book_text(book_id, retries=3):
    urls = [
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
    ]

    for url in urls:
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=20, stream=True)
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt == retries - 1:
                    print(f"❌ Failed {book_id} from {url}")
                time.sleep(1)

    return None


# ---------------------------------
# Remove Gutenberg header/footer
# ---------------------------------
def remove_gutenberg_metadata(text):
    if not text:
        return None

    start = "*** START OF"
    end = "*** END OF"

    if start in text and end in text:
        text = text.split(start, 1)[1]
        text = text.split(end, 1)[0]

    return text.strip()


# ---------------------------------
# Skip front matter
# ---------------------------------
def skip_front_matter(text):
    chapter_pattern = re.compile(
        r'\b(chapter\s+(one|\d+|i+)|act\s+i)\b',
        re.IGNORECASE
    )

    match = chapter_pattern.search(text)
    if match:
        return text[match.start():]

    return text


# ---------------------------------
# Tokenization
# ---------------------------------
def tokenize_text(text):
    text = text.lower()
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    tokenized = []
    for s in sentences:
        words = s.split()
        tokenized.append(['<s>'] + words + ['</s>'])

    return tokenized


# ---------------------------------
# Read book list
# ---------------------------------
def read_books_file(path):
    books = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                books.append((parts[0], parts[1]))
    return books


# ---------------------------------
# MAIN FUNCTION (SAFE)
# ---------------------------------
def build_tokenized_corpus(book_file):
    all_tokenized = []

    books = read_books_file(book_file)

    for book_id, title in books:
        print(f"Processing: {title} ({book_id})")

        raw = fetch_book_text(book_id)
        if not raw:
            print(f"⚠ Skipping {title}")
            continue

        clean = remove_gutenberg_metadata(raw)
        content = skip_front_matter(clean)
        tokenized = tokenize_text(content)

        all_tokenized.extend(tokenized)

    return all_tokenized
