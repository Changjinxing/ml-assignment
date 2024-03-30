import random
import subprocess
import time
import torch


def md5(text: str):
    import hashlib
    return hashlib.md5(text.encode()).hexdigest()


def min_memory_used_index(num_gpus, threshold=100):
    # sleep random [1000, 5000] ms
    start = time.time()
    random_sleep_s = random.randint(1000, 5000) / 1000.0
    time.sleep(random_sleep_s)
    end = time.time()
    duration = end - start

    # Execute nvidia-smi command
    result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,nounits,noheader'],
                            capture_output=True, text=True)

    # Split the output by newline characters
    used_memory_values = result.stdout.strip().split('\n')

    more_than_half = sum(int(value) < 100 for value in used_memory_values) >= len(used_memory_values) / 2
    if more_than_half:
        random_gpu_index = torch.randint(0, num_gpus, (1,))
        return random_gpu_index.item(), "Random"

    # Parse the used memory values
    # used_memory_gb = [int(value) / 1024 for value in used_memory_values]
    used_memory_gb = [int(value) for value in used_memory_values]

    # Calculate the total number of GPUs
    num_gpus = len(used_memory_gb)

    # Calculate the average memory usage per GPU
    # average_memory_gb = sum(used_memory_gb) / num_gpus

    # Find the GPU with the highest memory usage
    min_memory_index = used_memory_gb.index(min(used_memory_gb))
    print(
        f"[min_memory_used_index]sleep random secodes: {random_sleep_s}, start: {start}, end: {end}, duration: {duration}, gpu: {min_memory_index}, used_memory_gb: {used_memory_gb}")
    return min_memory_index, "Min Memory Used"
