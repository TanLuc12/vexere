import logging
import os
from typing import List, Optional

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DATABASE")
username = os.getenv("POSTGRES_USERNAME")
password = os.getenv("POSTGRES_PASSWORD")

logger = logging.getLogger(__name__)

class VexereVectorStore:
    def __init__(self):
        self.collection_name = "vexere_faq"
        self.embedding_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            dimensions=1536,
            api_key=openai_api_key
        )
        self.connection = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        
        logger.info(f"Initializing PGVector store with collection: {self.collection_name}")
        
        try:
            self.vector_store = PGVector(
                embedding_function=self.embedding_model,
                collection_name=self.collection_name,
                connection_string=self.connection
            )
            logger.info("PGVector store initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PGVector store: {str(e)}")
            raise

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to PGVector store"""
        try:
            logger.info(f"Adding {len(documents)} documents to PGVector store")
            
            ids = self.vector_store.add_documents(documents)
            
            logger.info(f"Successfully added {len(ids)} documents to vector store")
            return ids
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Search for similar documents"""
        try:
            logger.info(f"Searching for similar documents: '{query[:50]}...' (k={k})")
            
            results = self.vector_store.similarity_search(query, k=k)
            
            logger.info(f"Found {len(results)} similar documents")
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return []

    def get_retriever(self, k: int = 3):
        """Get retriever for LangChain chains"""
        try:
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": k}
            )
            logger.info(f"Created retriever with k={k}")
            return retriever
            
        except Exception as e:
            logger.error(f"Error creating retriever: {str(e)}")
            raise