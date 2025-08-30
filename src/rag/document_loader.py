import logging
import os
from langchain_community.document_loaders import CSVLoader

logger = logging.getLogger(__name__)

class CSVDataLoader:
    def __init__(self, file_path: str = r"D:\vexere\data\faq_data.csv") -> None:
        self.file_path = file_path
        logger.info(f" Initialized CSVDataLoader with file: {self.file_path}")

    def load_data(self):
        try:

            if not os.path.exists(self.file_path):
                logger.error(f"File not found: {self.file_path}")
                raise FileNotFoundError(f"CSV file not found: {self.file_path}")
            
            logger.info(f"Loading data from: {self.file_path}")
            loader = CSVLoader(
                file_path=self.file_path,
                csv_args={
                    'delimiter': ',',
                    'quotechar': '"',
                    'fieldnames': ['question', 'answer']
                },
                encoding="utf-8-sig"
            )
            documents = loader.load()
            return documents
        except Exception as e:
            logger.error(f"Error loading CSV data: {str(e)}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    data_loader = CSVDataLoader()
    documents = data_loader.load_data()
    print(f"Total documents: {len(documents)}")
