import numpy as np
import pandas as pd


def travel_gen(start, days):
    days_range = pd.to_timedelta(np.arange(0, days), unit='D')
    date = pd.to_datetime(start) + np.random.choice(days_range)
    return date


def sql_create_tables(db):
    # create empty tables for sql db
    sql_init_query = """
    CREATE TABLE user (
        user_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    );

    CREATE TABLE user_following (
        user_follower_id INT NOT NULL,
        user_followee_id INT NOT NULL,

        PRIMARY KEY (user_follower_id, user_followee_id),
        FOREIGN KEY (user_follower_id) REFERENCES user(user_id) on delete cascade,
        FOREIGN KEY (user_followee_id) REFERENCES user(user_id) on delete cascade
    );
    
    CREATE TABLE attraction (
        attr_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        attr_name VARCHAR(100) NOT NULL UNIQUE,
        attr_desc VARCHAR(1000) NOT NULL,
        attr_coords VARCHAR(100) NOT NULL
    );
    
    CREATE TABLE attraction_type (
        attr_type_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        attr_type_name VARCHAR(100) NOT NULL UNIQUE,
        attr_type_desc VARCHAR(1000) NOT NULL
    );
    
    CREATE TABLE attr_x_attr_type (
        attr_id INT NOT NULL,
        attr_type_id INT NOT NULL,

        PRIMARY KEY (attr_id, attr_type_id),
        FOREIGN KEY (attr_id) REFERENCES attraction(attr_id) on delete cascade,
        FOREIGN KEY (attr_type_id) REFERENCES attraction_type(attr_type_id) on delete cascade
    );
    
    CREATE TABLE user_travel (
        user_id INT NOT NULL,
        attr_id INT NOT NULL,

        travel_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        
        PRIMARY KEY (user_id, attr_id, travel_date),
        FOREIGN KEY (user_id) REFERENCES user(user_id) on delete cascade,
        FOREIGN KEY (attr_id) REFERENCES attraction(attr_id) on delete cascade
    );
    
    CREATE TABLE review (
        user_id INT NOT NULL,
        attr_id INT NOT NULL,
    
        review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        review_text VARCHAR(1000) NOT NULL,
        review_rating INT NOT NULL,
        
        PRIMARY KEY (user_id, attr_id),
        FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
        FOREIGN KEY (attr_id) REFERENCES attraction(attr_id) ON DELETE CASCADE
    );
    
    CREATE TABLE travel_agency (
        agency_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        agency_name VARCHAR(100) NOT NULL UNIQUE,
        agency_email VARCHAR(100) NOT NULL UNIQUE,
        agency_phone VARCHAR(100) NOT NULL UNIQUE,
        agency_address VARCHAR(100) NOT NULL
    );
    
    CREATE TABLE tour (
        tour_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        tour_price INT NOT NULL,
        tour_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
        attr_id INT NOT NULL,
        agency_id INT NOT NULL,
    
        FOREIGN KEY (attr_id) REFERENCES attraction(attr_id) ON DELETE CASCADE,
        FOREIGN KEY (agency_id) REFERENCES travel_agency(agency_id) ON DELETE CASCADE
    );
    
    CREATE TABLE tour_booking (
        booking_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        
        user_id INT NOT NULL,
        tour_id INT NOT NULL,
    
        booking_price INT NOT NULL,
        booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
        FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
        FOREIGN KEY (tour_id) REFERENCES tour(tour_id) ON DELETE CASCADE
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
    user_data = pd.read_csv("data/users.csv")
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
    attraction_data = pd.read_csv("data/attractions.csv")
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
    attraction_type_data = pd.read_csv("data/attraction_types.csv")
    number_of_attraction_types = attraction_type_data.shape[0]
    sql_query = "INSERT INTO attraction_type (attr_type_name, attr_type_desc) VALUES "
    for index, data in attraction_type_data.iterrows():
        sql_query += "('%s', '%s')," % (data["attr_type_name"], data["attr_type_desc"])

    cursor.execute(sql_query[:-1])

    # attraction x attraction_type table
    attraction_x_attraction_type_data = pd.read_csv(
        "data/attraction_mappings.csv"
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
    travel_agency = pd.read_csv("data/travel_agencies.csv")
    number_of_travel_agencies = travel_agency.shape[0]
    sql_query = "INSERT INTO travel_agency (agency_name, agency_email, agency_phone, agency_address) VALUES "
    for index, data in travel_agency.iterrows():
        sql_query += "('%s', '%s', '%s', '%s')," % (
            data["agency_name"],
            data["agency_email"],
            data["agency_phone"],
            data["agency_address"],
        )

    cursor.execute(sql_query[:-1])

    # insert data into user_following table
    generated_pairs = set()
    sql_query = "INSERT INTO user_following (user_follower_id, user_followee_id) VALUES "
    for _ in range(number_of_users * 3):
        user_follower_id = np.random.randint(1, number_of_users+1)
        user_followee_id = np.random.randint(1, number_of_users+1)

        while user_followee_id == user_follower_id or (user_follower_id, user_followee_id) in generated_pairs:
            user_followee_id = np.random.randint(1, number_of_users+1)

        generated_pairs.add((user_follower_id, user_followee_id))

        sql_query += " (%d, %d)," % (
            user_follower_id,
            user_followee_id
        )

    cursor.execute(sql_query[:-1])

    # insert data into tour table
    sql_query = "INSERT INTO tour (tour_price, tour_date, attr_id, agency_id) VALUES "
    # List to store tour details
    tours_list = []
    tour_id = 1
    for _ in range(number_of_travel_agencies * 3):
        tour_price = np.random.randint(100, 800)
        tour_date = str(travel_gen("2020-01-01", 730))
        attr_id = np.random.randint(1, number_of_attractions + 1)
        agency_id = np.random.randint(1, number_of_travel_agencies + 1)

        tours_list.append({
            "tour_id": tour_id,
            "tour_price": tour_price,
            "tour_date": tour_date
        })

        sql_query += " (%d, '%s', %d, %d)," % (
            tour_price,
            tour_date,
            attr_id,
            agency_id,
        )

        tour_id += 1

    cursor.execute(sql_query[:-1])

    # insert data into tour_booking table
    sql_query = "INSERT INTO tour_booking (user_id, tour_id, booking_price, booking_date) VALUES "
    for _ in range(50):
        random_tour = np.random.choice(tours_list)
        sql_query += " (%d, %d, %d, '%s')," % (
            np.random.randint(1, number_of_users + 1),
            random_tour["tour_id"],
            random_tour["tour_price"] + np.random.randint(-20, 20),  # A random difference from actual tour price
            str(travel_gen(random_tour["tour_date"], 365)),  # A random date after the tour date
        )

    cursor.execute(sql_query[:-1])

    db.commit()

    cursor.close()

    return None


# reset sql db
def sql_empty_db(db):
    cursor = db.cursor()
    for table in [
            "tour_booking",
            "tour",
            "travel_agency",
            "review",
            "user_travel",
            "attr_x_attr_type",
            "attraction_type",
            "attraction",
            "user_following",
            "user"
    ]:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    db.commit()
    cursor.close()
    return None
