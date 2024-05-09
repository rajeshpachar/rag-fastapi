from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session
# import nltk
# from nltk.tokenize import sent_tokenize
from openai import OpenAI
from dotenv import load_dotenv

from app.models import FileChunk
from app.tasks.chunk_gen import get_char_text_chunks
from app.libs.string_utils import sanitize_string
from app.tasks.embed_gen import gai_embeddings, oai_embeddings
# , hugging_embeddings

client = OpenAI()

# nltk.download('punkt')


class TextProcessor:
    def __init__(self, db: Session, file_id: int, chunk_size: int = 256, chunk_overlap=16):
        self.db = db
        self.file_id = file_id
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap


    def chunk_and_embed(self, text: str):
        # Split text into sentences
        # sentences = sent_tokenize(text)

        # Chunk sentences
        # chunks = [' '.join(sentences[i:i + self.chunk_size])
                #   for i in range(0, len(sentences), self.chunk_size)]
        chunks = get_char_text_chunks(text, self.chunk_size, self.chunk_overlap)
        # Embed chunks
        # for idx, vector in build_googleai_embeddings(chunks):
        for idx, chunk in enumerate(chunks):
            if not chunk or len(chunk) < 16:
                continue

            vector = gai_embeddings.embed_query(chunk)
            # alt_vector = hugging_embeddings.embed_query(chunk)
            # Create embeddings
            chunk = chunks[idx]
            print("saving chunk idx "+str(idx) + " of " + str(len(chunk)))
            # Store chunk and embedding in database
            file_chunk = FileChunk(file_id=self.file_id,
                                   chunk_text=sanitize_string(chunk),
                                   chunk_index=idx,
                                   vector=vector)
            self.db.add(file_chunk)
        
        self.db.commit()
        print("now commited")
