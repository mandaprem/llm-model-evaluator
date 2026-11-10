from groq import Groq
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client

client = Groq()

# Fetch and print all active model IDs available to your account
models = client.models.list()
for model in models.data:
    print(model.id)