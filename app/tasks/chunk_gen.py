# https://medium.com/@tejpal.abhyuday/retrieval-augmented-generation-rag-from-basics-to-advanced-a2b068fd576c

from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_char_text_chunks(text, chunk_size=512, chunk_overlap=24):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks


from langchain.text_splitter import SpacyTextSplitter

def get_spacy_text_chunks(text, chunk_size=512, chunk_overlap=24):
    text_splitter = SpacyTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_text(text)
    return docs


from langchain.text_splitter import NLTKTextSplitter

def get_nltk_text_chunks(text, chunk_size=512, chunk_overlap=24):
    text_splitter = NLTKTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_text(text)
    return docs
