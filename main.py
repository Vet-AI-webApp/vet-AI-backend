import os

import constants

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.indexes import VectorstoreIndexCreator

# ---------------------------- GLOBAL VARIABLES ---------------------------- #
os.environ['OPENAI_API_KEY'] = constants.OPENAI_API_KEY

# ---------------------------- FLASK ---------------------------- #
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ---------------------------- MODELS FOR DATABASE ---------------------------- #
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"User(id = {self.id} , name = {self.name}, age = {self.age})"

# ---------------------------- PUBLIC FUNCTIONS ---------------------------- #
def getInput():
    # query from the user input
    return input("Enter your query: ")

# ---------------------------- AI ---------------------------- #
def getVectorIndex():    
    # load the data from the file
    # books = ["Clinical Veterinary Advisor_ Dogs and Cats   ( PDFDrive ).pdf", "Textbook of Veterinary Internal Medicine ( PDFDrive ).pdf"]
    books = ["A_python_book.pdf"]

    chunks = []

    for book in books:
        # Local PDF file uploads
        # bookPath = f"./veterinarianBooks/{book}"
        bookPath = book

        if book:
            loader = UnstructuredPDFLoader(file_path=bookPath)
            data = loader.load()
        else:
            print("Upload a PDF file")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=1000)
        chunks.extend(text_splitter.split_documents(data))

    # return the index / search engine from the data loader
    return VectorstoreIndexCreator().from_documents(chunks)

# ---------------------------- API ---------------------------- #
def runAPI(myVectorIndex):
    @app.route("/")
    def hello():
        return "Hello World!"

    @app.route("/get/<user_id>")
    def get_user(user_id):
        user_data = {
            "user_id": user_id,
            "name": "John Doe",
            "age": 30
        }

        extra = request.args.get("extra")
        if extra:
            user_data["extra"] = extra

        return jsonify(user_data), 200

    @app.route("/post", methods=["POST"])
    def post_query():
        jsonData = request.get_json()
        query = jsonData["query"]
        result = myVectorIndex.query(query)

        return jsonify(result), 201

    app.run(debug=True)

# ---------------------------- MAIN ---------------------------- #
def main():
    # get the vector index or search engine
    vectorIndex = getVectorIndex()

    # Create or migrate database
    with app.app_context():
        db.create_all()

    runAPI(vectorIndex)
    
    # while True:
    #     query = getInput()
    #     if (query == "exit"):
    #         sys.exit()
    #     else:
    #         result = vectorIndex.query(query)
    #         print(result)

main()