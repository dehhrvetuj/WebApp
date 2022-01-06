import os
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, send_from_directory
from flask import session, flash
from werkzeug.utils  import secure_filename
from engine.grading_func import grading_engine


UPLOAD_FOLDER = './files/upload'
DOWNLOAD_FOLDER='./files/download'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024


@app.route('/grading', methods=['POST','GET'])
def grading():
    if request.method == "POST":

        obj = [request.form['obj1'], request.form['obj2'], request.form['obj3'], request.form['obj4'], request.form['obj5']]
        proc = [request.form['proc1'], request.form['proc2'], request.form['proc3'], request.form['proc4'], request.form['proc5']]  
        
        if 'file' not in request.files:
            flash("You did NOT upload your Excel file")
            return "You did NOT upload your Excel file"
        else:
            file = request.files['file']
        
        if file.filename == '':
            flash("Empty File Name")
            return("Empty File Name")

        ifname = secure_filename(file.filename)

        file.save(os.path.join(app.config["UPLOAD_FOLDER"],ifname))
        
        ofname = ifname + '.txt'
        infile = os.path.join(app.config["UPLOAD_FOLDER"],ifname)
        outfile = os.path.join(app.config["UPLOAD_FOLDER"],ofname)
        
        ret = grading_engine(infile, outfile, obj, proc)
        
        if ret is None:
	        return redirect(url_for("upload_file", filename=ofname))
        else:
	        return ret
    else:
        return render_template("grading.html")

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'],filename)

@app.route('/upload/<filename>')
def upload_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#@app.route('/')
#def start():
#    greeting = ''
#    input('>>>>')
#    return f"Hello, {greeting}"
#
#@app.route('/index')
#def index():
#    greeting = ''
#    #input('>>>>')
#    #return f"Hello, {greeting}"
#    return render_template("index.html", greeting=greeting)
#
#@app.route('/congwang')
#def congwang():
#    greeting = ''
#    #return "This is Cong Wang's page"
#    return render_template("flask.pocoo.org.html",greeting=greeting)
#
#@app.route('/hello')
#def hello():
#    name = request.args.get('name','Nobody')
#    greet = request.args.get('greet','Hello')
#
#    greeting = f"{greet}, {name}"
#
#    return render_template('index.html',greeting=greeting)

#@app.route('/login', methods=['POST','GET'])
#def login():
#    error = None
#    if request.method == "POST":
#        if request.form['username'] != "admin" or request.form['password'] != 'admin':
#            error = "Invalid Credentials. Please try again."
#            flash("wrong password!")
#            return render_template("login.html",error=error)
#        else:
#            session['logged_in'] = True
#            return redirect(url_for("home", username=request.form['username']))
#    else:
#        return render_template("login.html",error=error)
#
#
#@app.route('/logout')
#def logout():
#    session['logged_in'] = False
#    return home('')
#
#
#@app.route('/home/<username>')
#def home(username):
#    if not session.get('logged_in'):
#        return render_template("login.html")
#    else:
#        return f'Hello {username} <a href="/logout">Logout</a>'



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
    #app.run(debug=True, host='0.0.0.0', port=5000)
