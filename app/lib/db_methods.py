import numpy as np
import pandas as pd

# Saksham use case 1 -create user-----------------------------------------------
def create_user(db, mongo_db, user_name, user_email, user_password, db_type):
    #sql
    if db_type == 'sql':
        db.execute('INSERT INTO user (name, email, password) VALUES (?, ?, ?)', (user_name, user_email, user_password))
        db.commit()
    #mongo
    elif db_type == 'mongo':
        mongo_db.users.insert_one({'name': user_name, 'email': user_email, 'password': user_password})

# get user by email
def get_user_by_email(db, mongo_db, user_email, db_type):
    #sql
    if db_type == 'sql':
        user = db.execute('SELECT * FROM user WHERE email = ?', (user_email,)).fetchone()
        return user
    #mongo
    elif db_type == 'mongo':
        user = mongo_db.users.find_one({'email': user_email})
        return user
    else:
        return None
    
# get user by id
def get_user(db, mongo_db, user_id, db_type):
    #sql
    if db_type == 'sql':
        user = db.execute('SELECT * FROM user WHERE user_id = ?', (user_id,)).fetchone()
        return user
    #mongo
    elif db_type == 'mongo':
        user = mongo_db.users.find_one({'_id': user_id})
        return user
    else:
        return None
    
# get user by id
def get_all_attractions(db, mongo_db, db_type):
    # sql
    if db_type == 'sql':
        attractions = db.execute('SELECT * FROM attraction').fetchall()
        return attractions
    # mongo
    elif db_type == 'mongo':
        attractions = mongo_db.attractions.find()
        return attractions

# get attraction by id
def get_attraction(db, mongo_db, attraction_id, db_type):
    # sql
    if db_type == 'sql':
        attraction = db.execute('SELECT * FROM attraction WHERE attraction_id = ?', (attraction_id,)).fetchone()
        return attraction
    # mongo
    elif db_type == 'mongo':
        attraction = mongo_db.attractions.find_one({'_id': attraction_id})
        return attraction
    
# Saksham use case 2 -mark attraction as visited-----------------------------------------
def mark_visited(db, mongo_db, user_id, attraction_id, date_visited, db_type):
    #sql 
    if db_type == 'sql':
        db.execute('INSERT INTO user_travel (user_id, attraction_id, date_visited) VALUES (?, ?, ?)', (user_id, attraction_id, date_visited))
        db.commit()
    #mongo
    elif db_type == 'mongo':
        mongo_db.user_travel.insert_one({'user_id': user_id, 'attraction_id': attraction_id, 'date_visited': date_visited})

# get all agencies
def get_all_agencies(db, mongo_db, db_type):
    # sql
    if db_type == 'sql':
        agencies = db.execute('SELECT * FROM agency').fetchall()
        return agencies
    # mongo
    elif db_type == 'mongo':
        agencies = mongo_db.agencies.find()
        return agencies
    
# get agency by id
def get_agency(db, mongo_db, agency_id, db_type):
    # sql
    if db_type == 'sql':
        agency = db.execute('SELECT * FROM agency WHERE agency_id = ?', (agency_id,)).fetchone()
        return agency
    # mongo
    elif db_type == 'mongo':
        agency = mongo_db.agencies.find_one({'_id': agency_id})
        return agency

# get all tours by an agency
def get_all_tours(db, mongo_db, agency_id, db_type):
    # sql
    if db_type == 'sql':
        tours = db.execute('SELECT * FROM tour WHERE agency_id = ?', (agency_id,)).fetchall()
        return tours
    # mongo
    elif db_type == 'mongo':
        tours = mongo_db.tours.find({'agency_id': agency_id})
        return tours
    
# get tour by id
def get_tour(db, mongo_db, tour_id, db_type):
    # sql
    if db_type == 'sql':
        tour = db.execute('SELECT * FROM tour WHERE tour_id = ?', (tour_id,)).fetchone()
        return tour
    # mongo
    elif db_type == 'mongo':
        tour = mongo_db.tours.find_one({'_id': tour_id})
        return tour
    
def create_booking(db, mongo_db, user_id, tour_id, booking_date, db_type):
    booking_date = get_tour(db, mongo_db, tour_id, db_type)['date']
    
    #sql 
    if db_type == 'sql':
        db.execute('INSERT INTO user_tour (user_id, tour_id, booking_date) VALUES (?, ?, ?)', (user_id, tour_id, booking_date))
        db.commit()
    #mongo
    elif db_type == 'mongo':
        mongo_db.user_tour.insert_one({'user_id': user_id, 'tour_id': tour_id, 'booking_date': booking_date})