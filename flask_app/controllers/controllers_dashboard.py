from flask_app import app
from flask import request, redirect, render_template, flash, session
from flask_app.models.users import Users
from flask_app.models.dashboard import Dashboard
from flask_app.models import application
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)





@app.route('/')
def index():
    return render_template("dashboard.html")

@app.route('/register/form', methods=["POST"])
def register_form():
    banana = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'], 
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password':banana,
    }
    if Users.is_valid(request.form):
        id = Users.register(data)
        session['user_id']= id    
        return redirect("/main")
    return redirect('/')

@app.route('/login/form', methods = ['POST'])
def login_form():
    data = {'email': request.form['email']}
    user_in_db = Users.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/ Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/main")

@app.route("/main")
def main():
    if not session:
        return redirect ('/')
    data = {'id': session['user_id']}
    return render_template("main.html", user = Users.get_one(data), 
                            bulding = Dashboard.get_all())

@app.route('/one/apartment/<int:id>')
def one_apartment(id):
    data = {"id": id}
    user_data = {"id": session['user_id']}
    apartment = Dashboard.get_one(data)
    return render_template("one.html", apartment = apartment, user = Users.get_one(user_data), Application = application.Application)

@app.route('/join/user/apartment', methods=['POST'])
def join_user():
    data = {"building_id": request.form['building_id'], 'applicant_id': request.form['applicant_id']}
    # Check if the user has already applied to the apartment
    if application.Application.has_user_applied(data):
        error_message = "You have already applied to this apartment."
        return render_template("application.html", error_message=error_message)
    # Join the user to the building
    application.Application.join_user_to_building(request.form)
    return redirect("/application")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/apply/building/<int:id>")
def apply_building(id):
    data = {"id": id}
    user_data = {"id": session['user_id']}
    apartment = Dashboard.get_one(data)
    return render_template("application.html", 
                            apartment = apartment, 
                            user = Users.get_one(user_data))

@app.route('/update/application/<int:id>/<int:building_id>')
def update_applict(id, building_id):
    print(id)
    data= {'id': id}
    building_data = {'id': building_id}
    user_data = {'id': session['user_id']}
    application_single =  application.Application.get_one(data)
    apartment = Dashboard.get_one(building_data)
    return render_template('update.html',application_single=application_single, 
                                        apartment = apartment, 
                                        user = Users.get_one(user_data) )

@app.route('/update/form', methods=["POST"])
def second_form():
    application.Application.join_user_to_building(request.form)
    return redirect("/profile")

@app.route('/delete/application/<int:id>')
def deleteapplication(id):
    data = {'id': id}
    application.Application.deleteApplication(data)
    return redirect('/profile')

@app.route('/profile')
def profile():
    user_data = {"id": session['user_id']}
    applications = application.Application.join_application_and_user(user_data)
    return render_template('profile.html',applications=applications, user = Users.get_one(user_data))

@app.route('/update/form/applicaiton', methods=['POST'])
def update_form_itself():
    user_data ={'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'user_py_id': request.form['user_id'],
                'password': request.form['password'],
                'email': request.form['email']}
    application_data = {'building_id': request.form['building_id'],
                        'applicant_id': request.form['applicant_id'],
                        'last_address': request.form['last_address'],
                        'income': request.form['income'],
                        'birthday': request.form['birthday'],
                        'moving_date': request.form['moving_date'],
                        'id': request.form['id']}   
    Users.update_user(user_data)
    application.Application.join_user_to_building_update(application_data)
    return redirect('/profile')


