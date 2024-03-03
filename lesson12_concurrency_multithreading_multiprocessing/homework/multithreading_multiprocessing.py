import multiprocessing
import os
import threading
import time
from pathlib import Path

import requests


# CPU-bound task (heavy computation)
def encrypt_file(path: Path):
    print(f"Processing file from {path} in process {os.getpid()}")
    _ = [i for i in range(100_000_000)]


def measure_encryption_performance(path):
    start_time = time.perf_counter()
    encrypt_file(path)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f"Time taken for encryption task: {time_taken} seconds")
    return time_taken


# I/O-bound task (downloading image from URL)
def download_image(image_url):
    print(
        f"Downloading image from {image_url} in thread {threading.current_thread().name}"
    )
    response = requests.get(image_url)
    with open("image.jpg", "wb") as f:
        f.write(response.content)


def measure_download_performance(image_url):
    start_time = time.perf_counter()
    download_image(image_url)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f"Time taken for download task: {time_taken} seconds")
    return time_taken


if __name__ == "__main__":
    try:
        start_time = time.perf_counter()

        file_path = Path("rockyou.txt")

        download_thread = threading.Thread(
            target=measure_download_performance,
            args=("https://picsum.photos/1000/1000",),
        )
        download_thread.start()

        encrypt_process = multiprocessing.Process(
            target=measure_encryption_performance, args=(file_path,)
        )
        encrypt_process.start()

        download_thread.join()
        encrypt_process.join()

        end_time = time.perf_counter()

        total_time = end_time - start_time
        print(f"Total time: {total_time} seconds")

    except Exception as e:
        print(f"Error occurred: {e}")
