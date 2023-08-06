from .database import db
from flask_login import UserMixin

class Category(db.Model):
    __tablename__ = 'category'
    categoryId = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement= True)
    categoryName = db.Column(db.String, nullable = False)

class Product(db.Model):
    __tablename__ = 'product'
    productId = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement= True)
    productName = db.Column(db.String, nullable = False)
    expiryDate = db.Column(db.String)
    manufacturingDate = db.Column(db.String)
    ratePerUnit = db.Column(db.Float)
    categoryId = db.Column(db.Integer, db.ForeignKey('category.categoryId'),nullable= False)
    inStock = db.Column(db.Integer)
    category = db.relationship('Category', backref=db.backref('product', lazy=True))

class Managers(db.Model, UserMixin):
    __tablename__ = 'managers'
    managerId = db.Column(db.Integer, nullable= False, primary_key=True,autoincrement= True,)
    managerUserName = db.Column(db.String, nullable=False, unique=True)
    managerPassword= db.Column(db.String, nullable=True,unique=True )
    def get_id(self):
       return (self.managerId)
    
class Customers(db.Model, UserMixin):
    __tablename__= 'customers'
    customerId= db.Column(db.Integer, nullable= False, primary_key=True,autoincrement= True)
    customerFirstName = db.Column(db.String, nullable = False)
    customerLastName = db.Column(db.String, nullable = False)
    customerMailId = db.Column(db.String, nullable=False, primary_key = False, unique= True)
    customerUserName = db.Column(db.String, nullable= False, unique = True)
    customerUserPassword = db.Column(db.String, nullable = False, unique = True)
    customerAddress = db.Column(db.String, nullable = False)
    def get_id(self):
        return (self.customerId)


class CustomerCart(db.Model):
    __tablename__= 'customerCart'
    cartItemId = db.Column(db.Integer, nullable= False, primary_key=True,autoincrement= True)
    itemAdded = db.Column(db.String)
    itemAddedQuantity= db.Column(db.Integer)
    customerId= db.Column(db.Integer, db.ForeignKey('customers.customerId'))
    customer = db.relationship('Customers',backref=db.backref('customerCart', lazy=True))
    productId = db.Column(db.Integer,db.ForeignKey('product.productId'))
    product = db.relationship('Product', backref= db.backref('customerCart',lazy = True) )
