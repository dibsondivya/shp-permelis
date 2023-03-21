from html.entities import html5
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response, flash
from flaskext.mysql import MySQL
import pdfkit
import bcrypt
import secretact
from werkzeug.utils import secure_filename
import datetime

cwd = os.getcwd()

app = Flask(__name__)

app.secret_key = os.urandom(12).hex() # to access sessions
app.config.update(dict(
   PREFERRED_URL_SCHEME = 'https'
))
UPLOAD_FOLDER = 'static/images/'

mysql = MySQL()
 
# configuring MySQL for the web application
app.config['MYSQL_DATABASE_USER'] = secretact.dbuser    # default user of MySQL to be replaced with appropriate username
app.config['MYSQL_DATABASE_PASSWORD'] = secretact.dbpass # default passwrod of MySQL to be replaced with appropriate password
app.config['MYSQL_DATABASE_DB'] = secretact.dbname  # Database name to be replaced with appropriate database name
app.config['MYSQL_DATABASE_HOST'] = secretact.dbhost # default database host of MySQL to be replaced with appropriate database host
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql.init_app(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
      

@app.route('/')
def auth():
    if 'authenticated' in session:
        session.pop('authenticated', None)
    return render_template('auth.html')

@app.route('/authcheck', methods=['POST', 'GET'])
def authcheck():
    if request.method == 'POST':
        auth = request.form.get('auth')

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "SELECT * FROM AuthenticationInfo"
        cursor.execute(sql)
        authenticated = cursor.fetchone()
        authenticatedpass = authenticated[0]

        cursor.close()
        conn.close()

        # if the user doesn't exist, reload the page
        if bcrypt.checkpw(auth.encode('utf-8'), authenticatedpass.encode('utf-8')):
            session['authenticated'] = 'valid'
            return redirect(url_for('index'))
        else:  
            return redirect(url_for('auth')) 

    else:
        return redirect(url_for('auth')) 
 
@app.route('/index')
def index():
    if 'authenticated' in session:
        if 'drugcart' in session:
            session.pop('drugcart', None)
            session.pop('drugcartlist', None)
        return render_template('index.html')
    else:
        return redirect(url_for('auth'))

@app.route('/fetchrecords', methods=['POST','GET'])
def fetchrecords():
    if 'authenticated' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        if request.method == 'POST':
            search_word = request.form['search_word']
            if search_word == '':
                sql = "SELECT * FROM DrugInfo"
                cursor.execute(sql)
                druglist = cursor.fetchall()
            else:
                # to prevent injections
                sql = "SELECT * FROM DrugInfo WHERE Entry LIKE '%{}%' OR Brand LIKE '%{}%' OR Generic LIKE '%{}%' OR Keywords LIKE '%{}%' OR Purpose LIKE '%{}%' ORDER BY Generic, CONVERT(REGEXP_SUBSTR(Entry,'[0-9]+'), UNSIGNED INTEGER) ASC;".format(search_word,search_word,search_word,search_word,search_word)
                cursor.execute(sql)
                druglist = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(druglist) == 0:
            remark = "No medications found."
        else:
            remark = "Click on the names or images of the medications below to get more details."
        return jsonify({'data': render_template('search.html', druglist=druglist, remark=remark)})
    else:
        return redirect(url_for('auth'))

@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    if 'authenticated' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        if request.method == 'POST':
            id = request.form['id']
            sql = "SELECT * FROM DrugInfo WHERE Id = %s"
            vals = (id,)
            cursor.execute(sql, vals)
            druglist = cursor.fetchall() 
        cursor.close()
        conn.close()
        return jsonify({'htmlresponse': render_template('modal.html', druglist=druglist)})
    else:
        return redirect(url_for('auth'))

@app.route("/add",methods=["POST","GET"])
def add():
    if 'authenticated' in session:
        id = request.form['id']
        if 'drugcart' in session:
            drugcart = session['drugcart']
            drugcart.append(id)
            drugcartnumber = len(drugcart)
            session['drugcart'] = drugcart
        else:
            drugcart = []
            drugcart.append(id)
            drugcartnumber = len(drugcart)
            session.permanent = False
            session['drugcart'] = drugcart

        conn = mysql.connect()
        cursor = conn.cursor()
        drugcartlist = []
        for id in drugcart:
            sql = "SELECT * FROM DrugInfo WHERE Id = %s"
            vals = (id,)
            cursor.execute(sql, vals)
            drugcartrecord = cursor.fetchall()
            drugcartlist.append(drugcartrecord[0])

        session["drugcartlist"] = drugcartlist
        cursor.close()
        conn.close()
        return jsonify({'htmlresponse': render_template('cart.html', drugcartlist=drugcartlist)})
    else:
        return redirect(url_for('auth'))

@app.route("/empty", methods=["POST", "GET"])
def empty():
    if 'authenticated' in session:
        if "drugcartlist" in session:
            drugcart = session['drugcart']
            drugcartlist = session['drugcartlist']
            id = int(request.form['id'])
            for i in list(enumerate(drugcartlist)):
                if i[0] == id:
                    delete = list(enumerate(drugcartlist)).index(i)
                    drugcartlist.pop(delete)
                    drugcart.pop(delete)
                
            if len(drugcart) > 0:
                session['drugcart'] = drugcart
                session['drugcartlist'] = drugcartlist
                return jsonify('Delete success!')
            else:
                session.pop('drugcart', None)
                session.pop('drugcartlist', None)
                return jsonify('Delete success!')
        else:
            return jsonify('Cart is already empty!')
    else:
        return jsonify('Please refresh the page.')

@app.route("/emptyall", methods=["POST", "GET"])
def emptyall():
    if "authenticated" in session:
        if "drugcart" in session:
            session.pop('drugcart', None)
            session.pop('drugcartlist', None)
            return jsonify('Delete success!')
        else:
            return jsonify('Cart is already empty!')
    else:
        return jsonify('Please refresh the page.')

@app.route('/printing')
def printing():
    if 'authenticated' in session:
        if "drugcart" in session:
            drugcartlist = session['drugcartlist']
            if len(drugcartlist) > 0:
                printout = render_template("print.html", drugcartlist=drugcartlist, cwd=cwd)
                options = {'enable-local-file-access': None,
                '--footer-html': "file:///{}/templates/footer.html".format(cwd),
                '--header-html': "file:///{}/templates/header.html".format(cwd),
                '--no-stop-slow-scripts': None}
                '''
                for use in windows: 
                config = pdfkit.configuration(wkhtmltopdf=r'////PATH/////')
                pdf = pdfkit.from_string(printout, False, options=options, configuration=config)
                '''
                pdf = pdfkit.from_string(printout, False, options=options)
                response = make_response(pdf)
                response.headers['Content-Type'] = 'application/pdf' # alternatives include /json for js and /css for css based input
                response.headers['Content-Disposition'] = 'attachment; filename=PERMELIS - {}.pdf'.format(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")) #alternative is 'inline;
                return response
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('auth'))

@app.route("/admin")
def admin():
    if 'authenticated' in session:
        if "username" in session:
            session.pop('username', False)
        return render_template('login.html')
    else:
        return redirect(url_for('auth'))

@app.route('/loginsubmit', methods=["POST","GET"])
def adminlogin():
    if 'authenticated' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        if request.method == 'POST':
            loginusername = request.form.get('username')
            loginpassword = request.form.get('password')

            sql = "SELECT * FROM AdminInfo WHERE Username=%s"
            vals = (loginusername,)
            cursor.execute(sql, vals)
            user = cursor.fetchone()
            trueloginpassword = user[1]
            cursor.close()
            conn.close()

            # if user exists
            if user and bcrypt.checkpw(loginpassword.encode('utf-8'), trueloginpassword.encode('utf-8')):
                session['username'] = user[0]
                return redirect(url_for('adminview'))
            else:
                return redirect(url_for('admin'))        
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('auth'))
       
