
import logging
import os
from typing import Dict, List

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from src.rag.document_loader import CSVDataLoader
from src.rag.vector_store import VexereVectorStore


load_dotenv()

logger = logging.getLogger(__name__)

class VexereRAGPipeline:
    def __init__(self):
        """Initialize RAG pipeline"""
        logger.info("Initializing Vexere RAG Pipeline")
        
        self.data_loader = CSVDataLoader()
        self.vector_store = VexereVectorStore()
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt_template = self.create_prompt_template()
        
        self.qa_chain = None
        self.setup_qa_chain()
        
        logger.info("RAG Pipeline initialized successfully")

    def create_prompt_template(self) -> PromptTemplate:
        """Create prompt template for RAG"""
        template = """Bạn là trợ lý AI của Vexere, nền tảng đặt vé trực tuyến hàng đầu Việt Nam.

Nhiệm vụ của bạn:
- Trả lời câu hỏi về dịch vụ của Vexere một cách chính xác và thân thiện
- Sử dụng thông tin từ cơ sở tri thức để đưa ra câu trả lời phù hợp
- Nếu không có thông tin cần thiết, hãy đề xuất liên hệ bộ phận hỗ trợ

Thông tin từ cơ sở tri thức:
{context}

Câu hỏi của khách hàng: {question}

Trả lời một cách thân thiện và chuyên nghiệp:"""

        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

    def setup_qa_chain(self):
        """Setup RetrievalQA chain"""
        try:
            retriever = self.vector_store.get_retriever(k=3)
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": self.prompt_template},
                return_source_documents=True
            )
            
            logger.info("QA chain setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up QA chain: {str(e)}")
            raise

    def setup_data(self):
        """Load and process FAQ data into vector store"""
        try:
            logger.info("Setting up FAQ data")
            
            documents = self.data_loader.load_data()
            logger.info(f"Loaded {len(documents)} documents")
            
            self.vector_store.add_documents(documents)
            
            logger.info("Data setup completed successfully")
            
        except Exception as e:
            logger.error(f"Error in data setup: {str(e)}")
            raise

    def query(self, question: str) -> Dict:
        """Process user question through RAG pipeline"""
        try:
            if not self.qa_chain:
                raise ValueError("QA chain not initialized")
            
            logger.info(f"Processing question: {question[:50]}...")
            
            result = self.qa_chain.invoke({"query": question})
            
            response = {
                "answer": result.get("result", "").strip(),
                "sources": [],
                "num_sources": len(result.get("source_documents", []))
            }
            
            source_docs = result.get("source_documents", [])
            for doc in source_docs:
                source_info = {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                response["sources"].append(source_info)
            
            logger.info(f"Generated answer with {response['num_sources']} sources")
            return response
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return {
                "answer": "Xin lỗi, có lỗi xảy ra khi xử lý câu hỏi của bạn. Vui lòng thử lại sau.",
                "sources": [],
                "num_sources": 0,
                "error": str(e)
            }

    def search_similar(self, query: str, k: int = 3) -> List[Dict]:
        """Search for similar documents without LLM processing"""
        try:
            logger.info(f"Searching similar documents for: {query[:50]}...")
            
            results = self.vector_store.similarity_search(query, k=k)
            
            similar_docs = []
            for doc in results:
                doc_info = {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                similar_docs.append(doc_info)
            
            logger.info(f"Found {len(similar_docs)} similar documents")
            return similar_docs
            
        except Exception as e:
            logger.error(f"Error searching similar documents: {str(e)}")
            return []



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        logger.info("Testing Vexere RAG Pipeline")
        
        rag = VexereRAGPipeline()
        
        print("Setting up data...")
        # rag.setup_data()
        
            
        result = rag.query("Làm thế nào để đặt vé máy bay?")
        
        print(f" Answer: {result['answer'][:150]}...")
        print(f"Sources used: {result['num_sources']}")
        
        if "error" in result:
            print(f"⚠️ Error: {result['error']}")
        
        logger.info("RAG pipeline test completed successfully")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")