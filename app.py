from flask import Flask, jsonify

app = Flask(__name__)

user_list = [
    {
        "user_id": 1,
        "user_name": "uanalberto"
    },
    {
        "user_id": 2,
        "user_name": "marisabe"
    },
    {
        "user_id": 3,
        "user_name": "soyconchaentro"
    },
]

concert_list = [
    {
        "place_id": 1,
        "place_name": "Rave en el Raval",
        "place_description": "Cuidado no te roben",
        "price": 20,
        "estimated_max_hours": 3,
        "match_ratio": 90
    },
    {
        "place_id": 2,
        "place_name": "Cumbia en el mar",
        "place_description": "Dale mambo",
        "price": 15,
        "estimated_max_hours": 4,
        "match_ratio": 70
    }
]

# Contact API routes
@app.route('/users', methods=['GET'])
def users():
    return jsonify({"message": "success", "users": user_list}), 200

@app.route('/search', methods=['POST'])
def search():
    return jsonify({"message": "success"}), 200 

@app.route('/places', methods=['GET'])
def places():
    return jsonify({"message": "success", "concerts": concert_list}), 200

if __name__ == '__main__':
    app.run(debug=True)
    
    