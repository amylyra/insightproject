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
    """
    Amy Yuan [2:26 PM]
    1. search by product brand and name
    2. return product ingredient list from ES
    3. clean up
    ingredient_return_list = [] (edited)
    4. for every single ingredient in the ingredient list:
    ingredient_return_list += ES.search(single_ingredient, index) (edited)
    ingredient_return_list
    has all the search outcome of ingredient extracted from ES.ingredient
    5. display all the extracted ingredients by name, function, safety rating, blablabla.
    in a table
    to frontend.
    """

    # Search by product brand and name
    if request.method == "POST":
        db.remove()
        search_brand_name = request.form['brand_name']
        search_product_name = request.form['product_name']
        es = init_search()
        product_result = product_search(search_brand_name, search_product_name, es) #TO_DO

    # step 2 and 3
        if product_result:
            ing_raw_list = product_result['Ingredient']
        ing_clean_list = process_ingredient(ing_raw_list) #TO_DO

    # step 4
        ing_canonical_list = []
        for i in ing_clean_list:
            ing_result = ingredient_search(i, es)
                if ing_result:
                    new_ingredient = Ingredient()
                    db_session.add(new_ingredient)
                    db_session.commit()
                    data = {
                        "name": new_ingredient.name,
                        "about": new_ingredient.about,
                        "safety": new_ingredient.safety,
                        "function": new_ingredient.function,
                        }

        print(data)
        pusher_client.trigger('table', 'new-record', {'data': data })



        ing_can_list.append

    ingredients = Ingredient.query.all()
    return render_template('index.html', ingredients=ingredients)

@app.route('/backend', methods=["POST", "GET"])
def backend():
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

        return redirect("/backend", code=302)
    else:
        ingredients = Ingredient.query.all()
        return render_template('backend.html', ingredients=ingredients)

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
#        return redirect("/backend", code=302)
#    else:
#        new_flight = Flight.query.get(id)
#        new_flight.check_in = new_flight.check_in.strftime("%d-%m-%Y %H:%M %p")
#        new_flight.departure = new_flight.departure.strftime("%d-%m-%Y %H:%M %p")
#
#        return render_template('update_flight.html', data=new_flight)

# run Flask app
if __name__ == "__main__":
    app.run()