@app.route('/adminview')
def adminview():
    if 'authenticated' in session:
        #create connection to access data
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM DrugInfo ORDER BY Entry ASC"
        cursor.execute(sql)
        admindruginfo = cursor.fetchall()

        username = session['username']
        cursor.close()
        conn.close()

        return render_template('admin.html', username=username, admindruginfo=admindruginfo)
    else:
        return redirect(url_for('auth'))

@app.route('/adminadd', methods=['POST', 'GET'])
def adminadd():
    if 'authenticated' in session:
        if request.method == 'POST':
            file = request.files['InputImg'] #unique
            entry = request.form.get('InputEntry') #unique
            purpose = request.form.get('InputPurpose')
            brand = request.form.get('InputBrand')
            generic = request.form.get('InputGeneric')
            cost = request.form.get('InputCost')  
            details = request.form.get('InputDetails')
            keywords = request.form.get('InputKeywords')
            if file and allowed_file(file.filename):
                conn = mysql.connect()
                cursor = conn.cursor()

                filename = secure_filename(file.filename)
                sql = "SELECT * FROM DrugInfo WHERE Entry=%s OR Img=%s"
                vals = (entry, filename,)
                cursor.execute(sql, vals)
                existing = cursor.fetchall()

                if existing!=():
                    flash('Please enter a new Entry name or rename your Image.')
                else:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    sql = "INSERT INTO DrugInfo (Entry, Img, Purpose, Brand, Generic, Cost, Details, Keywords) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    vals = (entry, filename, purpose, brand, generic, cost, details, keywords,)
                    cursor.execute(sql, vals)
                    conn.commit()
                    flash('New medication added successfully.')
                cursor.close()
                conn.close()
                return redirect(url_for('adminview'))
            else:
                flash('Medication addition failed. Please try again.')
                return redirect(url_for('adminview'))
        else:
            return redirect(url_for('adminview'))
    else:
        return redirect(url_for('auth'))

