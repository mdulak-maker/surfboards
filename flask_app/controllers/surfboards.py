from flask_app import app
from flask_app.models.surfboard import Surfboard
from flask_app.models.user import User
from flask import render_template, redirect, request, session, flash
from werkzeug.utils import secure_filename
from werkzeug.utils import safe_join
import os


@app.route("/surfboards")
def dashboard():
    #check if user ID is in session
    if 'user_id' not in session:
        flash("You must be logged in to view this page.")
        return redirect("/") 
    
    all_surfboards = Surfboard.get_all_surfboards_with_users()
     # Retrieve the user ID from the session
    user_id = session['user_id']
    data = {'id': user_id}
    # Retrieve the user's information using the user ID
    user = User.get_by_id(data) # Assuming you have a method to get a user by ID
    surfboard_id = {"id": id} #setting surfboard ID
    surfboard = Surfboard.get_surfboard_by_id(surfboard_id)
    return render_template("Dashboard.html", all_surfboards=all_surfboards, user=user, surfboard = surfboard)
    
@app.route("/surfboards/new", methods = ["GET",'POST'])
def add_surfboard():
    if 'user_id' not in session:
        flash("You must be logged in to view this page.")
        return redirect("/") 
    
    if request.method == "POST":
        # Check for file first (whether it's empty, etc.)
        file = request.files['image']
        
        if file.filename == '':
            flash('No selected file')
            return redirect("/surfboards/new")
        
        os.makedirs('static/img', exist_ok=True) #make the directory/ensure that it exists
        filename = secure_filename(file.filename)
        file_path = safe_join(app.root_path, 'static', 'img', filename)  # Uses an absolute path
        file.save(file_path)
        user_id = session['user_id']
        data = {
            "user_id": user_id,
            "board_name": request.form["board_name"],
            "volume": request.form["volume"],
            "price": request.form['price'],
            "image": filename,  # store just the filename in database
            "shaper": request.form["shaper"],
            "year": request.form["year"],
        }
    
        if not Surfboard.validate_surfboard(request.form):
            return redirect('/surfboards/new')
        else:
            print("Data dictionary before saving:", data)
            Surfboard.save(data)
            print(data)
            return redirect("/surfboards")

    return render_template("addSurfboard.html")

@app.route("/surfboards/update", methods = ["GET",'POST'])
def edit_surfboard():
    if request.method == "POST":
    
        id = request.form['id']
        data = {
            "id": id,
            "board_name": request.form["board_name"],
            "shaper": request.form["shaper"],
            "volume": request.form["volume"],
            "price": request.form["price"],
            "year": request.form["year"],
            "image": request.form["image"]
        }
        if not Surfboard.validate.surfboard(request.form):
            return redirect(f'/surfboards/edit/{id}')
        else:
            Surfboard.update(data)
            print(data)
            return redirect("/surfboards")
    return redirect("/surfboards")

@app.route("/delete", methods = ["post", "get"])
def delete():
    id = request.form['surfboard_id']
    Surfboard.delete_surfboards(id)
    return redirect("/surfboards")

@app.route('/surfboards/<int:id>', methods=["GET"])
def get_surfboard_by_id(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page.")
        return redirect("/") 
    print(f"Accessing surfboard with ID: {id}") # Debug print
    
    user_id = session['user_id']
    data = {'id': user_id}
    # Retrieve the user's information using the user ID
    user = User.get_by_id(data)
    surfboard_id = {"id": id}
    surfboard = Surfboard.get_surfboard_by_id(surfboard_id)
    print(surfboard.shaper)

    print(f"Surfboard retrieved: {surfboard}") # Debug print
    return render_template('showSurfboard.html',surfboard=surfboard, user = user)
    
@app.route('/surfboards/edit/<int:id>', methods = ["POST", "GET"])
def get_surfboard_by(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page.")
        return redirect("/") 
    print(f"Accessing surfboard with ID: {id}") # Debug print
    surfboard_id = {"id": id}
    surfboard = Surfboard.get_surfboard_by_id(surfboard_id)
    print(surfboard.year)
    print(f"Recipe retrieved: {surfboard}") # Debug print
    return render_template('editSurfboard.html',surfboard = surfboard)

