import pymysql


def get_db():
    '''
    returns the pymysql database connection object required to interact with the database.
    '''
    db = pymysql.connect("localhost", "root", "admin", "recipe_search")
    return db