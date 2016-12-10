from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests

#create app
app = Flask(__name__)

#setup sql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:toor@localhost/Speeddating'
db = SQLAlchemy(app)



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
        prename = str(result['prename'])
        name = str(result['name'])
        # # con = mysql.connect()
        #cursor = con.cursor()
        # sql = "INSERT INTO Person (Name,Prename) VALUES (?,?)"
        # cursor.execute(sql, (name,prename))
        #con.commit()
        #con.close()
        return render_template('signup.html')
    return render_template('signup.html')



if __name__ == '__main__':
   app.run()
