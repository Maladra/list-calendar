from flask import Flask, session, flash, g, redirect, url_for, escape, request, render_template, jsonify
import sqlite3

conn = sqlite3.connect('tableau.db') #connexion a la DB
cursor = conn.cursor() # definition cursor

#creation de la table
cursor.execute("""CREATE TABLE IF NOT EXISTS donnees
                  (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                   date_modif DATE,
                   description TEXT,
                   statut  TEXT,
                   texte TEXT)""")

#remplissage table a remove
i=0
while i <20:
    cursor.execute("""INSERT INTO donnees (date_modif,description,statut,texte) VALUES(?,?,?,?)""", ("1999-03-20",'description','statut','texte3'))
    #possibilité de passer par un dico
    i=i+1


conn.commit() #validation des modifications
conn.close() #fermeture de la connexion a la db


agenda = Flask(__name__)

agenda.secret_key = #Your_Secret_Key


@agenda.route("/")
def index():
    if 'username' in session:
        return render_template ('index.html')
    return redirect(url_for('connexion'))

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
        conn = sqlite3.connect('tableau.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""select * from donnees""")
        rows = cursor.fetchall()
        conn.close()
        return render_template('tab.html', rows=rows)


@agenda.route('/form_ajout')
def form_ajout():
    return render_template("form_ajout.html")


@agenda.route('/db_add', methods=['post'])
def db_add():
    date=request.form['date']
    description=request.form['description']
    statut=request.form['statut']
    texte=request.form['texte']
    conn = sqlite3.connect('tableau.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO donnees (date_modif,description,statut,texte) VALUES(?,?,?,?)""",(date,description,statut,texte))
    conn.commit()
    conn.close()
    #TODO pop JS "blabla ok"
    return redirect(url_for('tab'))

@agenda.route('/db_remove')
def db_remove():
    conn = sqlite3.connect('tableau.db')
    cursor = conn.cursor()
    mon_id=request.form['mon_id']
    cursor.execute("""
    DELETE FROM donnees WHERE id=?""",(mon_id,))
    conn.commit()
    conn.close()
    #TODO requete remove + FLASH

    return redirect(url_for('tab'))

@agenda.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('connexion'))

@agenda.route('/test')
def test():
        return render_template('test.html')

@agenda.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
