from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
db = yaml.load(open('db.yaml'), Loader=yaml.Loader)
#Configure DB
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #Fetch form data
        userDetails = request.form
        name = userDetails['name']
        age = userDetails['age']
        gender = userDetails['gender']
        city = userDetails['city']
        email = userDetails['email']
        phone = userDetails['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO USERS(name, age, gender, city, email, phone) VALUES (%s, %s, %s, %s, %s, %s)",(name, age, gender, city, email, phone))
        mysql.connection.commit()
        cur.close()
        return redirect('/home')
    return render_template("index.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT * FROM USERS")
    if resultVal > 0:
        userDetails = cur.fetchall()
        print(userDetails)
        return render_template('users.html', userDetail=userDetails)

if __name__=='__main__':
    app.run(debug=True)