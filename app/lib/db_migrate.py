import pymongo
import numpy as np
import pandas as pd

def reset_nosql(mongo_db):
    for cname in mongo_db.list_collection_names():
        mongo_db[cname].drop()


def migrate_db(db, mongo_db):
    # TODO: proof read this
    data_user = pd.read_sql_query("SELECT * FROM user", db)
    data_attraction = pd.read_sql_query("SELECT * FROM attraction", db)
    data_attraction_type = pd.read_sql_query("SELECT * FROM attraction_type", db)
    data_review = pd.read_sql_query("SELECT * FROM review", db)
    data_travel_agency = pd.read_sql_query("SELECT * FROM travel_agency", db)
    data_tour = pd.read_sql_query("SELECT * FROM tour", db)
    data_tour_booking = pd.read_sql_query("SELECT * FROM tour_booking", db)
    data_user_travel = pd.read_sql_query("SELECT * FROM user_travel", db)
    data_user_following = pd.read_sql_query("SELECT * FROM user_following", db)
    data_attr_x_attr_type = pd.read_sql_query("SELECT * FROM attr_x_attr_type", db)

    # TODO: proof read this
    data_user = data_user.rename(columns={"user_id": "_id"})
    data_attraction = data_attraction.rename(columns={"attr_id": "_id"})
    data_attraction_type = data_attraction_type.rename(columns={"attr_type_id": "_id"})
    data_review = data_review.rename(columns={"review_id": "_id"})
    data_review['review_date'] = pd.to_datetime(data_review['review_date'])
    data_travel_agency = data_travel_agency.rename(columns={"travel_agency_id": "_id"})
    data_tour = data_tour.rename(columns={"tour_id": "_id"})
    data_tour['tour_date'] = pd.to_datetime(data_tour['tour_date'])
    data_tour_booking = data_tour_booking.rename(columns={"tour_booking_id": "_id"})
    data_user_travel = data_user_travel.rename(columns={"user_id": "_id"})
    data_user_following = data_user_following.rename(columns={"user_follower_id": "_id"})
    data_attr_x_attr_type = data_attr_x_attr_type.rename(columns={"attr_x_attr_type_id": "_id"})

