from flask import request, jsonify

def init_routes(app, vectorIndex):
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
        result = vectorIndex.query(query)

        return jsonify(result), 201