import matplotlib.pyplot as plt
from collections import Counter


def visualize_top_words(words, top_n=10):
    if words and isinstance(words, dict):
        top_n = len(words.keys()) if len(words.keys()) < top_n else top_n
    # get top_n number of words
    top_words = Counter(words).most_common(top_n)

    # make dict
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 8))
    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title(f"Top {top_n} most frequent words")
    plt.gca().invert_yaxis()
    plt.show()
