# Title: Assignment 5
# Description: A GUI for querying and modifying the flowers2019.db through sqlite3 queries, insertions, and triggers
# Date: 12/12/2019
# Authors: Zoe Frongillo and Jhanava Ramisetty

from flask import Flask, render_template, request, redirect, session
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

cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'sightings_logs');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TABLE sightings_logs (old_name, new_name, old_person, new_person, old_location, new_location, old_sighted, new_sighted, user_action, created_at);")

cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'features_logs');"
)
count1 = cursorObj.fetchone()
if count1[0] == 0:
    cursorObj.execute(
        "CREATE TABLE features_logs (old_location, new_location, old_class, new_class, old_latitude, new_latitude, old_longitude, new_longitude, old_map, new_map, old_elev, new_elev, user_action, created_at);")

cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'flowers_logs');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TABLE flowers_logs (old_genus, new_genus, old_species, new_species, old_comname, new_comname, user_action, created_at);")


# Create trigger to log SIGHTINGS, FEATURES, and FLOWERS table insertions, deletions, and updates
# SIGHTINGS
cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'sightings_insert_log');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER sightings_insert_log AFTER INSERT ON SIGHTINGS BEGIN INSERT INTO sightings_logs(new_name, new_person, new_location, new_sighted, user_action, created_at) VALUES(new.name, new.person, new.location, new.sighted, 'INSERT', DATETIME('NOW')); END;")


cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'sightings_delete_log');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER sightings_delete_log AFTER DELETE ON SIGHTINGS BEGIN INSERT INTO sightings_logs(old_name, old_person, old_location, old_sighted, user_action, created_at) VALUES(old.name, old.person, old.location, old.sighted, 'DELETE', DATETIME('NOW')); END;")


cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'sightings_update_log');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER sightings_update_log AFTER UPDATE ON SIGHTINGS WHEN old.name <> new.name OR old.person <> old.person OR old.location <> new.location OR old.sighted <> new.sighted BEGIN INSERT INTO sightings_logs VALUES(old.name, new.name, old.person, new.person, old.location, new.location, old.sighted, new.sighted, 'UPDATE', DATETIME('NOW')); END;")


# FEATURES
cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'features_insert_log');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER features_insert_log AFTER INSERT ON FEATURES BEGIN INSERT INTO features_logs(new_location, new_class, new_latitude, new_longitude, new_map, new_elev, user_action, created_at) VALUES(new.location, new.class, new.latitude, new.longitude, new.map, new.elev, 'INSERT', DATETIME('NOW')); END;")


cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'features_delete_log');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER features_delete_log AFTER DELETE ON FEATURES BEGIN INSERT INTO features_logs(old_location, old_class, old_latitude, old_longitude, old_map, old_elev, user_action, created_at) VALUES(old.location, old.class, old.latitude, old.longitude, old.map, old.elev, 'DELETE', DATETIME('NOW')); END;")


cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'features_update_log');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER features_update_log AFTER UPDATE ON FEATURES WHEN old.location <> new.location OR old.class <> new.class OR old.latitude <> new.latitude OR old.longitude <> new.longitude OR old.map <> new.map OR old.elev <> new.elev BEGIN INSERT INTO features_logs VALUES(old.location, new.location, old.class, new.class, old.latitude, new.latitude, old.longitude, new.longitude, old.map, new.map, old.elev, new.elev, 'UPDATE', DATETIME('NOW')); END;")


#FLOWERS
cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'flowers_insert_log');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER flowers_insert_log AFTER INSERT ON FLOWERS BEGIN INSERT INTO flowers_logs(new_genus, new_species, new_comname, user_action, created_at) VALUES(new.genus, new.species, new.comname, 'INSERT', DATETIME('NOW')); END;")


cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'flowers_delete_log');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER flowers_delete_log AFTER DELETE ON FLOWERS BEGIN INSERT INTO flowers_logs(old_genus, old_species, old_comname, user_action, created_at) VALUES(old.genus, old.species, old.comname, 'DELETE', DATETIME('NOW')); END;")


cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'flowers_update_log');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER flowers_update_log AFTER UPDATE ON FLOWERS WHEN old.genus <> new.genus OR old.species <> new.species OR old.comname <> new.comname BEGIN INSERT INTO flowers_logs VALUES(old.genus, new.genus, old.species, new.species, old.comname, new.comname, 'UPDATE', DATETIME('NOW')); END;")

# Create trigger to keep SIGHTINGS table updated as well
cursorObj.execute(
    "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'up_flowers');"
)
count = cursorObj.fetchone()
if count[0] == 0:
    cursorObj.execute(
        "CREATE TRIGGER up_flowers AFTER UPDATE ON Flowers BEGIN UPDATE Sightings SET name = new.comname WHERE name = old.comname; END;")

# Create trigger to log changes
# Trigger for update on flowers
# before creating trigger, make sure it does not exist

# cursorObj.execute(
#     "SELECT COUNT(*) FROM (SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'log_up_flowers');"
# )
# count = cursorObj.fetchone()
# if count[0] == 0:
#     cursorObj.execute(
#         "CREATE TRIGGER log_up_flowers AFTER UPDATE on FLOWERS "
#         "BEGIN"
#           " INSERT INTO log_changes VALUES(\"Update\", \"Flowers\", old.genus, old.species, "
#             "old.comname, new.genus, new.species, new.comname,"
#             " \"n/a\",\"n/a\",\"n/a\",\"n/a\"); "
#         "end; ")

# close the connection to the database
conn.close()


# Python3 code to convert tuple into string
def convertTuple(tup):
    str = ''.join(tup)
    return str


# This is the app route for the "Flower" Page form to receive user input
@app.route('/select_flower', methods=['POST'])
def select_flower():
    # Request the receive input (POST) to get the selected flower
    sel_Flower = request.form['sel_Flower']
    print("The selected Flower is '" + sel_Flower + "'")

    # Establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database within the app route
    cursorObj = conn.cursor()
    # Run the Query on SIGHTINGS table to get the 10 most recent sightings of the selected flower (from user input)
    cursorObj.execute(
        "SELECT * FROM SIGHTINGS WHERE name = \"" + sel_Flower + "\" ORDER by date(sighted) DESC limit 10")
    # save the queried tuples to the "flowerMostRec"
    flowerMostRec = cursorObj.fetchall()
    # close the connection to the database
    conn.close()

    # render the next template to display the data
    return render_template('flowers_display10.html', flowerMostRec=flowerMostRec, sel_Flower=sel_Flower)


# Update App Route
@app.route('/update_flower', methods=['POST'])
def update_flower():
    # Establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database within the app route
    cursorObj = conn.cursor()

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

    # Retrieve the updated attributes
    up_genus = request.form['up_genus']
    print("The new Flower's genus is '" + up_genus + "'")

    up_species = request.form['up_species']
    print("The new Flower's species is '" + up_species + "'")

    up_comname = request.form['up_comname']
    print("The new Flower's comname is '" + up_comname + "'")

    # Check if updated attributes are blank
    up_genus = request.form['up_genus']
    if up_genus == '':
        up_genus = sel_genus
    print("The Flower's new genus is '" + up_genus + "'")

    up_species = request.form['up_species']
    if up_species == '':
        up_species = sel_species
    print("The Flower's new species is '" + up_species + "'")

    up_comname = request.form['up_comname']
    if up_comname == '':
        up_comname = sel_comname
    print("The Flower's new comname is '" + up_comname + "'")

    cursorObj.execute(
        "SELECT name FROM SIGHTINGS WHERE name = \"" + up_comname + "\"")
    print(cursorObj.fetchone())
    # sName = convertTuple(cursorObj.fetchone())
    # print("Sightings name updated to: '" + sName + "'")

    # Check if updated attributes are blank
    up_genus = request.form['up_genus']
    if up_genus == '':
        up_genus = sel_genus
    print("The Flower's new genus is '" + up_genus + "'")

    up_species = request.form['up_species']
    if up_species == '':
        up_species = sel_species
    print("The Flower's new species is '" + up_species + "'")

    up_comname = request.form['up_comname']
    if up_comname == '':
        up_comname = sel_comname
    print("The Flower's new comname is '" + up_comname + "'")

    # Run the Modification on FLOWERS table to UPDATE
    cursorObj.execute(
        "UPDATE FLOWERS SET genus = \"" + up_genus + "\", species = \"" + up_species + "\", comname = \"" + up_comname + "\" WHERE comname = \"" + sel_comname + "\"")

    cursorObj.execute(
        "SELECT name FROM SIGHTINGS WHERE name = \"" + up_comname + "\"")
    print(cursorObj.fetchone())
    # sName = convertTuple(cursorObj.fetchone())
    # print("Sightings name updated to: '" + sName + "'")

    cursorObj.execute(
        "SELECT * FROM flowers_logs;")
    print(cursorObj.fetchall())

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
    return render_template('update_flower.html', query_updated=query_updated, sel_Flower=sel_comname)


