from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, request, session, flash


@app.route('/')
def index():
    return render_template("login.html",)

@app.route('/register')
def register():
    print(User)
    return render_template('registration.html')

@app.route('/users/login', methods=["GET", "POST"])
def login():
    data = {
      "email":request.form["email"]
    }
    user_in_db = User.get_by_email(data)
   
    if not user_in_db:
        flash("Invalid Email")
        return redirect("/")
    print("Hashed password from DB:", user_in_db.password)
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    
    return redirect("/surfboards")

@app.route('/users/new', methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        

        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        
        email_data = {
            "email":request.form['email']
        }
   
        
        existing_user = User.get_by_email(email_data)

        if not User.validate_user(request.form):
            return redirect('/')
        # Form data is available in the request.form dictionary for POST requests.
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": request.form["password"],
            "seller": request.form["seller"],
            "buyer": request.form['buyer']
        }

        

        if existing_user:   
            flash("Already a user, please login or reset your credentials if you forgot them")
            return redirect ('/')
        else:
        # We pass the data dictionary into the save method from the User class.
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
            print(pw_hash)
            data["password"] = pw_hash
            print(data)# Don't forget to redirect after saving to the database.
            user_id = User.save(data)
            session['user_id'] = user_id

    return redirect('/surfboards')
        # Don't forget to redirect after saving to the database.
        

        # Form data is available in the request.form dictionary for POST requests
       
    # For GET requests, render the template without accessing form data.
@app.route("/logout")
def logout():
        session.clear()
        return redirect("/")