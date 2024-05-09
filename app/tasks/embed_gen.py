# https://medium.com/@akriti.upadhyay/implementing-rag-with-langchain-and-hugging-face-28e3ea66c5f7

import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings


# models/text-embedding-004  models/embedding-001
gai_embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
# text-embedding-3-small text-embedding-3-large text-embedding-ada-002
# https://openai.com/api/pricing/
oai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# vector size is 768
def build_googleai_embeddings(docs):
    for idx, doc in enumerate(docs):
        vector = gai_embeddings.embed_query(doc)
        yield idx, vector

# vector size 3072 , 1536
def build_openai_embeddings(docs):
    for idx, doc in enumerate(docs):
        vector = oai_embeddings.embed_query(doc)
        yield idx, vector

# from langchain.embeddings import HuggingFaceEmbeddings

# def  create_huggingface_embeddings_model() :
#      # Define the path to the pre-trained model you want to use
#     modelPath = "sentence-transformers/all-MiniLM-l6-v2"

#     # Create a dictionary with model configuration options, specifying to use the CPU for computations
#     model_kwargs = {'device':'cpu'}

#     # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
#     encode_kwargs = {'normalize_embeddings': False}

#     # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
#     embeddings = HuggingFaceEmbeddings(
#         model_name=modelPath,     # Provide the pre-trained model's path
#         model_kwargs=model_kwargs, # Pass the model configuration options
#         encode_kwargs=encode_kwargs # Pass the encoding options
#     )
#     return embeddings

# hugging_embeddings = create_huggingface_embeddings_model()


# # vector size 384
# def build_MiniLM_embeddings(docs):
#     for idx, doc in enumerate(docs):
#         vector = hugging_embeddings.embed_query(doc)
#         yield idx, vector