# Need an app route for insertion specification (instructions)
@app.route('/insert_sighting', methods=['POST'])
def insert_sighting():
    # Request the receive input (POST) to new SIGHTING
    in_fl_name = request.form['sel_InsS_Flower_Comname']
    print("The new Sighting's Flower's name is '" + in_fl_name + "'")

    in_person = request.form['in_person']
    print("The new Sighting's Person name is '" + in_person + "'")

    in_location = request.form['in_location']
    print("The new Sighting's Location name is '" + in_location + "'")

    in_sighted = request.form['in_sighted']
    print("The new Sighting's Date is '" + in_sighted + "'")

    # Establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database within the app route
    cursorObj = conn.cursor()
    # Run the Modification on FLOWERS table to insert
    cursorObj.execute("INSERT INTO SIGHTINGS VALUES (\"" + in_fl_name + "\" ,\"" + in_person + "\" ,\""
                      + in_location + "\" ,\"" + in_sighted + "\")")
    # commit these changes
    conn.commit()
    # Run the query to get the insertion values
    cursorObj.execute(
        "SELECT * FROM SIGHTINGS WHERE name = \"" + in_fl_name + "\" AND sighted = \"" + in_sighted + "\"")
    # save the queried tuple to the "query_inserted"
    query_inserted = cursorObj.fetchall()
    # close the connection to the database
    conn.close()

    # render the next template to display the data
    return render_template('insert_flower.html', query_inserted=query_inserted, sel_Flower=in_fl_name)


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


# App route to login on the web app
@app.route('/login')
def login():
    return render_template('login.html')


# App route to login on the web app
@app.route('/login_form', methods=['POST'])
def login_form():
    # Request the receive input (POST) to new user
    email = request.form['login_email']
    print("The user's email is '" + email + "'")

    password = request.form['login_pw']
    print("The user's password is '" + password + "'")

    # Establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database within the app route
    cursorObj = conn.cursor()
    # All items retrieval from FLOWERS table in DB
    cursorObj.execute("SELECT fullName FROM USERS WHERE email = \"" + email + "\" AND password = \"" + password + "\"")
    # save fetch all to itemsFlowers list; to be referenced in templates
    query_tuple = cursorObj.fetchone()
    # close the connection to the database
    conn.close()

    # if query was empty, user does not exist
    if not (query_tuple):
        print("User does not exist")
        return render_template('login_failure.html')
    else:
        query_name = convertTuple(query_tuple)
        return render_template('login_success.html', query_name=query_name)


# App route to log out
@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/logout_form', methods=['POST'])
def logout_form():
    return render_template('logout_success.html')


# App route to sign up on the web app
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/sign_up_form', methods=['POST'])
def sign_up_form():
    # Request the receive input (POST) to new user
    fullName = request.form['fullName']
    print("The user's full name is '" + fullName + "'")

    email = request.form['email']
    print("The user's email is '" + email + "'")

    password = request.form['password']
    print("The user's password is '" + password + "'")

    # Establish a connection with the database file
    conn = sqlite3.connect('flowers2019.db')
    # create a cursor to query the database within the app route
    cursorObj = conn.cursor()
    # Run the Modification on FLOWERS table to insert
    cursorObj.execute(
        "INSERT INTO USERS VALUES (\"" + fullName + "\" ,\"" + email + "\" ,\"" + password + "\")")
    # commit these changes
    conn.commit()
    # close the connection to the database
    conn.close()

    return render_template('sign_up_complete.html')


# App route for the Home page on the web app
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
