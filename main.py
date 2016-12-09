from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import requests

mysql = MySQL()
app = Flask(__name__)


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'toor'
app.config['MYSQL_DATABASE_DB'] = 'Speeddating'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        result = request.form
        ack = requests.post("https://amiv-apidev.vsos.ethz.ch/sessions", data={"user" : str(result['nethz']), "password" : str(result['password'])}, verify=False)
        if ack.status_code == 201:
            return render_template("admin.html")
        return render_template('login.html')
    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        result = request.form
        prename1 = str(result['prename'])
        name1 = str(result['name'])
        con = mysql.connect()
        cursor = con.cursor()
        sql = "INSERT INTO Person (Name,Prename) VALUES (?,?)"
        cursor.execute(sql, (name1,prename1))
        con.commit()
        con.close()   
        return render_template('signup.html')
    return render_template('signup.html')



if __name__ == '__main__':
   app.run()
