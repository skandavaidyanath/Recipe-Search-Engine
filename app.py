from flask import Flask, render_template, url_for, request, flash, redirect, session
from passlib.hash import sha256_crypt
import pymysql
import requests
import json
import pickle

from db import get_db
from search import get_docs
from trie import TrieNode
from spellcheck import SpellChecker
from search_bar import bar
from update_database import update_database_click


trie = None
spellcheck = None
app = Flask(__name__)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    handler for login page.
    '''
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        sql = "SELECT ID, USERNAME, PASSWORD FROM USERS WHERE USERNAME = '" + \
            request.form['username'] + "'"
        try:
            cursor.execute(sql)
            number = cursor.rowcount
            if number == 0:
                flash('REGISTER FIRST!')
                return redirect(url_for('login'))
            else:
                row = cursor.fetchone()
                password = row[2]
                if sha256_crypt.verify(request.form['password'], password):
                    session['logged_in'] = True
                    session['user_id'] = row[0]
                    return redirect(url_for('home'))
                else:
                    flash("INCORRECT CREDENTIALS")
                    return render_template('login.html')
        except Exception as e:
            print(e)
            db.rollback()
        db.close()
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    handler for register page.
    '''
    if request.method == 'POST':
        for value in request.form.values():
            if value == "":
                flash('NO FIELD SHOULD BE EMPTY')
                return redirect(url_for('register'))
        password = request.form['password']
        password2 = request.form['password2']
        if password != password2:
            flash("PASSWORDS DON'T MATCH")
            return redirect(url_for('register'))
        db = get_db()
        cursor = db.cursor()
        sql = 'SELECT USERNAME FROM USERS WHERE USERNAME = "' + \
            request.form['username'] + '"'

        try:
            cursor.execute(sql)
            number = cursor.rowcount
            if number != 0:
                flash('ERROR: USERNAME ALREADY EXISTS')
                return redirect(url_for('register'))
        except Exception as e:
            print(e)
            db.rollback()
            db.close()

        hashed = sha256_crypt.encrypt(password)
        sql = "INSERT INTO USERS VALUES(null,'" + \
            request.form['username'] + "', '" + hashed + "');"
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
        db.close()
        flash('Successfully Registered!')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout', methods=['GET'])
def logout():
    '''
    handler for logout functionality.
    '''
    session['logged_in'] = False
    session['user_id'] = -1
    flash("Logged out")
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    '''
    handler for search page
    '''
    if 'logged_in' in session and not session['logged_in']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        return render_template('index.html', results=get_docs(request.form['query']))
    return render_template('index.html', results=[])


@app.route('/result/', methods=['GET'])
def result():
    '''
    handler for the result page.
    it also makes sure clicks are stored in the database.
    '''
    if 'logged_in' in session and not session['logged_in']:
        return redirect(url_for('login'))
    update_database_click(session['user_id'], request.args.get('docId'))
    return render_template('result.html',
                           dish_name=request.args.get('dish_name'),
                           ingredients=request.args.get('ingredients'),
                           directions=request.args.get('directions'),
                           recipe_links=request.args.get('recipe_links'))


@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    '''
    handler to serve autocomplete data.
    '''
    text = request.form['text']
    results = bar(spellcheck, trie, text)
    if results:
        return json.dumps(results[:10])
    else:
        return json.dumps([])


if __name__ == '__main__':
    with open('my_trie.pickle', 'rb') as fp:
        trie = pickle.load(fp)
    with open('my_spellchecker.pickle', 'rb') as fp:
        spellcheck = pickle.load(fp)
    app.config.from_object(__name__)
    app.config.update(dict(SECRET_KEY='development key',))
    app.run(debug=True)