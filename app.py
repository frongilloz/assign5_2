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

# Python3 code to convert tuple into string
def convertTuple(tup):
    str =  ''.join(tup)
    return str

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
    return render_template('flowers_display10.html', flowerMostRec=flowerMostRec, sel_Flower=sel_Flower)

# Update App Route
@app.route('/update_flower', methods = ['POST'])
def update_flower():
    # Establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database within the app route
    cursorObj = conn.cursor()

    # # Create trigger to keep SIGHTINGS table updated as well
    # cursorObj.execute(
    #     "CREATE TRIGGER up_flowers AFTER UPDATE ON Flowers BEGIN UPDATE Sightings SET name = new.comname; END;")

    # Request the receive input (POST) to updated flower
    sel_comname = request.form['sel_Upd_Flower_Comname']
    print("The selected Flower is '" + sel_comname + "'")

    # Query FLOWERS table to get the initial attributes of the selected flower to update
    cursorObj.execute(
        "SELECT genus FROM FLOWERS WHERE comname = \"" + sel_comname + "\"")
    sel_genus = convertTuple(cursorObj.fetchone())
    print("The selected Flower's genus is '" + sel_genus + "'")

    cursorObj.execute(
        "SELECT species FROM FLOWERS WHERE comname = \"" + sel_comname + "\"")
    sel_species = convertTuple(cursorObj.fetchone())
    print("The selected Flower's species is '" + sel_species + "'")


    up_genus = request.form['up_genus']
    print("The new Flower's genus is '" + up_genus + "'")

    up_species = request.form['up_species']
    print("The new Flower's species is '" + up_species + "'")

    up_comname = request.form['up_comname']
    print("The new Flower's comname is '" + up_comname + "'")

    up_genus = request.form['up_genus']
    if up_genus == '':
        up_genus = sel_genus
    print("The Flower's new genus is '" + up_genus + "'")

    up_species = request.form['up_species']
    if up_species == '':
        up_species = sel_species
    print("The Flower's new genus is '" + up_species + "'")

    up_comname = request.form['up_comname']
    if up_comname == '':
        up_comname = sel_comname
    print("The Flower's new genus is '" + up_comname + "'")

    # Run the Modification on FLOWERS table to UPDATE
    cursorObj.execute(
        "UPDATE FLOWERS SET genus = \"" + up_genus + "\", species = \"" + up_species + "\", comname = \"" + up_comname + "\" WHERE comname = \"" + sel_comname + "\"")

    cursorObj.execute(
        "SELECT name FROM SIGHTINGS WHERE name = \"" + sel_comname + "\"")
    sName = convertTuple(cursorObj.fetchone())
    print("Sightings name updated to: '" + sName + "'")

    # Run the query to get the updated values
    cursorObj.execute(
        "SELECT * FROM FLOWERS WHERE COMNAME = \"" + up_comname + "\"")
    # save the queried tuple to the "query_updated"
    query_updated = cursorObj.fetchall()
    # commit these changes
    conn.commit()
    # close the connection to the database
    conn.close()

    # render the next template to display the data
    return render_template('update_flower.html', query_updated=query_updated)


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
    # commit these changes
    conn.commit()
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
    # Every time /flowers is loaded, refresh/update the itemsFlowers
    # Establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database within the app route
    cursorObj = conn.cursor()
    # All items retrieval from FLOWERS table in DB
    cursorObj.execute("SELECT * FROM FLOWERS")
    # save fetch all to itemsFlowers list; to be referenced in templates
    itemsFlowers = cursorObj.fetchall()
    # close the connection to the database
    conn.close()

    return render_template('flowers.html', itemsFlowers=itemsFlowers)

# App route for the Home page on the web app
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
