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

@app.route('/backend', methods=["POST", "GET"])
def backend():
    if request.method == "POST":
        search_brand = request.form["brand"]
        search_name = request.form["name"]
        es = init_search()
        product_result = product_search(search_brand, search_name, es)
        if product_result:
            brand = product_result[0]
            name = product_result[1]
            ing_raw = product_result[2]
            listPrice = product_result[3]
            size=product_result[4]
            rating=product_result[5]
        else:
            brand =  name = ingredients = listPrice = size = rating = None
        
        ing_clean_list = ingredients_processing(ing_raw)
        for ing in ing_clean_list:
            ing_result = ingredient_search(ing, es,index=ingredient_index)
            if ing_result:
                name = ing_result[0]
                about =ing_result[1]
                safety = ing_ result[2]
                function =ing_result[3]
           else:
                name = about = safety = function = None
           new_ingredient = Ingredient(name, about, safety, function)
           db_session.add(new_ingredient)
           db_session.commit()
           ing_data = {
                        "name": new_ingredient.name,
                        "about": new_ingredient.about,
                        "safety": new_ingredient.safety,
                        "function": new_ingredient.function,
                        }

        print(data)
        pusher_client.trigger('table', 'new-record', {'data': ing_data })
        
        print(name)
        print("foo0 " + brand)
        print("foo1 " + name)
        print("foo2 " + ingredients)
        new_product = Product(brand, name, ing_raw, listPrice,size,rating)
        db_session.add(new_product)
        db_session.commit()
        data_product = {
            "brand": new_product.brand,
            "name": new_product.name,
            "ingredients": new_product.ing_raw,
            "listPrice": new_product.listPrice,
            "size":new_product.size,
            "rating":new_product.rating
            }

        print(data_product)
        pusher_client.trigger('table', 'new-record', {'data': data_product })
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
