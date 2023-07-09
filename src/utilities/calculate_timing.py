import io
from utilities.token_helper import num_tokens_from_string
from shared.constants import LLAMA_TIMINGS_FILE

def calculate_average_timings(file_path):
    with io.open(file_path, "r") as file:
        timings = []
        total_tokens = 0
        text = file.read()


        # Parse the debug text and extract the relevant information
        for line in text.split("\n"):
            if line.startswith("Query Tokens: "):
                tokens = line.split()
                num_tokens = int(tokens[2])
                total_tokens = total_tokens + num_tokens

            elif "total time" in line:
                tokens = line.split()
                total_time = float(tokens[4])                
                timings.append(total_time)

        # Calculate the average ms per token 
        average_time_per_token = sum(timings) / total_tokens

    return average_time_per_token

def convert_milliseconds_to_english(milliseconds):
    seconds = int((milliseconds / 1000) % 60)
    minutes = int((milliseconds / (1000 * 60)) % 60)
    hours = int((milliseconds / (1000 * 60 * 60)) % 24)
    milliseconds = int(milliseconds % 1000)

    result = ""
    if hours > 0:
        result += f"{hours} hour{'s' if hours > 1 else ''} "
    if minutes > 0:
        result += f"{minutes} minute{'s' if minutes > 1 else ''} "
    if seconds > 0:
        result += f"{seconds} second{'s' if seconds > 1 else ''} "
    if milliseconds > 0:
        result += f"{milliseconds} millisecond{'s' if milliseconds > 1 else ''}"

    return result.strip()

def calculate_total_processing_time_from_docs(docs) -> float:
    """calculate the time it will take to process the given text, using averages from the llama timings"""
    total_time = 0
    for doc in docs:
        total_time += calculate_total_processing_time_from_text(doc.page_content)

    return total_time

def calculate_total_processing_time_from_tokens(num_tokens:int) -> float:
    average_time_per_token = calculate_average_timings(LLAMA_TIMINGS_FILE)
    # print(f"Reading {LLAMA_TIMINGS_FILE} looks like the average time per token on this system is: {average_time_per_token}")
    total_processing_time = num_tokens * average_time_per_token
    return total_processing_time

def calculate_total_processing_time_from_text(text:str) -> float:
    expected_tokens = num_tokens_from_string(text)

    total_processing_time = calculate_total_processing_time_from_tokens(expected_tokens)

    return total_processing_time

