### Running the App

To get the app running:

 - From a command line, make sure you are in the project's root folder - `realtime-table`
 - Create a virtual environment:
 ```
 python3 -m venv env
 ```
 - Activate the virtual environment:
 ```
   source env/bin/activate
 ```
 On windows? Activate it with the below:
 ```
   env/Scripts/activate
 ```

 - Install the dependencies:
 ```
 pip install -r requirements.txt
 ```

 - Initialize DB: 
 python
 >>> from database import init_db
 >>> init_db()

 - Finally run the app:
 ```
  flask run
 ```

 Congrats! The app should now be running on http://localhost:5000.


- Open your browser and fire up the app - http://localhost:5000/
- Then, open the backend page in another tab - http://localhost:5000/backend
- Next, add or update a flight. You would see the changes appear in realtime on the index page. 

## Built With

* [Flask](http://flask.pocoo.org/) - A microframework for Python
* [Pusher](https://pusher.com/) - APIs to enable devs building realtime features
