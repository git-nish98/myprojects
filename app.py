from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash , check_password_hash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.secret_key = "your_secret_key"

#Configure SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db = SQLAlchemy(app)

#Datebase Model ~ single row within our db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25),unique=True, nullable=False )
    hash_password = db.Column(db.String(150), nullable=False)
    
    def set_password(self,password):
        self.hash_password = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.hash_password,password)


#Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

#Login
@app.route("/login", methods=["POST" , "GET"])
def login():
    #Collect infp from the form
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username']=username
        return redirect(url_for('dashboard'))
    else:
        return render_template("register.html")
    #Check if it is in the DB 
    #Otherwise show home page


#Register
@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user :
        return render_template("index.html", error="User already here!")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session["username"]=username
        return redirect(url_for('dashboard'))    
#Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("home.html", username=session["username"])
    

@app.route('/main')
def main():
    return render_template('home.html' , username=session["username"])

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/aipage')
def aipage():
    return render_template('aihome.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')  
#Forgot pass

@app.route("/forgotpass")
def forgotpass():
    return render_template("fpass.html")
    
@app.route("/updatepass",methods=["POST"])
def updatepass():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user :
        user.password = user.set_password(password)
        db.session.commit()
    return redirect(url_for('home'))
            

#Logout
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)