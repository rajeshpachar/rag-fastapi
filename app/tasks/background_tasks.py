from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session
import nltk
from nltk.tokenize import sent_tokenize
from openai import OpenAI
from dotenv import load_dotenv

from app.models import FileChunk
from app.tasks.chunk_gen import get_char_text_chunks
from app.tasks.embed_gen import build_googleai_embeddings

client = OpenAI()

nltk.download('punkt')


class TextProcessor:
    def __init__(self, db: Session, file_id: int, chunk_size: int = 2):
        self.db = db
        self.file_id = file_id
        self.chunk_size = chunk_size


    def chunk_and_embed(self, text: str):
        # Split text into sentences
        # sentences = sent_tokenize(text)

        # Chunk sentences
        # chunks = [' '.join(sentences[i:i + self.chunk_size])
                #   for i in range(0, len(sentences), self.chunk_size)]
        chunks = get_char_text_chunks(text, self.chunk_size)
        # Embed chunks
        for idx, vector in build_googleai_embeddings(chunks):
            # Create embeddings
            chunk = chunks[idx]
            # Store chunk and embedding in database
            file_chunk = FileChunk(file_id=self.file_id,
                                   chunk_text=chunk,
                                   chunk_index=idx,
                                   chunk_length=len(chunk),
                                   embedding_vector=vector)
            self.db.add(file_chunk)

        self.db.commit()
