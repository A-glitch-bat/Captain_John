from llama_cpp import Llama

# Load the model (adjust the path to match your setup)
llm = Llama(
    model_path="../models/your-model.gguf",  # relative to your Flask script
    n_ctx=512,       # context window
    n_threads=4      # adjust based on Pi performance
)

# Generate a response
output = llm("Q: What is the capital of France?\nA:", max_tokens=50)
print(output["choices"][0]["text"])
