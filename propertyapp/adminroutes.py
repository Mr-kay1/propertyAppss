import os,random,string
#import 3rd party
from flask import render_template, redirect,flash, session, request,url_for
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
#import from local files
from propertyapp import app,db
from propertyapp.models import Properties,Property_pix,State,Categories,Contact


def generate_name():
    filename = random.sample(string.ascii_lowercase,10)
    return ''.join(filename)#join every member of the list filename together


#admin login route
@app.route("/admin/login", methods=["POST","GET"])
def login():
    if request.method =="GET":
        return render_template("admin/admin_login.html")
    else:
        email = request.form.get("email")
        pwd = request.form.get("password")
        #write the select query
        query = f"SELECT * FROM admin WHERE admin_email ='{email}' AND admin_password = '{pwd}'"
        result = db.session.execute(text(query))
        total = result.fetchone()
        if total:
            session["loggedin"]=email
            return redirect("/admin/property-table")
        else:
            flash("Invalid Credentials")
            return redirect("/admin/login")


#admin dashboard     
@app.route("/admin_dasboard")
def admin_dashboard():
    if session.get("loggedin") == None:
        return redirect("/admin/login")
    else:
        data = Properties.query.all()
        qry= Categories.query.all()
        return render_template("admin/admin_dashboard.html", data=data,qry=qry)
    
#adding property =======================  
@app.route("/admin/addproperty", methods=["POST","GET"])
def add_prop():
    if session.get("loggedin") == None:
        return redirect("/admin/login")
    else:
        if request.method =="GET":
            states = db.session.query(State).all()
            cat_egory = db.session.query(Categories).all()
            return render_template("admin/add_property.html", states=states,cat_egory=cat_egory)
        else:
            #retrive from form
            data = request.form
            adds = data.get('address')
            propstate = data.get('state')
            propdesc = data.get('desc')
            price = data.get('property_price')
            cat = data.get('category')
            agent = data.get('number')
            img = request.files.getlist('picture')
            
            if adds != '' and propstate != '' and propdesc != '' and price != '' and cat != '' and agent != '':
                query = Properties(property_address=adds, stateid=propstate, property_desc=propdesc, property_price=price,category=cat,agent_phone=agent)            
                db.session.add(query)
                db.session.commit()
                allowed = [".jpg",".jpeg",".png"]
                for i in img:
                    picture = i.filename
                    if picture !="":
                        name,ext = os.path.splitext(picture)
                        if ext in allowed:
                            newname = generate_name()+ext
                            i.save('propertyapp/static/uploads/'+newname)
                            deets = Property_pix(pic_name=newname,propid=query.property_id)
                            db.session.add(deets)
                            db.session.commit()
                        else:
                            flash("image extension not allowed")
                            return redirect(url_for('add_prop'))
                    else:
                        flash("images must be uploaded")
                        return redirect(url_for('add_prop'))
                flash("property added succesfully")
                return redirect(url_for('property_table'))
            else:
                flash("all fields are required")
                return redirect("add_prop")
            
#deleting of post               
@app.route("/admin/delete/<id>")
def delete(id):
    props = Properties.query.get_or_404(id)
    db.session.delete(props)
    db.session.commit()
    flash("successfully deleted")
    return redirect(url_for('property_table'))

#edting ... approving or pending post
@app.route("/admin/property/edit/<id>")
def edit_property(id):
    #ensure that the route is protected
    if session.get('loggedin') != None:
        #query to fetch a topic of interest i.e the one with id
        property_deets = Properties.query.get(id)
        return render_template("admin/prop_edit.html",property_deets=property_deets)
    else:
        return redirect(url_for('login'))
    
#updating     
@app.route("/admin/update_property", methods=["POST"])
def update_topic():
    #how to update
    if session.get('loggedin') != None:
        newstatus=request.form.get('status')
        propid = request.form.get('propid')
        x=Properties.query.get(propid)
        x.property_status = newstatus
        db.session.commit()
        flash("property succesfully updated")
        return redirect("/admin/property-table")
    else:
        return redirect("/admin/login")
    
#fetching all from data base
@app.route("/admin/property-table")
def property_table():
    if session.get("loggedin") == None:
        return redirect("/admin/login")
    else:
        data = Properties.query.all()
        return render_template("admin/property_table.html", data=data)
    
@app.route("/admin/picture-table")
def picture_table():
    if session.get("loggedin") == None:
        return redirect("/admin/login")
    else:
        data = Property_pix.query.all()
        return render_template("admin/pictures.html", data=data)
    
@app.route("/admin/delete_pictures/<id>")
def delete_pictures(id):
    props = Property_pix.query.get_or_404(id)
    db.session.delete(props)
    db.session.commit()
    flash("successfully deleted")
    return redirect(url_for('picture_table'))


#adding categories
@app.route("/admin/addcategory", methods=["POST","GET"])
def add_category():
    if session.get("loggedin") == None:
        return redirect("/admin/login")
    else:
        if request.method =="GET":
            return render_template("admin/add_categories.html")
        else:
            #retriving from form
            caat = request.form.get('addcat')
            if caat != '':
                query1 = Categories(category_name=caat)
                db.session.add(query1)
                db.session.commit()
                flash("new category added")
                return redirect("/admin/category_table")
            else:
                flash("No category added")
                return render_template("admin/add_categories.html")
        

@app.route("/admin/category_table")
def category_table():
    catt = Categories.query.all()
    return render_template("admin/categories_table.html",catt=catt)

@app.route("/admin/delete_category/<id>")
def delete_category(id):
    cates = Categories.query.get_or_404(id)
    db.session.delete(cates)
    db.session.commit()
    flash("successfully deleted")
    return redirect(url_for('category_table'))

@app.route("/admin/feedback.html")
def feedback():
    data = Contact.query.all()
    return render_template("admin/feedback.html", data=data)

@app.route("/admin/delete_feedback/<id>")
def delete_feedback(id):
    feedb = Contact.query.get_or_404(id)
    db.session.delete(feedb)
    db.session.commit()
    flash("successfully deleted")
    return redirect(url_for('feedback'))

@app.route("/admin/agent")
def agent():
    data = Properties.query.all()
    return render_template("admin/agent.html", data=data)

@app.route("/admin/delete_agent")
def delete_agent(id):
    fagent = Contact.query.get_or_404(id)
    db.session.delete(agent)
    db.session.commit()
    flash("successfully deleted")
    return redirect(url_for('agent'))

    
#admin logout
@app.route("/admin/logout")
def admin_logout():
    if session.get("loggedin") != None:
        session.pop("loggedin",None)
    return redirect("/admin/login")