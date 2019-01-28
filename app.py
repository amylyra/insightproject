import pusher
import os
from database import db_session
from flask import Flask, request, jsonify, render_template, redirect
from models import Ingredient
from search import init_search, ingredient_search

app = Flask(__name__)

pusher_client = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product', methods=["POST", "GET"])
def product():
    if request.method == "POST":
        search_brand = request.form["brand"]
        search_name = request.form["name"]
        es = init_search()
        result = product_search(search_brand, search_name, es)
        if result:
            brand = result[0]
            name = result[1]
            ingredients = result[2]
            listPrice = result[3]
            size=result[4]
            rating=result[5]
        else:
            brand =  name = ingredients = listPrice = size = rating = None

        print(name)
        print("foo0 " + brand)
        new_product = Product(brand, name, ingredients, listPrice,size,rating)
        print("foo1 " + name)
        db_session.add(new_product)
        print("foo2 " + ingredients)
        db_session.commit()

        data = {
            "brand": new_product.brand,
            "name": new_product.name,
            "ingredients": new_product.ingredients,
            "listPrice": new_product.listPrice,
            "size":new_product.size,
            "rating":new_product.rating

            }

        print(data)
        pusher_client.trigger('table', 'new-record', {'data': data })

        return redirect("/product", code=302)
    else:
        products = Product.query.all()
        return render_template('backend_product.html', products=products)

@app.route('/ing', methods=["POST", "GET"])
def ingredient():
    if request.method == "POST":
        search_name = request.form["ingredient"]
        es = init_search()
        result = ingredient_search(search_name, es)
        if result:
            name = result[0]
            about = result[1]
            safety = result[2]
            function = result[3]
        else:
            name = about = safety = function = None

        print(name)
        print("foo0 " + about)
        new_ingredient = Ingredient(name, about, safety, function)
        print("foo1 " + about)
        db_session.add(new_ingredient)
        print("foo2 " + about)
        db_session.commit()

        data = {
            "name": new_ingredient.name,
            "about": new_ingredient.about,
            "safety": new_ingredient.safety,
            "function": new_ingredient.function,
            }

        print(data)
        pusher_client.trigger('table', 'new-record', {'data': data })

        return redirect("/ing", code=302)
    else:
        ingredients = Ingredient.query.all()
        return render_template('backend_ing.html', ingredients=ingredients)

#@app.route('/edit/<int:id>', methods=["POST", "GET"])
#def update_record(id):
#    if request.method == "POST":
#        flight = request.form["flight"]
#        destination = request.form["destination"]
#        check_in = datetime.strptime(request.form['check_in'], '%d-%m-%Y %H:%M %p')
#        departure = datetime.strptime(request.form['departure'], '%d-%m-%Y %H:%M %p')
#        status = request.form["status"]
#
#        update_flight = Flight.query.get(id)
#        update_flight.flight = flight
#        update_flight.destination = destination
#        update_flight.check_in = check_in
#        update_flight.departure = departure
#        update_flight.status = status
#
#        db_session.commit()
#
#        data = {
#            "id": id,
#            "flight": flight,
#            "destination": destination,
#            "check_in": request.form['check_in'],
#            "departure": request.form['departure'],
#            "status": status}
#
#        pusher_client.trigger('table', 'update-record', {'data': data })
#
#        return redirect("/
", code=302)
#    else:
#        new_flight = Flight.query.get(id)
#        new_flight.check_in = new_flight.check_in.strftime("%d-%m-%Y %H:%M %p")
#        new_flight.departure = new_flight.departure.strftime("%d-%m-%Y %H:%M %p")
#
#        return render_template('update_flight.html', data=new_flight)

# run Flask app
if __name__ == "__main__":
    app.run()
