import numpy as np
import pandas as pd


def travel_gen(start, days):
    days_range = np.arange(0, days)
    date = pd.to_datetime(start) + np.random.choice(days_range)
    return date


def sql_create_tables(db):
    # create empty tables for sql db
    sql_init_query = """
    CREATE TABLE user (
        user_id INT AUTO_INCREMENT NOT_NULL PRIMARY KEY,
        full_name VARCHAR(100) NOT_NULL,
        password VARCHAR(100) NOT_NULL,
        email VARCHAR(100) NOT_NULL UNIQUE
    );

    CREATE TABLE user_following (
        user_follower_id INT NOT_NULL,
        user_followee_id INT NOT_NULL,

        PRIMARY KEY (user_follower_id, user_followee_id),
        FOREIGN KEY (user_follower_id) REFERENCES user(user_id) on delete cascade,
        FOREIGN KEY (user_followee_id) REFERENCES user(user_id) on delete cascade
    );
    
    CREATE TABLE attraction (
        attr_id INT AUTO_INCREMENT NOT_NULL PRIMARY KEY,
        attr_name VARCHAR(100) NOT_NULL UNIQUE,
        attr_desc VARCHAR(1000) NOT_NULL,
        attr_coords VARCHAR(100) NOT_NULL
    );
    
    CREATE TABLE attraction_type (
        attr_type_id INT AUTO_INCREMENT NOT_NULL PRIMARY KEY,
        attr_type_name VARCHAR(100) NOT_NULL UNIQUE,
        attr_type_desc VARCHAR(1000) NOT_NULL
    );
    
    CREATE TABLE attr_x_attr_type (
        attr_id INT NOT_NULL,
        attr_type_id INT NOT_NULL,

        PRIMARY KEY (attr_id, attr_type_id),
        FOREIGN KEY (attr_id) REFERENCES attraction(attr_id) on delete cascade,
        FOREIGN KEY (attr_type_id) REFERENCES attraction_type(attr_type_id) on delete cascade
    );
    
    CREATE TABLE user_travel (
        user_id INT NOT_NULL,
        attr_id INT NOT_NULL,

        travel_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        
        PRIMARY KEY (user_id, attr_id, travel_date),
        FOREIGN KEY (user_id) REFERENCES user(user_id) on delete cascade,
        FOREIGN KEY (attr_id) REFERENCES attraction(attr_id) on delete cascade
    );
    
    CREATE TABLE review (
        user_id INT NOT_NULL,
        attr_id INT NOT_NULL,

        review_date DATETIME CURRENT_TIMESTAMP DEFAULT,
        review_text VARCHAR(1000) NOT_NULL,
        review_rating INT NOT_NULL,
        
        PRIMARY KEY (user_id, attr_id),
        FOREIGN KEY (user_id) REFERENCES user(user_id) on delete cascade,
        FOREIGN KEY (attr_id) REFERENCES attraction(attr_id) on delete cascade
    );
    
    
    CREATE TABLE travel_agency (
        agency_id INT AUTO_INCREMENT NOT_NULL PRIMARY KEY,
        agency_name VARCHAR(100) NOT_NULL UNIQUE,
        agency_email VARCHAR(100) NOT_NULL UNIQUE,
        agency_phone VARCHAR(100) NOT_NULL UNIQUE,
        agency_address VARCHAR(100) NOT_NULL
    );
    
    CREATE TABLE tour (
        tour_id INT AUTO_INCREMENT NOT_NULL PRIMARY KEY,
        tour_price INT NOT_NULL,
        tour_date DATETIME DEFAULT,

        attr_id INT NOT_NULL,
        agency_id INT NOT_NULL,

        FOREIGN KEY (attr_id) REFERENCES attraction(attr_id) on delete cascade,
        FOREIGN KEY (agency_id) REFERENCES travel_agency(agency_id) on delete cascade
    );
    
    CREATE TABLE tour_booking (
        booking_id INT AUTO_INCREMENT NOT_NULL PRIMARY KEY,
        
        user_id INT NOT_NULL,
        tour_id INT NOT_NULL,

        booking_price INT NOT_NULL,
        booking_date DATETIME DEFAULT,

        FOREIGN KEY (user_id) REFERENCES user(user_id) on delete cascade,
        FOREIGN KEY (tour_id) REFERENCES tour(tour_id) on delete cascade,
        FOREIGN KEY (booking_price) REFERENCES tour(tour_price) on delete cascade
    )
    
    
    """

    cursor = db.cursor()
    for sub_sql_query in sql_init_query.split(";"):
        cursor.execute(sub_sql_query)
    db.commit()
    cursor.close()
    return None


