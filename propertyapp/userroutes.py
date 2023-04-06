import os, random, string, json
#import 3rd party
from flask import render_template, redirect,flash, session, request,url_for
from werkzeug.security import generate_password_hash, check_password_hash
#import from local files
from propertyapp import app,db
from propertyapp.models import Customers,Properties,Property_pix,Categories,State,Contact

#generate name for profile picture
def generate_name():
    filename = random.sample(string.ascii_lowercase,10)
    return ''.join(filename)#join every member of the list filename together


@app.route("/register", methods=["POST","GET"])
def user_reg():
    if request.method =="GET":
        return render_template("user/user_register.html")
    else:
        fullname = request.form.get("name")
        adds = request.form.get("message")
        email = request.form.get("email")
        number = request.form.get("phone")
        password = request.form.get("password")
        hashed_pwd = generate_password_hash(password)
        if fullname !='' and adds != '' and email !='' and password !='':
            #insert into databse using ORM method
            cust = Customers(cust_fullname= fullname, cust_email=email, cust_address = adds, cust_phone= number, cust_pwd =hashed_pwd)
            db.session.add(cust)
            db.session.commit()
            #to get the record that has just been inserted
            cust = cust.cust_id
            session['user']= cust #keep the userid in session
            return redirect(url_for('user_home'))
        else:
            flash("you must complete the fields on signup")
            return redirect(url_for('user_reg'))
            #after the above three steps av been executed
 
@app.route("/login", methods=["POST","GET"])
def user_login():
    if request.method == "GET":
        return render_template("user/user_login.html")
    else:
        #retrieve the form data
        fullname = request.form.get('name')
        password = request.form.get('password')
        #run a query to know if the username exist on the database
        deets = db.session.query(Customers).filter(Customers.cust_fullname==fullname).first()
        #compare the password coming from the form with the hashed passwprd in the db
        if deets != None:
            pass_indb = deets.cust_pwd
            #compare the plan passowrd from the fomr
            chk = check_password_hash(pass_indb,password)
            if chk:
                #loggin the person in
                id = deets.cust_id
                session['user']=id
                return redirect(url_for('user_home'))
            else:
                flash("invalid password")
                return redirect(url_for('user_login'))
        #if the password check above is right , we shouls log them in by keeping their details(user_id) in session['user'] and redirect them to the dashboard
        else:
            flash("invalid username")
            return redirect(url_for('user_login'))  
        
#checking user details using json
@app.route("/check_username", methods=["POST","GET"])
def check_username():
    if request.method == "GET":
        return "please complete the form "
    else:
        email = request.form.get('email')
        data = db.session.query(Customers).filter(Customers.cust_email==email).first()
        if data == None:
            sendback = {'status':1, 'feedback': "Email is available please register"}
            return json.dumps(sendback)
        else:
            sendback = {'status': 0, 'feedback': "email address already registered. "}
            return json.dumps(sendback)         
            
@app.route("/logout")
def user_logout():
    #pop the session and redirect to home page
    if session.get('user') != None:
        session.pop('user',None)
    return redirect(url_for('home_page'))
 
    
@app.route("/")
def home_page():
    data = Properties.query.all()
    data2 = Categories.query.all()
    states = db.session.query(State).all()
    
    propz = []
    for y in data:
        image = db.session.query(Property_pix.pic_name,Property_pix.propid).filter(Property_pix.propid==y.property_id).first()
        propz.append(image)
    return render_template("user/index.html",data=data,propz=propz,data2=data2,states=states)

@app.route("/home")
def user_home():
    imgs = db.session.query(Customers).get(session.get('user'))
    data = Properties.query.all()
    data2 = Categories.query.all()
    propz = []
    for y in data:
        image = db.session.query(Property_pix.pic_name,Property_pix.propid).filter(Property_pix.propid==y.property_id).first()
        propz.append(image)
    return render_template("user/user_home.html",imgs=imgs,data=data,propz=propz,data2=data2)

