from flask import Flask, session, flash, g, redirect, url_for, escape, request, render_template, jsonify
import sqlite3
import configparser

config =configparser.ConfigParser()
config.read('conf.ini')
secret_key=config.get('CONFIG','secret_key')
database=config.get('CONFIG','database')
your_username=config.get('ACCOUNT','my_username')


conn = sqlite3.connect(database) #connexion a la DB
cursor = conn.cursor() # definition cursor

#creation de la table
cursor.execute("""CREATE TABLE IF NOT EXISTS donnees
                  (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                   date_modif DATE,
                   description TEXT,
                   statut  TEXT,
                   texte TEXT)""")


conn.commit() #validation des modifications
conn.close() #fermeture de la connexion a la db


def db_func_select_id(database,id_modif):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM donnees WHERE id=? """,(id_modif,))
    rows=cursor.fetchone()
    conn.close()
    return rows


def db_func_list(database):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""select * from donnees""")
    rows = cursor.fetchall()
    conn.close()
    return rows


def db_func_delete(database,mon_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM donnees WHERE id=?""",(mon_id,))
    conn.commit()
    conn.close()
    return 0

def db_func_add(database,date,description,statut,texte):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO donnees (date_modif,description,statut,texte) VALUES(?,?,?,?)""",(date,description,statut,texte,))
    conn.commit()
    conn.close()
    return 0

def db_func_edit(database,date,description,statut,texte,id_edit):
    conn =sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(''' UPDATE donnees SET date_modif = ?,description = ?,statut = ?,texte = ? WHERE id=? ''',(date,description,statut,texte,id_edit,))
    conn.commit()
    conn.close()
    return 0


agenda = Flask(__name__)

agenda.secret_key = secret_key

@agenda.route("/connexion")
def connexion():
    return render_template('connexion.html')

@agenda.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == your_username:
            session['username'] = request.form['username']
            return redirect(url_for('tab'))
    return redirect(url_for('connexion'))


@agenda.route('/tab')
def tab():
    if 'username' in session:
        return render_template('tab.html', rows=db_func_list(database))


@agenda.route('/form_ajout')
def form_ajout():
    return render_template("form_ajout.html")

@agenda.route('/form_edit', methods=['POST'])
def form_edit():
    id_modif=request.form['edit']
    session['id_selected'] = id_modif
    return render_template('form_edit.html',rows=db_func_select_id(database,id_modif))



@agenda.route('/db_add', methods=['post'])
def db_add():
    date=request.form['date']
    description=request.form['description']
    statut=request.form['statut']
    texte=request.form['texte']
    db_func_add(database,date,description,statut,texte)
    #TODO pop JS "blabla ok"
    return redirect(url_for('tab'))



@agenda.route('/db_remove', methods=['post'])
def db_remove():
    mon_id=session.pop('id_selected',None)
    db_func_delete(database,mon_id)
    #TODO requete remove + JS
    return redirect(url_for('tab'))

@agenda.route('/db_edit', methods=['post'])
def db_edit():
    date=request.form['date']
    description=request.form['description']
    statut=request.form['statut']
    texte=request.form['texte']
    mon_id=session.pop('id_selected',None)
    db_func_edit(database,date,description,statut,texte,mon_id)
    return redirect(url_for('tab'))

@agenda.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('connexion'))


#FOR TESTING

@agenda.route('/test')
def test():
        return render_template('test.html')

@agenda.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
