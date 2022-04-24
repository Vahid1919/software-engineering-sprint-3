from email import message
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime
from pip import main
import yaml
import uuid
import qrcode
import qrcode.image.svg
from io import BytesIO
from flask_bcrypt import Bcrypt
from flask_selfdoc import Autodoc

import helpers.my_validation  # custom validation functions 

app = Flask(__name__)

bcrypt = Bcrypt(app)
auto = Autodoc(app)
app.secret_key = 'BAD_SECRET_KEY'

# Load database configuration into flask app from file
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['SECRET_KEY'] = db['bcrypt_secret']

mysql = MySQL(app)

# Route for home/index
@app.before_request
def before_request():
    session.permanent = True


# Home page
@app.route('/')
@app.route('/index')
@auto.doc()
def index():
    # Shows user selection menu. Not protected
    
    # If any user is already signed in as a visitor, redirect to home
    # TODO --> This is good theoritically but is sometimes buggy when opening browser anew
    if 'User_device_id' in session:
        return redirect('/visitor-home')
    
    if 'Place_device_id' in session:
        return redirect('/place-home')
    
    if 'Agent_id' in session:
        return redirect('/agent-home')
    
    if 'Hospital_id' in session:
        return redirect('/hospital-home')
    
    
    return render_template('index.html')


# Visitor registration page
@app.route('/visitor-registration', methods=['GET', 'POST'])
@auto.doc()
def registerVisitor():
    # Requires: name, city, address, email, phone

    # If the user is already logged in, redirect to home
    if 'User_device_id' in session:
        return redirect('/visitor-home')

    if request.method == 'GET':
        return render_template('visitor-registration.html')
    
    elif request.method == 'POST':
        # Obtain form data from request object
        name = request.form['name']
        city = request.form['city']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        device_id = uuid.uuid4()  # Generate unique identifier for user device

        # Validate input
        valid, message = helpers.my_validation.visitor_validate([name, city, address, email, phone])
        if not valid:
            return render_template('visitor-registration.html', message=message), 400

        # Set user session object
        session['User_device_id'] = device_id

        # Execute and commit SQL command
        cur = mysql.connection.cursor()
        command = f"""INSERT INTO Visitor(visitor_name, city , address, phone_number, email, device_id)
                    VALUES ("{name}", "{city}", "{address}", "{phone}", "{email}", "{device_id}")"""
        cur.execute(command)
        mysql.connection.commit()
        cur.close()

        # store full name in session
        names = name.split(' ')
        session['user_first_name'] = names[0]
        


        # Registration successful. Redirect to Visitor home page
        
        return redirect('/visitor-home')


# PlaceOwner registration page
@app.route('/place-registration', methods=['GET', 'POST'])
@auto.doc()
def registerPlace():
    # Requires: pname, address, email, phone

    # If the user is already logged in, redirect to home
    if 'Place_device_id' in session:
        return redirect('/place-home')
    
    if request.method == 'GET':
        return render_template('place-registration.html')

    elif request.method == 'POST':
        # Obtain form data from request object
        pname = request.form['pname']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']

        # Validate input
        valid, message = helpers.my_validation.place_validate([pname, phone, address, email])
        if (not valid):
            return render_template('place-registration.html', message=message), 400

        # Generate unique string for QRcode and set session with it
        QRcode = uuid.uuid4()
        session['Place_device_id'] = QRcode
        session['Place_name'] = pname

        # Execute and commit SQL command
        cur = mysql.connection.cursor()
        command = f"""INSERT INTO PlaceOwner(place_name, phone_no, email, address, QRcode)
                    VALUES ('{pname}', '{phone}', '{email}', '{address}', '{QRcode}')"""
        cur.execute(command)
        mysql.connection.commit()
        cur.close()

        return render_template('place-home.html'), 200


# Agent login page
@app.route('/agent-login', methods=['GET', 'POST'])
@auto.doc()
def loginAgent():
    # Requires: agent_id, username, password

    # If the user is already logged in, redirect to home
    if 'Agent_id' in session:
        return redirect('/agent-home')
    
    if request.method == 'GET':
        return render_template('agent-login.html')
    
    elif request.method == 'POST':
        # Obtain data from request object
        agent_id = request.form['agent_id']
        username = request.form['username']
        password = request.form['password']

        # Validate input
        valid, message = helpers.my_validation.agent_validate([agent_id,username,password])
        if not valid:
            return render_template('agent-login.html',message=message),  401

        # Find agent specified by the ID
        cur = mysql.connection.cursor()
        command = f"SELECT * FROM Agent WHERE agent_id={agent_id}"
        cur.execute(command)
        agent = cur.fetchall()
        cur.close()

        # If agent isn't found, redirect back to the page with an error
        if (len(agent) == 0):
            return redirect('/agent-login'), 400

        else:
            # If agent is found, check username and password
            if (agent[0][1] == username and agent[0][2] == password):
                session['Agent_id'] = agent_id
                return render_template('agent-home.html', username = username)
            else:
                return render_template('agent-login.html'),  401


