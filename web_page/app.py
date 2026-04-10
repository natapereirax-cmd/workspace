#API feita com FLASK para ter acesso às rotas do site

from flask import Flask, render_template, request, jsonify
from user.user_service import create_user
from user.user_repository import email_exists

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Nate_workspace2000'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    
    data = request.get_json()

    firstname = data.get('firstname')
    lastname = data.get('lastname')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([firstname, lastname, email, password, username]):
        return jsonify({'error': 'Missing fields'}), 400
    
    if email_exists(email):
        return jsonify({'error': 'Email already exists'}), 400
    
    create_user(firstname, lastname, username, email, password)

    return jsonify({'message': 'user created'}), 201

@app.route('/check_email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    exists = email_exists(email)
    return jsonify({'exists': exists}), 200

if __name__ == "__main__":
    app.run(debug=True)