@app.route('/adminedit/<int:id>', methods = ['POST','GET'])
def adminedit(id):
    if 'authenticated' in session:
        if 'username' in session:
            username = session['username']
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = 'SELECT * FROM DrugInfo WHERE Id = %s'
            vals = (id,)
            cursor.execute(sql,vals)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('edit.html', username=username, drug = data[0])
        else:
            return redirect(url_for('adminview'))
    else:
        return redirect(url_for('auth'))

@app.route('/adminupdate/<int:id>', methods = ['POST','GET'])
def admineupdate(id):
    if 'authenticated' in session:
        if request.method == 'POST':
            file = request.files['img'] #unique
            entry = request.form.get('entry') #unique
            purpose = request.form.get('purpose')
            brand = request.form.get('brand')
            generic = request.form.get('generic')
            cost = request.form.get('cost')  
            details = request.form.get('details')
            keywords = request.form.get('keywords')

            # store id number of given entry
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "SELECT Id FROM DrugInfo WHERE Entry=%s"
            vals = (entry,)
            cursor.execute(sql, vals)
            checkid = cursor.fetchone()

            # if image is updated
            if file and allowed_file(file.filename):
                conn = mysql.connect()
                cursor = conn.cursor()
                filename = secure_filename(file.filename)
                sql = "SELECT * FROM DrugInfo WHERE Img=%s"
                vals = (filename,)
                cursor.execute(sql, vals)
                existing = cursor.fetchone()

                # image exists with this name
                if existing!=None:
                    cursor.close()
                    conn.close()
                    flash('Current image already exists. Please try again.')
                    return redirect(url_for('adminedit', id=id))

                # if this is the only image with this name  
                else:
                    # if entry does not exist aka is unique or no change to entry name
                    if checkid==None or checkid[0]==id:
                        sql = "SELECT Img FROM DrugInfo WHERE Id=%s"
                        vals = (id,)
                        cursor.execute(sql, vals)
                        oldentry = cursor.fetchone()
                        oldfilename = oldentry[0]
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], oldfilename))

                        sql = "UPDATE DrugInfo SET Entry=%s, Img=%s, Purpose=%s, Brand=%s, Generic=%s, Cost=%s, Details=%s, Keywords=%s where Id=%s"
                        vals = (entry, filename, purpose, brand, generic, cost, details, keywords, id,)
                        cursor.execute(sql, vals)
                        conn.commit()    
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        flash('Medication updated successfully.')
                        cursor.close()
                        conn.close()
                        return redirect(url_for('adminview'))
                    else:
                        cursor.close()
                        conn.close()
                        flash('Current entry name already exists. Please try again.')
                        return redirect(url_for('adminedit', id=id))

            # image is not updated
            elif file.filename == '':
                conn = mysql.connect()
                cursor = conn.cursor()
                # if entry does not exist aka is unique or no change to entry name
                if checkid==None or checkid[0]==id:       
                    sql="UPDATE DrugInfo SET Entry=%s, Purpose=%s, Brand=%s, Generic=%s, Cost=%s, Details=%s, Keywords=%s where Id=%s"
                    vals = (entry, purpose, brand, generic, cost, details, keywords, id,)
                    cursor.execute(sql, vals)
                    conn.commit()
                    flash('Medication updated successfully.')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('adminview'))
                else:
                    cursor.close()
                    conn.close()
                    flash('Current entry name already exists. Please try again.')
                    return redirect(url_for('adminedit', id=id))
                
            else:
                flash('Please try again.')
                return redirect(url_for('adminview'))      
        else:
            return redirect(url_for('adminview'))
    else:
        return redirect(url_for('auth'))

