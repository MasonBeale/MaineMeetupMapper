'''
analytics.py
Functions for getting simple analytics from the database
need to add more stuff
currently assumes theres a connection to the db but im not sure how to do that yet
@author Mason Beale
'''
def get_total_users(cursor):
    cursor.execute("SELECT COUNT(user_id) FROM User;")
    result = cursor.fetchone()
    return result[0]

def get_total_events(cursor):
    cursor.execute("SELECT COUNT(event_id) FROM Event;")
    result = cursor.fetchone()
    return result[0]

def get_total_locations(cursor):
    cursor.execute("SELECT COUNT(location_id) FROM Location;")
    result = cursor.fetchone()
    return result[0]

def get_popular_events(cursor, limit):
    # sort rsvps by event id USE INDEXES
    # count number of rsvps per event
    # return top events
    pass

def get_active_users(cursor, limit):
    # sort rsvps by user id USE INDEXES
    # count number of rsvps per user
    # return top users
    pass


# below might not be analytics technically but whatever also all ai from here down

def get_event_attendance(cursor, event_id):
    cursor.execute("SELECT COUNT(user_id) FROM RSVP WHERE event_id = %s;", (event_id,)) # use index, also this is weird ai syntax
    result = cursor.fetchone()
    return result[0]

def get_user_rsvps(cursor, user_id):
    cursor.execute("SELECT event_id FROM RSVP WHERE user_id = %s;", (user_id,))
    result = cursor.fetchall()
    return [row[0] for row in result]