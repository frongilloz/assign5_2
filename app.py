from flask import Flask, render_template, request
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


@app.route('/flowers', methods=["GET", "POST"])
def flowers():
    # form = Form()

    if request.method == 'POST':
        # cursorObj = conn.execute("SELECT * FROM Sightings WHERE Sightings.name = request.form.value ORDER BY sighted LIMIT 10")
        # Helpful Video: https://www.youtube.com/watch?v=I2dJuNwlIH0
        print(request.form)
    return render_template('flowers.html',itemsFlowers=itemsFlowers)



@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
