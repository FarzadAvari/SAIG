from flask import render_template,url_for,flash,redirect,request,Response
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.camera import Camera

posts = [
	{
		'author':'John Lennon',
		'title':'The beatles',
		'content':'Awesome concert at the bay',
		'date':'23/4/2290'
	},
	{
		'author':'Da Vinci',
		'title':'Mona Lisa',
		'content':'Medieval level painting for the masses',
		'date':'12/5/1680'
	}
]

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/register", methods = ['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created!','success')
		return redirect(url_for('login'))
	return render_template("register.html", title = 'Register', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('account'))
		else:
			flash('Login unsuccessful, please check login and password', 'danger')

	return render_template("login.html", title = 'Login', form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file = image_file)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/camera1")
def camera1():
	return render_template('camera1.html', title='Camera1')
	#feed = return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
	#return render_template('camera1.html', title='Camera1', feed = feed)
#	return Response(stream_template('camera1.html', feed=Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')))
	

@app.route("/video_feed")
def video_feed():
	return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(Camera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')



