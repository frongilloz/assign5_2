from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# establish a connection with the database file
conn = sqlite3.connect('flowers2019.db')
# create a cursor to query the database; does NOT change
cursorObj = conn.cursor()

# All items retrieval from FLOWERS table in DB
cursorObj.execute("SELECT * FROM FLOWERS")
# save fetch all to itemsFlowers list; to be referenced in templates
itemsFlowers = cursorObj.fetchall()

# All items retrieval from SIGHTINGS table in DB
cursorObj = conn.execute("SELECT * FROM SIGHTINGS")
# save fetch all to itemsSightings list; to be referenced in templates
itemsSightings = cursorObj.fetchall()

# close the connection to the database
conn.close()

# This is the app route for the "Flower" Page form to receive user input
@app.route('/select_flower', methods = ['POST'])
def select_flower():
    # Request the receive input (POST) to get the selected flower
    sel_Flower = request.form['sel_Flower']
    print("The selected Flower is '" + sel_Flower + "'")

    # Establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database within the app route
    cursorObj = conn.cursor()
    # Run the Query on SIGHTINGS table to get the 10 most recent sightings of the selected flower (from user input)
    cursorObj.execute("SELECT * FROM SIGHTINGS WHERE name = \"" + sel_Flower + "\" ORDER by date(sighted) DESC limit 10")
    # save the queried tuples to the "flowerMostRec"
    flowerMostRec = cursorObj.fetchall()
    # close the connection to the database
    conn.close()

    # render the next template to display the data
    return render_template('flowers_display10.html', flowerMostRec=flowerMostRec)


# Need an app route for insertion specification (instructions)
@app.route('/insert_flower', methods = ['POST'])
def insert_flower():
    # Request the receive input (POST) to new flower
    in_genus = request.form['in_genus']
    print("The new Flower's genus is '" + in_genus + "'")

    in_species = request.form['in_species']
    print("The new Flower's species is '" + in_species + "'")

    in_comname = request.form['in_comname']
    print("The new Flower's comname is '" + in_comname + "'")

    # Establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database within the app route
    cursorObj = conn.cursor()
    # Run the Modification on FLOWERS table to insert
    cursorObj.execute("INSERT INTO FLOWERS VALUES (\"" + in_genus + "\" ,\"" + in_species + "\" ,\"" + in_comname + "\")")
    # Run the query to get the insertion values
    cursorObj.execute(
        "SELECT * FROM FLOWERS WHERE COMNAME = \"" + in_comname +"\"")
    # save the queried tuple to the "query_inserted"
    query_inserted = cursorObj.fetchall()
    # close the connection to the database
    conn.close()

    # render the next template to display the data
    return render_template('insert_flower.html', query_inserted=query_inserted)


# App route for the page of Flowers on the web app
@app.route('/flowers')
def flowers():
    return render_template('flowers.html', itemsFlowers=itemsFlowers)

# App route for the Home page on the web app
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
