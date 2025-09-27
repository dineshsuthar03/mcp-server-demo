import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()  # make sure .env is loaded

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

MODEL = os.getenv("AZURE_OPENAI_MODEL")
