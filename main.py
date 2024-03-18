import asyncio
from count_key_words import count_key_words
from visualize_top_words import visualize_top_words
from async_files_sorting import parse_args_func, read_folder


def main():
    # # task 1
    # source_path, destination_path = parse_args_func()

    # asyncio.run(read_folder(source_path, destination_path))

    # task 2
    result = count_key_words("", None, True)

    visualize_top_words(result)


if __name__ == "__main__":
    main()