# Agent home page
@app.route('/agent-home')
@auto.doc()
def agentHome():
    if 'Agent_id' not in session:
        return redirect('/agent-login')
    return render_template('agent-home.html')


# Search by Visitor.
@app.route('/agent-visitor-search', methods=['GET', 'POST'])
@auto.doc()
def searchCitizen():
    # Shows dropdown with the infected visitors, and a table with them

    cur = mysql.connection.cursor()
    command = ""
    # Filter the information if a POST request is made
    if request.method == 'POST' and request.form['id'] != "invalid":
        command = f"""SELECT citizen_id, visitor_name, city, address, phone_number, email
                    FROM Visitor WHERE citizen_id = {request.form['id']}"""
    else:
        command = f"""SELECT citizen_id, visitor_name, city, address, phone_number, email, infected
                    FROM Visitor"""
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    return render_template('agent-visitor-search.html', data = result)


# Search by Place
@app.route('/agent-place-search', methods=['GET', 'POST'])
@auto.doc()
def searchPlace():
    # Shows dropdown with the places infected visitors have been to, and a table with them
    
    cur = mysql.connection.cursor()
    command = ""
    # Filter the information if a POST request is made
    if request.method == 'GET':
        # query for the places infected visitors have visited in a period of time
        command = """SELECT place_name, place_id FROM PlaceOwner, VisitorToPlace, Visitor
                    WHERE Visitor.device_id = VisitorToPlace.device_id AND
                        PlaceOwner.QRcode = VisitorToPlace.QRcode"""
    elif request.method == 'POST':
        from_time = request.form['from']
        to_time = request.form['to']
        # query for selecting the information of a place
        command = f"""SELECT * FROM PlaceOwner
                    WHERE Time >= '{from_time}' AND Time <= '{to_time}'"""
    cur.execute(command)
    result = cur.fetchall()
    return render_template('agent-place-search.html', data = result)


# Agent's Add Hospitals page
@app.route('/agent-add-hospital', methods=['GET', 'POST'])
@auto.doc()
def addHospital():
    # Requires: username, password
    
    if request.method == 'GET':
        return render_template('agent-add-hospital.html')

    elif request.method == 'POST':
        # Obtain form data from request object
        username = request.form['username']
        password = request.form['password']

        # Validate input
        valid, message = helpers.my_validation.place_validate([username, password])
        if (not valid):
            return render_template('agent-add-hospital.html', message = message), 400
        
        # If hospital is in the database already, redirect back to the page with an error
        cur = mysql.connection.cursor()
        command = f"SELECT * FROM Hospital WHERE username = '{username}' AND password = '{password}'"
        cur.execute(command)
        hospital = cur.fetchall()
        if (len(hospital) > 0):
            return redirect('/agent-add-hospital'), 200

        # Execute and commit SQL command
        command = f"""INSERT INTO Hospital(username, password)
                    VALUES ('{username}', '{password}')"""
        cur.execute(command)
        mysql.connection.commit()
        cur.close()

        message = f"Successfully registered {username} as Hospital"
        return render_template('agent-add-hospital.html', message = message), 200


# Hospital login page
@app.route('/hospital-login', methods=['GET', 'POST'])
@auto.doc()
def loginHospital():
    # Requires: username, password

    # If the registration is successful, redirect to the Hospital home page
    if 'Hospital_id' in session:
        return redirect('/hospital-home')
    
    if request.method == 'GET':
        return render_template('hospital-login.html')

    elif request.method == 'POST':
        # Obtain data from request object
        username = request.form['username']
        password = request.form['password']

        # Validate input
        valid, message = helpers.my_validation.hospital_validate([username, password])
        if not valid:
            return render_template('hospital-login.html', message = message),  401

        # Execute and commit SQL command
        cur = mysql.connection.cursor()
        command = f"SELECT * FROM Hospital WHERE username = '{username}' AND password = '{password}'"
        cur.execute(command)
        hospital = cur.fetchall()
        cur.close()

        # If hospital isn't found, redirect back to the page with an error
        if (len(hospital) == 0):
            return redirect('/hospital-login'), 400

        else:
            # If hospital is found, check username and password
            if (hospital[0][1] == username and hospital[0][2] == password):
                session['Hospital_id'] = hospital[0][0]
                session['Hospital_name'] = username
                return redirect('/hospital-DB-search')
            else:
                return render_template('hospital-login.html'),  401



# Hospital database access page
@app.route('/hospital-DB-search', methods=['GET', 'POST'])
@auto.doc()
def hospitalDBsearch():
    # Can look for visitors and change their infected status

    cur = mysql.connection.cursor()
    command = ""
    # Filter information if a POST request is made
    if request.method == 'GET':
        command = f"SELECT citizen_id, visitor_name, city, address, phone_number, email, infected FROM Visitor"

    elif request.method == 'POST':
        command = f"""SELECT citizen_id, visitor_name, city, address, phone_number, email, infected FROM Visitor
                    WHERE visitor_name LIKE '%{request.form['name']}%'"""
    cur.execute(command)
    visitors = cur.fetchall()
    hospital_username = session['Hospital_name']
    return render_template('hospital-DB-search.html', data = visitors, username = hospital_username ), 200


