import requests
import string

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser


def parse_args_func():
    parser = ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        help="Url to get text from",
        default="https://gutenberg.net.au/ebooks01/0100021.txt",
    )

    # parse arguments of command line to get source and destination folder names
    args = parser.parse_args()

    return args.url


def get_text(url):
    try:
        print(f"Start getting text from {url} ...")
        response = requests.get(url)
        response.raise_for_status()  # check for HTTP request error
        return response.text
    except requests.RequestExeption as e:
        return None


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


#  MapReduce function
def map_reduce(text, search_words=None):
    text = remove_punctuation(text)
    words = text.split()

    # if search words is given count only these words
    if search_words:
        words = [word for word in words if word in search_words]

    #  Step 1: parallel mapping
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Step 2: shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Step 3: parallel reduction
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def count_key_words(url, search_words, url_from_args=False):
    if url_from_args:
        url = parse_args_func()
    text = get_text(url)

    if text:
        print("Processing...")
        # MapReduce execution
        result = map_reduce(text, search_words)

        return result
    else:
        print("Error: couldn't get initial text")
        return None


if __name__ == "__main__":
    # url to get text from
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    # key words for search
    search_words = ["war", "peace", "love"]
    result = count_key_words(url, search_words)
    print("Result of words count: ", result)
