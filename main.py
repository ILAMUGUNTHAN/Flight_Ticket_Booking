# import necessary packages
from flask import Flask, render_template, request, redirect, url_for, session, flash

import datetime

# import modules
import functions as func
import database_operations as sql

app = Flask(__name__, template_folder="front_end")
app.secret_key = "supersecretkey"



# USER

# User login route
@app.route("/ulogin", methods=["GET", "POST"])
def ulogin():
    if request.method == "POST":
        user_id, password = request.form["username"], request.form["password"]
        result = sql.user_authenticate(user_id, func.hash_pass(password))
        if result == 1:
            session['loggedin'] = True
            session['user_id'] = user_id
            session['user_name'] = sql.get_uname(user_id)
            return redirect(url_for('userhome'))
        else:
            flash(result, 'Warning')
            return redirect(url_for('ulogin'))
    


# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_id = request.form["username"]
        result = sql.user_authenticate(user_id, " ")
        if result == "No User Name Exits":
            details = func.make_dict(request.form)
            try:
                sql.add_user(details)
            except:
                flash("Email id already used", 'Warning')
                return redirect(url_for('register'))

            flash("New User Close and login again After 5 mins", 'Warning')
            return redirect(url_for('ulogin'))

        else:
            flash("User Name Already Taken", 'Warning')
            return redirect(url_for('register'))

  




# OPERATIONS

# Route To search Flights
@app.route("/searchflight", methods=['GET', 'POST'])
def searchflight():
    if request.method == 'POST':
        time = request.form['time']
        date = request.form['date']
        val = func.time(date, time)
        flights = func.display_flights(val)
        



# route to book flights
@app.route("/book/<fname>", methods=["POST", 'GET'])
def book(fname):
    result = func.Book_ticket(session['user_id'], fname)
    flash(result, 'alert')
    return redirect(url_for('searchflight'))


# User Logout
@app.route("/alogout")
def alogout():
    session.pop('loggedin', None)
    session.pop('admin_id', None)
    return redirect(url_for('alogin'))


# ADMIN

# Admin login route
@app.route("/alogin", methods=['GET', 'POST'])
def alogin():
    if request.method == 'POST':
        admin_id, adminpass = request.form["adminname"], request.form["adminpass"]
        result = sql.admin_authenticate(admin_id, func.hash_pass(adminpass))
        if result == 1:
            session['loggedin'] = True
            session['admin_id'] = admin_id
            return redirect(url_for('adminhome'))
   


# Admin Home Page
@app.route("/adminhome")
def adminhome():
    flights = []
    flights = func.display_flights_details()
    return render_template("admin_home.html", admin=session['admin_id'], flights=flights)


# Operations

# route to add flights
@app.route("/addflight", methods=["POST", 'GET'])
def addflight():
    if request.method == 'POST':
        result = func.add_flights(request.form)
        flash(result, 'alert')
        return redirect(url_for('addflight'))
    else:
        return render_template('add_flight.html')


# route to remove flights
@app.route("/removeflight", methods=["POST", 'GET'])
def removeflight():
    if request.method == 'POST':
        result = func.remove_flights(request.form['fid'])
        flash(result, 'alert')
        return redirect(url_for('removeflight'))


# route to display all bookings in flight id
@app.route("/allbook", methods=["POST", 'GET'])
def allbook():
    if request.method == 'POST':
        flight_id = request.form['fid']
        users = func.display_allBookings(flight_id)
        flight = func.flight_detail(flight_id)
        if flight == False:
            flash("No Flights Found")
     

# Admin Logout
@app.route("/ulogout")
def ulogout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('ulogin'))


# Main Function To Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
