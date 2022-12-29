import requests, os, smtplib
from post import Post
from flask import Flask
from flask import request
from flask import render_template


#initilize global variables
EMAIL = os.getenv('SMTP_USER')
PW = os.getenv('SMTP_PASS')
APP = Flask(__name__, template_folder='templates', static_folder='static')
BLOG_POSTS = requests.get('https://api.npoint.io/08a3f685b4c52bd10b24').json()
POST_LIST = []


#populate POST_LIST with relevant key/value pairs from BLOGS_URL endpoint
for post in BLOG_POSTS:
    temp = Post(post['id'], post['title'], post['subtitle'], post['body'], post['author'], post['date'], post['image'])
    POST_LIST.append(temp)


@APP.route('/')
def main():
    return render_template('index.html', posts=POST_LIST)


@APP.route('/about')
def about():
    return render_template('about.html')


@APP.route('/contact', methods=['POST', 'GET'])
def contact():
    #if `POST` method do this
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        #prepare for email with `content` variable
        content = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}'
        #send email with relevant form data
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PW)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=f'Subject: From Flask and Bootstrap\n\n{content}')
        return render_template('form-entry.html', name=name, email=email, phone=phone, message=message)

    #if `GET` method do this
    return render_template('contact.html')


@APP.route('/post/<int:num>')
def post(num=None):
    requested = None
    for post in POST_LIST:
        if post.id == num:
            requested = post
    return render_template('post.html', post=requested)


if __name__ == '__main__':
    APP.run(debug=True)


#to start run
#export FLASK_APP=name_of_flask_file
#flask run