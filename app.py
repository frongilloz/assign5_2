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


@app.route('/select_flower', methods = ['POST'])
def select_flower():
    sel_Flower = request.form['sel_Flower']
    print("The selected Flower is '" + sel_Flower + "'")

    # establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database; does NOT change
    cursorObj = conn.cursor()
    # All items retrieval from SIGHTINGS table in DB
    cursorObj.execute("SELECT * FROM SIGHTINGS WHERE name = \"" + sel_Flower + "\" ORDER by date(sighted) DESC limit 10")
    # Run Query
    # save fetch all to itemsSightings list; to be referenced in templates
    flowerMostRec = cursorObj.fetchall()

    return render_template('flowers_display10.html', flowerMostRec=flowerMostRec) # used to be redirect('/flowers_display10')


@app.route('/flowers')
def flowers():
    return render_template('flowers.html', itemsFlowers=itemsFlowers)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
