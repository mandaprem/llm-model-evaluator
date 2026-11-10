def call(model_name, prompt):

    start_time = time.pref_counter()
    response = client.chat.completions.create(
    model=model_name,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
    latency = time.pref_counter() - start_time

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