from datetime import datetime
from propertyapp import db


class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_email = db.Column(db.String(120))
    admin_phonenumber = db.Column(db.String(120),nullable=True)
    
    
class Customers(db.Model):
    cust_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    cust_fullname = db.Column(db.String(100),nullable=False)
    cust_address = db.Column(db.String(150),nullable=False)
    cust_email = db.Column(db.String(120))
    cust_pix=db.Column(db.String(120),nullable=True)
    cust_phone = db.Column(db.String(120),nullable=True)  
    cust_pwd = db.Column(db.String(120),nullable=True)
    #set relationship
    #contCust = db.relationship("Customers", back_populates="custCont")
   # property_deets = db.relationship("Properties", back_populates="customersdeet")
   
class Contact(db.Model):
    contact_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    custid = db.Column(db.Integer, db.ForeignKey("customers.cust_id"))
    contact_fname = db.Column(db.String(100),nullable=False)
    contact_phone = db.Column(db.String(120),nullable=True)  
    contact_email = db.Column(db.String(120))
    contact_messgae = db.Column(db.String(250),nullable=False)
    #relationship
    #custCont = db.relationship("Customers", back_populates="contCust")
     

class Properties(db.Model):
    property_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    property_address = db.Column(db.String(150),nullable=False)
    property_price = db.Column(db.String(100),nullable=False)
    property_desc = db.Column(db.String(100),nullable=False)
    agent_phone = db.Column(db.String(120),nullable=True)  
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    property_status = db.Column(db.Enum('Buy','Sold'),nullable=False, server_default=('Buy'))
     #foriegn key
    stateid = db.Column(db.Integer, db.ForeignKey("state.state_id"))
    category = db.Column(db.Integer, db.ForeignKey("categories.category_id")) 
     #set relationship
   # customersdeet = db.relationship("Customers", back_populates="property_deets")
    prop_type = db.relationship("Categories", back_populates="props") 
    prop_prop = db.relationship("Property_pix", back_populates="prop_pix") 
    prop_state = db.relationship("State", back_populates="stateid") 
    
    
    
class Categories(db.Model):
    category_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    category_name = db.Column(db.String(120),nullable=True)
    #set relationship
    props = db.relationship("Properties", back_populates="prop_type")
   
     
    
class Property_pix(db.Model):
    pic_id =  db.Column(db.Integer, autoincrement=True,primary_key=True)
    pic_name = db.Column(db.String(120),nullable=True)
    propid = db.Column(db.Integer, db.ForeignKey("properties.property_id"))
     #set relationship
    prop_pix = db.relationship("Properties", back_populates="prop_prop")

class State(db.Model):
    state_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    state_name = db.Column(db.String(100),nullable=True)
    #set relationship
    stateid = db.relationship("Properties", back_populates="prop_state")
    
    

