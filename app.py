from flask import Flask, render_template
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

# close the connection to the database
conn.close()


@app.route('/flowers')
def flowers():
    return render_template('flowers.html',itemsFlowers=itemsFlowers)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