@app.route("/property")
def property():
    data = Properties.query.all()
    data2 = Categories.query.all()
    propz = []
    for y in data:
        image = db.session.query(Property_pix.pic_name,Property_pix.propid).filter(Property_pix.propid==y.property_id).first()
        propz.append(image)
    return render_template("user/property.html",data=data,propz=propz,data2=data2)

@app.route("/user_property")
def user_property():
    imgs = db.session.query(Customers).get(session.get('user'))
    data = Properties.query.all()
    data2 = Categories.query.all()
    propz = []
    for y in data:
        image = db.session.query(Property_pix.pic_name,Property_pix.propid).filter(Property_pix.propid==y.property_id).first()
        propz.append(image)
    return render_template("user/user_propperty.html",imgs=imgs,data=data,propz=propz,data2=data2)

@app.route("/details/<id>")
def prop_details(id):
    imag = db.session.query(Property_pix.pic_name,Property_pix.propid).filter(Property_pix.propid==id).all()
    property_deets = Properties.query.get(id)
    data = Categories.query.get(id)
    return render_template('user/property_details.html',imag=imag,property_deets=property_deets,data=data)

# @app.route("/user/category/<id>")
# def category(id):
#     product = Property_pix.query.filter(Property_pix.)

@app.route("/profile")
def user_propfile():
    imgs = db.session.query(Customers).get(session.get('user'))
    deets = db.session.query(Customers).filter(Customers.cust_id==session.get('user')).first()
    return render_template("user/profile_layout.html",imgs=imgs,deets=deets)

@app.route("/dashboard")
def dashboard():
    if session.get('user') != None:
    #retrieve the details of the logged in user
        id = session['user']
        deets= db.session.query(Customers).get(id)
        imgs = db.session.query(Customers).get(session.get('user'))
        return render_template("user/dashboard.html",imgs=imgs,deets=deets)
    else:
        return redirect(url_for("user_login"))

@app.route("/update_password")
def password_change():
    return render_template("user/password.html")

#profile picture===============
@app.route("/profile/picture", methods=["POST","GET"])
def profile_picture():
    if session.get('user') == None:
        return redirect(url_for('user_login'))
    else:
        if request.method == 'GET':
            imgs = db.session.query(Customers).get(session.get('user'))
            return render_template("user/account.html",imgs=imgs)
        else:
            #retrieve file
            file = request.files['pix']
            #to know the filenname
            filename = file.filename #original filename
            # filetype = file.mimetype
            allowed =['.png','.jpg','.jpeg']
            if filename !='':
                name,ext = os.path.splitext(filename)
                if ext.lower() in allowed:
                    newname = generate_name()+ext
                    file.save("propertyapp/static/uploads/"+newname)#it will uplaod the picture and save it as png
                    
                    #update user table using ORM --- we want to know the person that is logged in so we can update it
                    user = db.session.query(Customers).get(session['user'])
                    user.cust_pix = newname
                    db.session.commit()
                    flash("file uploaded") 
                    return redirect("/user/dashboard")
                    
                else:
                    return "file extension not allowed"
            else:
                flash("please choose a file")
                return redirect("/user/profile/picture")

@app.route("/contact-us", methods=["POST","GET"])
def contact():
    if session.get('user') == None:
        return redirect(url_for('user_login'))
    else:
        if request.method == "GET":
            return render_template("user/contact.html")
        else:
            name = request.form.get('fname')
            phone = request.form.get('phonenumber')
            email = request.form.get('email')
            msg = request.form.get('message')
            id = session['user']
            if name != '' and phone != '' and email != '' and msg != '':
                query3 = Contact(contact_fname=name, contact_phone=phone, contact_email=email, contact_messgae=msg,custid=id)
                db.session.add(query3)
                db.session.commit()
                flash('message delivered successfully')
                return redirect(url_for('contact'))
            else:
                flash('message not delivered')
                return redirect(url_for('contact'))    
        
@app.route("/about")
def about():
    return render_template("user/aboutus.html")


@app.route("/layout")
def layout():
    imgs = db.session.query(Customers).get(session.get('user'))
    return render_template("user/home_layout.html",imgs=imgs)