# route to change a visitor's status
@app.route('/hospital-DB-status-change', methods=['GET', 'POST'])
@auto.doc()
def hospitalDBstatuschange():
    if 'Hospital_id' not in session:
        return redirect('/hospital-login')
    
    if request.method == "POST":
        # Obtain data from request object
        name = request.form['name']
        status = request.form['status']

        # Update the status of the user and fetch the table again to show the change
        cur = mysql.connection.cursor()
        command = f"UPDATE Visitor SET infected = {status} WHERE visitor_name = '{name}'"
        cur.execute(command)
        mysql.connection.commit()

        command = f"""SELECT citizen_id, visitor_name, city, address, phone_number, email, infected FROM Visitor
                    WHERE visitor_name LIKE '%{name}%'"""
        cur.execute(command)
        visitors = cur.fetchall()
        cur.close()

        return render_template('hospital-DB-search.html', data=visitors ), 200


# Visitor home page
@app.route('/visitor-home')
@auto.doc()
def visitorHome():
    # If visitor is not logged in, redirect to home
    if 'User_device_id' not in session:
        return redirect('/visitor-registration')
    
    return render_template('visitor-home.html', name = session['user_first_name'])


# Visitor sign in to a place
@app.route('/place/<id>')
@auto.doc()
def visitorSignedIn(id):
    # If visitor is not logged in, redirect to home
    if 'User_device_id' not in session:
        return redirect('/')

    # Fetch name of place and obtain the name
    cur = mysql.connection.cursor()
    command = f'SELECT place_name FROM PlaceOwner WHERE QRcode="{str(id)}"'
    cur.execute(command)
    record = cur.fetchall()[0][0]

    # Use html with name as data
    return render_template('checked-in-place.html', data=record)


# PlaceOwner home page
@app.route('/place-home')
@auto.doc()
def placeHome():
    # If place owner is not logged in, redirect to home
    if 'Place_device_id' not in session:
        return redirect('/place-registration')
    
    # Generate QR code
    data = session['Place_device_id']  # Fetch QRcode string from session
    factory = qrcode.image.svg.SvgImage  # Select format of QR to generate
    img = qrcode.make(data, image_factory=factory)  # Generate QR code

    # Convert generated QR code into HTML readable format
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()
    
    #Get place name to personalize dashboard
    place_name = session['Place_name']

    # Show the place owner their QR
    return render_template('place-home.html', data_svg=svg, place_name = place_name)


# Visitor signin page
@app.route('/signin', methods=['POST'])
@auto.doc()
def signIn():
    # Requires: time, qr
    # Used to add record of user signin to database

    # If visitor is not logged in, redirect to home
    if 'User_device_id' not in session:
        return redirect('/')

    # Get time and qr from request object, needed to create a record
    time = request.form['time']
    qr = request.form['qrcode']
    device_id = session['User_device_id']

    # Query for finding whether a visitor has already signed in to the place
    cur = mysql.connection.cursor()
    command = f"""SELECT * FROM VisitorToPlace
                WHERE QRcode="{qr}" AND device_id="{device_id}" AND exit_time IS NULL"""
    cur.execute(command)
    result = cur.fetchall()

    if len(result) == 0:  # If the visitor has not signed in

        # String for creating new record, exit time is left NULL and updated later
        command = f"""INSERT INTO VisitorToPlace(QRcode, device_id, entry_time)
                VALUES ("{qr}", "{device_id}","{time}")"""
        cur.execute(command)
        mysql.connection.commit()
        cur.close()
        
        return time  # Return entry time

    else:  # If the visitor has already signed in

        # Query for fetching entry time
        command = f"""SELECT * FROM VisitorToPlace
                    WHERE QRcode="{qr}" AND device_id="{device_id}" AND exit_time IS NULL"""
        cur.execute(command)
        result = cur.fetchall()[0][2]
        cur.close()

        return str(result)  # Return entry time


# User signout page
@app.route('/signout', methods=['POST'])
@auto.doc()
def signOut():
    # Return user to index if not logged in
    if 'User_device_id' not in session:
        return redirect('/')

    # Obtain time, QR code, and device_id from request object
    time = request.form['time']
    qr = request.form['qrcode']
    device_id = session['User_device_id']

    # Update database to reflect visitor signout
    cur = mysql.connection.cursor()
    # Query string for updating exit time of record identified by qr, devce and entry time
    command = f"""UPDATE VisitorToPlace SET exit_time="{time}"
                WHERE QRcode="{qr}" AND device_id="{device_id}" AND exit_time is NULL"""
    cur = mysql.connection.cursor()
    cur.execute(command)
    mysql.connection.commit()
    cur.close()

    return "Saved"
 #redirect("/visitor-home")  # Return confirmation of signing out



# Access to documentation with /docs after the link
@app.route('/docs')
def documentation():
    return auto.html(title='Corona Archive documentation')


# Logout page
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