@app.route('/admindelete/<int:id>', methods = ['POST','GET'])
def admindelete(id):
    if 'authenticated' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM DrugInfo WHERE Id=%s"
        vals = (id,)
        cursor.execute(sql, vals)
        data = cursor.fetchone()
        filename = data[2]
     
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        sql = "DELETE FROM DrugInfo WHERE Id=%s"
        vals = (id,)
        cursor.execute(sql, vals)
        conn.commit()
        cursor.close()
        conn.close()

        flash('Entry deleted successfully.')
        return redirect(url_for('adminview'))
    else:
        return redirect(url_for('auth'))

@app.route('/adminregister', methods=['POST', 'GET'])
def adminregister():
    if 'authenticated' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        if request.method == 'POST':
            newusername = request.form.get('username')
            newpassword = request.form.get('password').encode('utf-8')
            sql = "SELECT * FROM AdminInfo WHERE Username=%s"
            vals = (newusername,)
            cursor.execute(sql, vals)
            adminuser = cursor.fetchone()

            if adminuser!=None:
                flash('This admin user already exists. Please try again.')
            else:
                hashed = bcrypt.hashpw(newpassword, bcrypt.gensalt())
                sql = "INSERT INTO AdminInfo (Username, Password) VALUES (%s, %s)"
                vals = (newusername, hashed,)
                cursor.execute(sql,vals)
                conn.commit()
                flash('New admin user successfully added.')
        cursor.close()
        conn.close()
        return redirect(url_for('adminview'))
    else:
        return redirect(url_for('auth'))

@app.route('/adminremove', methods=['POST', 'GET'])
def adminremove():
    if 'authenticated' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        if request.method == 'POST':
            myusername = request.form.get('myusername')
            mypassword = request.form.get('mypassword').encode('utf-8')
            sql = "SELECT * FROM AdminInfo WHERE Username=%s"
            vals = (myusername,)
            cursor.execute(sql, vals)
            myadmin = cursor.fetchone()

            if myadmin and bcrypt.checkpw(mypassword, myadmin[1].encode('utf-8')):
                removeuser = request.form.get('removeuser')
                sql = "SELECT * FROM AdminInfo WHERE Username=%s"
                vals = (removeuser,)
                cursor.execute(sql, vals)
                userpresent = cursor.fetchone()
                if userpresent and removeuser!=myusername:
                    sql = "DELETE FROM AdminInfo WHERE Username=%s"
                    vals = (removeuser,)
                    cursor.execute(sql, vals)
                    conn.commit()
                    flash('User successfully removed.')
                elif removeuser==myusername:
                    flash('Admin Error: Cannot remove ownself.')
                else:
                    flash('User to be removed does not exist.')
            else:
                flash('User credentials are invalid. Please try again.')
        cursor.close()
        conn.close()
        return (redirect(url_for('adminview')))
    else:
        return redirect(url_for('auth'))


@app.route('/adminauth', methods=['POST', 'GET'])
def adminauth():
    if 'authenticated' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        if request.method == 'POST':
            oldauth = request.form.get('oldauth')

            sql = "SELECT * FROM AuthenticationInfo"
            cursor.execute(sql)
            dbauth = cursor.fetchone()
            trueauth = dbauth[0]

            if bcrypt.checkpw(oldauth.encode('utf-8'), trueauth.encode('utf-8')): # if the old passwords match
                newauth = request.form.get('newauth').encode('utf-8')
                if bcrypt.checkpw(newauth, trueauth.encode('utf-8')): # if old and new passwords match
                    cursor.close()
                    conn.close()
                    flash('Edit of Authentication details failed. Both passwords match. Please try again.')
                    return (redirect(url_for('adminview')))
                else: # if old and new passwords are different
                    hashedauth = bcrypt.hashpw(newauth, bcrypt.gensalt())
                    sql = "UPDATE AuthenticationInfo SET Password=%s"
                    vals = (hashedauth,)
                    cursor.execute(sql, vals)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    flash('Authentication details successfully updated.')
                    return redirect(url_for('adminview'))
            else:
                cursor.close()
                conn.close()
                flash('Edit of Authentication details failed. Please try again.')
                return redirect(url_for('adminview'))                
        else:
            cursor.close()
            conn.close()
            return redirect(url_for('adminview'))
    else:
        return redirect(url_for('auth'))

@app.route('/adminlogout')
def adminlogout():
    if 'authenticated' in session:
        session.pop('username', None)
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('auth'))

if __name__ == "__main__":  
    app.run()