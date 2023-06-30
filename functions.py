# import libraries
import hashlib
import database_operations as sql
import datetime


# Common Functions

# hash the password
def hash_pass(password):
    salt = 'csk'
    password = password + salt
    hashed = hashlib.md5(password.encode())
    return hashed.hexdigest()


# convert values to dict
def make_dict(form):
    details = {
        'user_id': form['username'],
        'password': hash_pass(form['password']),
        'email_id': form['email'],
        'phone_no': form['phone'],
        'name': form['name'],
    }
    return details


# converting time from input
def time(date, time):
    val = date + " " + time
    print(val)
    date = datetime.datetime.strptime(val, '%Y-%m-%d %H:%M')
    return date


# User Side

# displaying All My bookings
def display_myBookings(user_id):
    bookings = []
    result = sql.get_mybooking(user_id)
    for row in result:
        date = row['booking_time'].strftime('%d/%m/%Y')
        time = row['booking_time'].strftime('%H:%M:%S')
        flight_id = row['flight_id']
        flight = sql.get_fdetails(flight_id)
        for values in flight:
            fname = values['flight_name']
            fcompany = values['flight_company']
            fdate = values['flight_time'].strftime('%d/%m/%Y')
            ftime = values['flight_time'].strftime('%H:%M:%S')
            current = [date, time, fname, fcompany, fdate, ftime]
        bookings.append(current)
    return bookings


# display all available flights
def display_flights(date):
    flights = []
    result = sql.get_flights(date)
    for row in result:
        if row['empty_seat'] > 0:
            fname = row['flight_name']
            fcompany = row['flight_company']
            fdate = row['flight_time'].strftime('%d/%m/%Y')
            ftime = row['flight_time'].strftime('%H:%M:%S')
            fid = row['flight_id']
            flight = [fname, fcompany, fdate, ftime, fid]
            flights.append(flight)
    print(flights)
    return flights


# Book the ticket
def Book_ticket(user_id, flight_id):
    if sql.update_seats(flight_id):
        sql.add_booking({'flight_id': flight_id, 'userid': user_id})
        return 'Succesfully Booked'
    else:
        return "failed"


# Admin Side

# adding flights
def add_flights(form):
    day = time(form['fdate'], form['ftime'])
    flight = {
        'flight_id': form['fid'],
        'flight_company': form['fcompany'],
        'flight_time': day,
        'flight_name': form['fname'],
    }
    if sql.add_flight(flight):
        return "successfully Added"
    else:
        return "failed"


# remove flights
def remove_flights(flight_id):
    if sql.remove_flight(flight_id):
        return "successfully Removed"
    else:
        return "failed to remove"


# show all bookings
def display_allBookings(flight_id):
    bookings = []
    result = sql.get_bookings(flight_id)
    for row in result:
        date = row['booking_time'].strftime('%d/%m/%Y')
        time = row['booking_time'].strftime('%H:%M:%S')
        name = sql.get_uname(row['user_id'])
        current = [name, date, time]
        bookings.append(current)
    return bookings


# flight details
def flight_detail(flight_id):
    flight = sql.get_fdetails(flight_id)
    for row in flight:
        fname = row['flight_name']
        fcompany = row['flight_company']
        fdate = row['flight_time'].strftime('%d/%m/%Y')
        ftime = row['flight_time'].strftime('%H:%M:%S')
        seats = row['empty_seat']
        result = [fname, fcompany, fdate, ftime, seats]
        return result
    return False


# display all flights
def display_flights_details():
    return sql.all_flights()