import pymysql
import random
import pickle
from db import get_db
import json


def update_database_click(userid, docid):
    '''
    Every time a user opens a recipe, it is updated in the database to show the user clicks using this function
    We will use this database to create trainign and test data for the recommender system.
    '''
    sql = "SELECT * FROM user_clicks WHERE USERID = " + \
        str(userid) + " AND DOCID = " + str(docid)
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        number = cursor.rowcount
        if number == 0:
        # New user-document pair, insert a new row in the table.
            try:
                sql = "INSERT INTO user_clicks VALUES(NULL," + str(
                    userid) + "," + str(docid) + ", 1, NULL)"
                cursor.execute(sql)
                db.commit()
                print('Successfully inserted new user-document pair')
            except Exception as e:
                print(e)
                print('Error in inserting a new user-document pair')
                db.rollback()
        else:
            try:
            # Old user-document pair. Just update the number of clicks.
                sql = "SELECT CLICKS FROM user_clicks WHERE USERID = " + \
                    str(userid) + " AND DOCID = " + str(docid)
                cursor.execute(sql)
                row = cursor.fetchone()
                clicks = row[0]
                if clicks < 50:
                    sql = "UPDATE user_clicks SET CLICKS = CLICKS + 1 WHERE USERID = " + \
                        str(userid) + " AND DOCID = " + str(docid)
                    cursor.execute(sql)
                    db.commit()
                    print('Successfully updated clicks ' + str(clicks + 1))
            except Exception as e:
                print(e)
                print('Error in updating clicks of existing user')
                db.rollback()
    except Exception as e:
        print(e)
        print('Error in checking if user is present')
        db.rollback()
    db.close()


def create_random_data(users, documents):
    '''
    Fills the database with random data to test the system.
    Creates random user-document pairs.
    '''
    for _ in range(100000):
        user_data = random.randint(min(users), max(users))
        document_data = random.randint(min(documents), max(documents))
        update_database_click(user_data, document_data)


def main():
    '''
    Fills the database with random data to test the system.
    '''
    db = get_db()
    cursor = db.cursor()
    nb_users = 0
    try:
        sql = "SELECT COUNT(*) FROM USERS"
        cursor.execute(sql)
        row = cursor.fetchone()
        nb_users = row[0]
    except Exception as e:
        print(e)
        db.rollback()
    db.close()
    fp = open("corpus/dish_names_dict.json", "r")
    corpus = json.load(fp)
    fp.close()
    nb_documents = len(corpus)
    users = [i+1 for i in range(nb_users)]
    documents = [(i + 1) for i in range(nb_documents)]
    create_random_data(users, documents)


def setup_db():
    '''
    Setting up the database by creating the necessary tables.
    users - the details of users in the system
    user_clicks - gives details about when the user-document apirs and the number of clicks for each document by a given user. 
    '''
    db = get_db()
    cursor = db.cursor()
    sql = 'create table users (id int auto_increment, username varchar(20), password varchar(256), primary key (id));'
    cursor.execute(sql)
    sql = 'create table user_clicks (id int auto_increment, userid int, docid int, clicks int, primary key (id));'
    cursor.execute(sql)
    cursor.close()
    db.close()


if __name__ == '__main__':
    # main()
    setup_db()
