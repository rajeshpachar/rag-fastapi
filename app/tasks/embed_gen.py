# https://medium.com/@akriti.upadhyay/implementing-rag-with-langchain-and-hugging-face-28e3ea66c5f7

import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings


def build_googleai_embeddings(docs):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print(len(docs))
    for idx, doc in enumerate(docs):
        vector = embeddings.embed_query(doc)
        yield idx, vector

def build_openai_embeddings(docs):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    for doc in docs:
        vector = embeddings.embed_query(doc)
        yield vector


def build_MiniLM_embeddings(docs):
    # Define the path to the pre-trained model you want to use
    modelPath = "sentence-transformers/all-MiniLM-l6-v2"

    # Create a dictionary with model configuration options, specifying to use the CPU for computations
    model_kwargs = {'device':'cpu'}

    # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
    encode_kwargs = {'normalize_embeddings': False}

    # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,     # Provide the pre-trained model's path
        model_kwargs=model_kwargs, # Pass the model configuration options
        encode_kwargs=encode_kwargs # Pass the encoding options
    )
    for doc in docs:
        vector = embeddings.embed_query(doc)
        yield vector

