from flask import Flask, render_template, request, redirect, url_for, session
from data import *

app = Flask(__name__)

app.secret_key = 'watubs'

#----------------------------------------Basic Display Pages---------------------------------------------------------- #

#Displays the Homepage
@app.route('/')
def homepage():
    return render_template("homepage.html")

#Displays Priacy Notice Page
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

#Displays Account Registration Page
@app.route('/account_register')
def account_register():
    return render_template("account_create.html")

#Displays Login Pge
@app.route("/account_login")
def login():
    return render_template("login.html")

#Displays the Login Page with an error message when inputting credentials not in the database
@app.route("/account_login/failed")
def retry():
    return render_template("retry.html")

#Displays the Account Registration Page with an error message when inputting an email already in the database
@app.route("/account_creation/failed")
def dupe():
    return render_template("dupe.html")



#-----------------------------------------Account Handling Functions---------------------------------------------------#

#Inputs the given account credentials into the accounts database
@app.route('/creating', methods=['POST'])
def account_creation():
    account_data = {'email': request.form['email'].lower(),
                    'password': request.form['password'].lower(),
                    'type': 'Regular'
                    }

    #Checks if the email is already in the database. Redirects to the dupe page if it is and inputs into database if it is not
    dupe = check_dupe(account_data['email'])
    if dupe is False:
        return redirect(url_for('dupe'))
    else:
        insert_account(account_data)
        return redirect(url_for('homepage'))

#Verifies login credentials and upon success declares session variables
@app.route("/verifying", methods=['POST'])
def signin():
    account_data = {'email': request.form['email'].lower(),
                    'password': request.form['password'].lower(),
                    'type': 'Regular'
                    }
    verify = login_account(account_data['email'], account_data['password'])

    #Redirects to login failed
    if verify is False:
        return redirect(url_for('retry'))
    else:
        #Create session data, we can access this data in other routes
        session['loggedin'] = True
        session['id'] = verify['id']
        session['email'] = verify['email']
        session['type'] = verify['type']
        #Redirect to home page
        return redirect(url_for('homepage'))

#Removes session variables
@app.route("/accountlogout")
def logout():
    #Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   session.pop('type', None)
   #Redirect to login page
   return redirect(url_for('homepage'))


#-------------------------------------------Application Form-----------------------------------------------------------#

#Displays the application form
@app.route("/application/<email>")
@app.route("/application")
def application():
    #Checks if user is logged in.
    #If they are an admin they can access the masterlist
    #If they are logged in, they can access the form.
    #If not logged in, redirects to login page
    if 'loggedin' in session:
        #Checks if the user has already filled out the form
        verify = check_application(session['email'])
        if session['type'] == "Admin":
            return redirect(url_for('masterlist'))
        #If user has not filled out the form, directs to the application form
        elif verify is False:
            return render_template("application.html")
        #If user has already filled out the form, directs to the application review page
        else:
            return render_template('review.html', account=verify)
    else:
        return redirect(url_for('login'))

#Receives data from application form and stores in the database
@app.route('/inputting', methods=['post'])
def apply():
    app_data = {
                'firstname': request.form['firstname'],
                'lastname': request.form['lastname'],
                'sex': request.form['sex'],
                'civil': request.form['marital'],
                'birthdate': request.form['birthdate'],
                'birthplace': request.form['birthplace'],
                'citizenship': request.form['citizen'],
                'religion': request.form['religion'],
                'landline': request.form['landlinephone'],
                'mobile': request.form['mobilephone'],
                'street1': request.form['street1'],
                'street2': request.form['street2'],
                'city': request.form['city'],
                'state': request.form['state'],
                'country': request.form['country'],
                'zip': request.form['zip'],
                'url': request.form['imageurl'],
                'apptype': request.form['applicationtype'],
                'semester': request.form['semester'],
                'campus': request.form['campus'],
                'course': request.form['course'],
                'email': session['email']
                }
    insert_application(app_data)
    return redirect(url_for('application'))


#----------------------------------------View Application Forms--------------------------------------------------------#

#Retreives all applications from the database and renders the masterlist
@app.route('/masterlist')
def masterlist():
    application = retreive_masterlist()
    return render_template('masterlist.html', applications=application)

#Shows the Application Review Page with a back button to go back to master list
@app.route("/processing/<appid>")
def adminview(appid):
    application = read_app_by_id(appid)
    return render_template('back_review.html', account=application)

#Receives search query from the masterlist and returns a new masterlist with all valid searches
@app.route('/search', methods=['POST'])
def fieldsearch():
    field = request.form['field']
    search = request.form['search']
    result = field_search(field, search)
    if result is False:
        return render_template('noresult.html')
    else:
        return render_template('searchML.html', applications=result)


#----------------------------------------Edit Application Forms--------------------------------------------------------#

#Receives application details and either redirects to edit page or deletes the application
@app.route('/modify/<email>', methods=['POST'])
def modify(email):
    application = check_application(email)
    if request.form['action'] == 'Edit':
        return render_template('edit.html', account=application)
    elif request.form['action'] == 'Delete':
        delete_application(email)
        return redirect(url_for('application'))

#Upon edit confirmation, updates the values in the database
@app.route('/update/<email>', methods=['POST'])
def update(email):
    app_data = {
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'sex': request.form['sex'],
        'civil': request.form['marital'],
        'birthdate': request.form['birthdate'],
        'birthplace': request.form['birthplace'],
        'citizenship': request.form['citizen'],
        'religion': request.form['religion'],
        'landline': request.form['landlinephone'],
        'mobile': request.form['mobilephone'],
        'street1': request.form['street1'],
        'street2': request.form['street2'],
        'city': request.form['city'],
        'state': request.form['state'],
        'country': request.form['country'],
        'zip': request.form['zip'],
        'url': request.form['imageurl'],
        'apptype': request.form['applicationtype'],
        'semester': request.form['semester'],
        'campus': request.form['campus'],
        'course': request.form['course'],
        'email': email
    }
    update_application(app_data)
    return redirect(url_for('application'))


if __name__ == '__main__':
    app.run(debug=True)