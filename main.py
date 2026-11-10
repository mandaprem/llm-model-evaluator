import os
from dotenv import load_dotenv
from groq import Groq
import json
import time 
import statistics

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

def call(model_name, prompt):

    start_time = time.perf_counter()
    response = client.chat.completions.create(
    model=model_name,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
    latency = time.perf_counter() - start_time

    answer = response.choices[0].message.content

    usage = response.usage

    result = {
        "model":response.model,
        "answer": answer,
        "latency": latency,
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens 
    }

    return result

test_cases = [
    {
        "question": "What is 5 + 5?",
        "expected_answer": "10"
    },
    {
        "question": "What is the capital of India?",
        "expected_answer": "New Delhi"
    },
    {
        "question": "Which programming language is commonly used for AI?",
        "expected_answer": "Python"
    }
]

def evaluate_answer(actual, expected):

    actual = " ".join(actual.strip().lower().split())
    expected = " ".join(expected.strip().lower().split())

    return expected in actual


# Models to compare
models = [
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b"
]

# Same prompt for both models
prompt = "Explain what an LLM is in simple words."

# Number of trials
trials = 3

# Test each model
# for model in models:

#     latencies = []

#     print(f"\nTesting Model: {model}")

#     for i in range(trials):

#         result = call(model, prompt)

#         latency = result["latency"]

#         latencies.append((latency))

#         print(f"Trial {i + 1}: {latency:.3f} seconds")

#     # Calculate average
#     average_latency = statistics.mean(latencies)

#     print(f"\nAverage Latency: {average_latency:.3f} seconds")

# actual = "The capital of India is New Delhi."
# expected = "New Delhi"

# print(evaluate_answer(actual, expected))

correct_answers = 0
total_questions = len(test_cases)
for model in models:

    print(f"\n========== Model: {model} ==========")

    correct_answers = 0
    total_questions = len(test_cases)

    for test in test_cases:

        question = test["question"]
        expected = test["expected_answer"]

        result = call(model, question)
        actual = result["answer"]

        accuracy = evaluate_answer(actual, expected)

        if accuracy:
            correct_answers += 1

        # print("\nQuestion:", question)
        # print("Expected:", expected)
        # print("Actual:", actual)
        # print("Correct:", accuracy)
        print(f"Question {test_cases.index(test) + 1}: {'PASS' if accuracy else 'FAIL'}")

    accuracy_percentage = (
        correct_answers / total_questions
    ) * 100

    print("\nModel Accuracy:", accuracy_percentage, "%")