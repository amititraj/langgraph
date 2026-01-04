from classes.file_details import CustomFile
from utilities.logging import logger
from typing import List
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
import hashlib
import os

class DocumentProcessor():
    def __init__(self):
        self.headers = [("#", "Header 1"), ("##", "Header 2")]
    
    def process(self, fileobj) -> CustomFile:        
        try:
            # get file name
            file_name = os.path.basename(fileobj.name)            
            # generate file hash
            with open(fileobj.name, "rb") as f:
                file_hash = self._generate_hash(f.read())            
            # get file chunks
            file_chunks = self._get_file_chunks(fileobj)
            
            file = CustomFile(name=file_name, hash=file_hash,chunks=file_chunks)
            return file
        except Exception as e:
            logger.error(f"Failed to process {fileobj.name}: {str(e)}")
            raise e
    
    def _generate_hash(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()
    
    def _get_file_chunks(self, fileobj)-> List:
        try:
            converter = DocumentConverter()
            markdown = converter.convert(fileobj.name).document.export_to_markdown()
            splitter = MarkdownHeaderTextSplitter(self.headers)
            return splitter.split_text(markdown)
        except Exception as e:
            logger.error(f"Error getting file chunks {fileobj.name}: {str(e)}")
            raise e
            
