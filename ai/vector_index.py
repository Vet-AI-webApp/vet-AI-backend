from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.indexes import VectorstoreIndexCreator

def getVectorIndex():    
    books = ["A_python_book.pdf"]
    chunks = []

    for book in books:
        bookPath = book

        if book:
            loader = UnstructuredPDFLoader(file_path=bookPath)
            data = loader.load()
        else:
            print("Upload a PDF file")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=1000)
        chunks.extend(text_splitter.split_documents(data))

    return VectorstoreIndexCreator().from_documents(chunks)