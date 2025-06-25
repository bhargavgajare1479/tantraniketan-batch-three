import random
import os
import heapq

CHUNK_SIZE = 10_000_000  # Adjust based on available memory
TEMP_DIR = "temp_chunks"

def generate_random_numbers(filename, count):
    with open(filename, 'w') as f:
        for _ in range(count):
            f.write(f"{random.randint(0, 1_000_000_000)}\n")

def sort_and_save_chunk(numbers, chunk_idx):
    numbers.sort()
    chunk_file = os.path.join(TEMP_DIR, f"chunk_{chunk_idx}.txt")
    with open(chunk_file, 'w') as f:
        for num in numbers:
            f.write(f"{num}\n")
    return chunk_file

def split_and_sort(input_file):
    os.makedirs(TEMP_DIR, exist_ok=True)
    chunk_files = []
    numbers = []
    chunk_idx = 0
    with open(input_file, 'r') as f:
        for line in f:
            numbers.append(int(line.strip()))
            if len(numbers) >= CHUNK_SIZE:
                chunk_files.append(sort_and_save_chunk(numbers, chunk_idx))
                numbers = []
                chunk_idx += 1
        if numbers:
            chunk_files.append(sort_and_save_chunk(numbers, chunk_idx))
    return chunk_files

def merge_chunks(chunk_files, output_file):
    files = [open(chunk, 'r') for chunk in chunk_files]
    heap = []
    for idx, f in enumerate(files):
        num = f.readline()
        if num:
            heapq.heappush(heap, (int(num.strip()), idx))
    with open(output_file, 'w') as out:
        while heap:
            smallest, idx = heapq.heappop(heap)
            out.write(f"{smallest}\n")
            next_num = files[idx].readline()
            if next_num:
                heapq.heappush(heap, (int(next_num.strip()), idx))
    for f in files:
        f.close()

def main():
    INPUT_FILE = "random_numbers.txt"
    OUTPUT_FILE = "sorted_numbers.txt"
    NUMBERS_COUNT = 1_000_000_000  # 1 billion

    # Step 1: Generate random numbers (uncomment to generate)
    # generate_random_numbers(INPUT_FILE, NUMBERS_COUNT)

    # Step 2: Split, sort, and save chunks
    chunk_files = split_and_sort(INPUT_FILE)

    # Step 3: Merge sorted chunks
    merge_chunks(chunk_files, OUTPUT_FILE)

    # Cleanup
    for chunk in chunk_files:
        os.remove(chunk)
    os.rmdir(TEMP_DIR) 

if __name__ == "__main__":
    main()