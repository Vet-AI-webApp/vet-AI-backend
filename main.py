import os
import constants

from api import create_app, db
from ai.vector_index import getVectorIndex

# Set OpenAI API Key
os.environ['OPENAI_API_KEY'] = constants.OPENAI_API_KEY

def main():
    # Get the vector index or search engine
    vectorIndex = getVectorIndex()

    # Create the Flask app
    app = create_app(vectorIndex)

    # Create or migrate database
    with app.app_context():
        db.create_all()

    # Run the API
    app.run(debug=True)

if __name__ == "__main__":
    main()