#!/usr/bin/env python3
from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, Pizza, RestaurantPizza
import os

#-------Config --------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# -------Routes-------
@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# GET /restaurants
class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return make_response(
            [r.to_dict() for r in restaurants],
            200
        )

api.add_resource(Restaurants, '/restaurants')

# GET /restaurants/<int:id>, DELETE /restaurants/<int:id>
class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        return restaurant.to_dict(), 200

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        db.session.delete(restaurant)
        db.session.commit()
        return {"message": f"Deleted restaurant: {restaurant.name}"}, 200

api.add_resource(RestaurantById, '/restaurants/<int:id>')
# GET /pizzas
class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return make_response(
            [p.to_dict() for p in pizzas],
            200
        )

api.add_resource(Pizzas, '/pizzas')

# POST /restaurant_pizzas
class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        try:
            new_rp = RestaurantPizza(
                price=data["price"],
                restaurant_id=data["restaurant_id"],
                pizza_id=data["pizza_id"]
            )
            db.session.add(new_rp)
            db.session.commit()

            return make_response(new_rp.to_dict(), 201)

        except Exception as e:  # noqa: F841
            return make_response({"errors": ["validation errors"]}, 400)

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

# ------Main Runner--------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