def sql_insert_data(db):
    # insert data into sql db

    cursor = db.cursor()

    # insert data into user table
    user_data = pd.read_csv("app/data/users.csv")
    number_of_users = user_data.shape[0]
    sql_query = "INSERT INTO user (full_name, password, email) VALUES "
    for index, data in user_data.iterrows():
        sql_query += "('%s', '%s', '%s')," % (
            data["full_name"],
            data["password"],
            data["email"],
        )

    cursor.execute(sql_query[:-1])

    # insert data into attraction table
    attraction_data = pd.read_csv("app/data/attractions.csv")
    number_of_attractions = attraction_data.shape[0]
    sql_query = "INSERT INTO attraction (attr_name, attr_desc, attr_coords) VALUES "
    for index, data in attraction_data.iterrows():
        sql_query += "('%s', '%s', '%s')," % (
            data["attr_name"],
            data["attr_desc"],
            data["attr_coords"],
        )

    cursor.execute(sql_query[:-1])

    # insert data into attraction_type table
    attraction_type_data = pd.read_csv("app/data/attraction_types.csv")
    number_of_attraction_types = attraction_type_data.shape[0]
    sql_query = "INSERT INTO attraction_type (attr_type_name, attr_type_desc) VALUES "
    for index, data in attraction_type_data.iterrows():
        sql_query += "('%s', '%s')," % (data["attr_type_name"], data["attr_type_desc"])

    cursor.execute(sql_query[:-1])

    # attraction x attraction_type table
    attraction_x_attraction_type_data = pd.read_csv(
        "app/data/attraction_mappings.csv"
    )
    sql_query = "INSERT INTO attr_x_attr_type (attr_id, attr_type_id) VALUES "
    for index, data in attraction_x_attraction_type_data.iterrows():
        sql_query += "(%d, %d)," % (data["attr_id"], data["attr_type_id"])

    cursor.execute(sql_query[:-1])

    # insert data into user_travel table
    sql_query = "INSERT INTO user_travel (user_id, attr_id, travel_date) VALUES "
    for user in range(1, number_of_users + 1):
        random_attractions = np.random.choice(
            range(1, number_of_attractions + 1),
            np.random.randint(number_of_attractions + 1),
            replace=False,
        )
        for attraction in random_attractions:
            sql_query += " (%d, %d, '%s')," % (
                user,
                attraction,
                str(travel_gen("2020-01-01", 730)),
            )

    cursor.execute(sql_query[:-1])

    # insert data into review table
    sql_query = "INSERT INTO review (user_id, attr_id, review_date, review_text, review_rating) VALUES "
    for user in range(1, number_of_users + 1):
        random_attractions = np.random.choice(
            range(1, number_of_attractions + 1),
            np.random.randint(number_of_attractions + 1),
            replace=False,
        )
        for attraction in random_attractions:
            sql_query += " (%d, %d, '%s', '%s', %d)," % (
                user,
                attraction,
                str(travel_gen("2021-01-01", 365)),
                f"Preset Review for {attraction_data.iloc[attraction-1]['attr_name']} by user: {user_data.iloc[user-1]['full_name']}",
                np.random.randint(1, 6),
            )

    cursor.execute(sql_query[:-1])

    # insert data into travel_agency table
    # TODO : complete method to insert data into travel_agency table

    cursor.execute(sql_query[:-1])

    # insert data into user_following table
    # TODO : complete method to insert data into user_following table
    
    cursor.execute(sql_query[:-1])

    # insert data into tour table
    # TODO : complete method to insert data into tour table

    cursor.execute(sql_query[:-1])

    db.commit()

    cursor.close()

    return None


# reset sql db
def sql_empty_db(db):
    cursor = db.cursor()
    for table in [
        "user",
        "user_following",
        "attraction",
        "attraction_type",
        "attr_x_attr_type",
        "user_travel",
        "review",
        "travel_agency",
        "tour",
        "tour_booking",
    ]:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    db.commit()
    cursor.close()
    return None
