from flask import request
from flask import render_template
from flask import current_app as app
from application.models import Category,Product, Customers, Managers
from .database import db
from flask import redirect 
from flask import url_for
from main import bcrypt
#from .controllers import login_manager
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
#from flask_bcrypt import Bcrypt

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view='customerLogin'

login_manager = LoginManager()
# allows our app to handle things like loggin in
login_manager.init_app(app)
#login_manager.login_view='customerLogin'

#now_user = None

@login_manager.user_loader
def load_Customer(customerId):
    return Customers.query.get(int(customerId))

@login_manager.user_loader
def load_Manager(managerId):
    return Managers.query.get(int(managerId))



@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form['user-type'] == "manager":
            #login_manager.login_view='managerLogin'
            return redirect(url_for('managerLogin'))
        if request.form['user-type'] == "customer":
            #login_manager.login_view='customerLogin'
            return redirect(url_for('customerLogin'))
    if request.method == "GET":
        return render_template('startPage.html')

@app.route('/customerLogin',methods=['GET','POST'])
def customerLogin():
    if request.method == 'GET':
        return render_template('customerLogin.html')
    if request.method == 'POST':
        UserName = request.form['UserName']
        UserPassword = request.form['Password']
        password_hash = bcrypt.generate_password_hash(UserPassword).decode('utf8')
        print(password_hash)
        customer__original = Customers.query.filter_by(customerUserName = UserName).first()
        manager__original = Managers.query.filter_by(managerUserName = UserName).first()
        print(customer__original)
        if customer__original:
            try:
                global now_user
                now_user = current_user
                if bcrypt.check_password_hash(customer__original.customerUserPassword, UserPassword):
                    login_user(customer__original)
                    print(current_user)
                    print(now_user)
                    return redirect(url_for('customerDashboard'))
            except Exception as e:
                print(e)
                    #return render_template('test.html',current_user=current_user)
        if manager__original:
            if bcrypt.check_password_hash(manager__original.managerPassword,UserPassword):
                login_user(manager__original)
                return redirect(url_for('addCategory'))

        #if customerUserName == customer__original.customerUserName:
        #    print(customer__original.customerUserPassword)
        #    if bcrypt.check_password_hash(customer__original.customerUserPassword, customerUserPassword):
        #        print('its a fucking match')
        #        login_user(customer__original)
        #        print('testing')
        #        print(current_user)
        #        #current_user = customer__original
        #        return redirect(url_for('customerDashboard'))
        #return render_template('customerLogin.html')
        #print(managerUserName,managerUserName__original.managerUserName, managerPassword)
        #return redirect(url_for('customerLogin'))
   
@app.route('/customerSignUp',methods=['GET','POST'])
def customerSignUp():
    if request.method == 'POST':
        customerFirstName=request.form['customerFirstName']
        customerLastName= request.form['customerLastName']
        customerUserName = request.form['customerUserName']
        customerMailId = request.form["customerMailId"]
        customerUserPassword = request.form['customerUserPassword']
        hash_user_password = bcrypt.generate_password_hash(customerUserPassword).decode('utf8')
        customerAddress = request.form['customerAddress']
        customerCity = request.form['customerCity']
        customerState = request.form['customerState']
        new_customer = Customers(customerFirstName=customerFirstName,
                                 customerLastName=customerLastName,
                                 customerUserName = customerUserName,
                                 customerMailId = customerMailId,
                                 customerUserPassword = hash_user_password,
                                 customerAddress = customerAddress+", "+customerCity+", "+customerState
                                 )
        print(new_customer.customerAddress)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('customerSignUp'))
    return render_template('customerSignUp.html')


@app.route('/customerDashboard',methods=['GET','POST'])
def customerDashboard():
    print('checking')
    #print(now_user)
    #print(now_user)
    return render_template('test.html',current_user=current_user)




@app.route('/managerLogin/',methods=['GET',"POST"])
def managerLogin():
    try:
        if request.method == 'GET':
            return render_template('loginPage.html')
        if request.method == 'POST':
            managerUserName = request.form['managerUserName']
            managerPassword = request.form['managerPassword']
            password_hash = bcrypt.generate_password_hash(managerPassword).decode('utf8')
            print(password_hash)
            managerUserName__original = Managers.query.filter_by(managerUserName=managerUserName).first()
            if managerUserName == managerUserName__original.managerUserName:
                print(managerUserName__original.managerPassword)
                if bcrypt.check_password_hash(managerUserName__original.managerPassword, managerPassword):
                    print('its a fucking match')
                    login_user(managerUserName__original)
                    print(current_user)
                    return redirect(url_for('addCategory'))
            print(managerUserName,managerUserName__original.managerUserName, managerPassword)
            return render_template('loginPage.html')
    except AttributeError:
        return render_template('loginPage.html')
   

@app.route('/managerLogout', methods=['GET','POST'])
@login_required
def managerLogout():
    logout_user()
    return redirect(url_for('managerLogin'))


@app.route('/addCategory',methods=["GET","POST"])
@login_required
def addCategory():
    if request.method == "POST":
        #print('in ifelse')
        categoryName= request.form['categoryName']
        #print(categoryName)
        newCategory = Category(categoryName = categoryName)
        #print(newCategory)
        db.session.add(newCategory)
        db.session.commit()
        all_categories = Category.query.all()
        #print(all_categories[0].categoryName)
        return redirect(url_for('addCategory'))

    all_categories = Category.query.all()
    print(all_categories[0].categoryName)
    return render_template('addCategory.html',allCategories = all_categories)


@app.route('/addProduct/<categoryName>',methods=['GET','POST'])
@login_required
def addProduct(categoryName):
    if request.method == "GET" :
        category = Category.query.filter_by(categoryName=categoryName).first()
        print(category)
        category = Category.query.get(category.categoryId)
        products = category.product
        for val in products:
            print(val.productName)
        return render_template('displayProducts.html',categoryName=categoryName,products=products)
    if request.method == "POST" :
        productName = request.form['productName']
        expiryDate = request.form['expiryDate']
        manufacturingDate = request.form['manufacturingDate']
        ratePerUnit = request.form['ratePerUnit']
        inStock= request.form['inStock']
        category = Category.query.filter_by(categoryName=categoryName).first()

        newProduct = Product(productName=productName,expiryDate=expiryDate,
                             manufacturingDate=manufacturingDate,ratePerUnit=float(ratePerUnit),
                             categoryId=category.categoryId,inStock=inStock)
        print(productName)
        #newProduct = Product(productName='test',expiryDate='23/23/2333',
        #                     manufacturingDate='23/42/5211',ratePerUnit=23.00,
        #                     categoryId=2)
        db.session.add(newProduct)
        db.session.commit()
        #print(newProduct.category.categoryName)
        return redirect(url_for('addProduct',categoryName=categoryName))
        return render_template('displayProducts.html',categoryName=categoryName)
    

@app.route('/updateProduct/<categoryName>/<productName>',methods=['GET','POST'])
@login_required
def updateProduct(categoryName,productName):
    if request.method == "GET":
        category = Category.query.filter_by(categoryName=categoryName).first()
        product= Product.query.filter_by(productName=productName,categoryId=category.categoryId).first()
        print(category)
        print(product)
        return render_template('editProduct.html',categoryName=categoryName,productName=productName)
    if request.method == "POST":
        category = Category.query.filter_by(categoryName=categoryName).first()
        product= Product.query.filter_by(productName=productName,categoryId=category.categoryId).first()
        if request.form['productName'] != '':
            product.productName = request.form['productName']
        if request.form['expiryDate'] != '':
            product.expiryDate = request.form['expiryDate']
        if request.form['manufacturingDate'] != '':
            product.manufacturingDate = request.form['manufacturingDate']
        if request.form['ratePerUnit'] != '':
            product.ratePerUnit = request.form['ratePerUnit']
        if request.form['inStock'] != '':
            product.inStock = request.form['inStock']
        db.session.commit()
        return redirect(url_for('updateProduct',categoryName=categoryName,productName=product.productName))
        return render_template('editProduct.html',categoryName=categoryName,productName=productName)
        #category = Category.query.filter_by(categoryName=categoryName).first()


@app.route('/delete/<categoryName>',methods=['GET'])
@login_required
def deleteCategory(categoryName):
    category_obj=Category.query.filter_by(categoryName=categoryName).first()
    print(category_obj.categoryName)
    db.session.delete(category_obj)
    db.session.commit()
    return redirect(url_for('addCategory'))
    return render_template('test.html')


@app.route('/delete/<categoryName>/<productName>',methods=['GET'])
@login_required
def deleteProduct(categoryName,productName):
    category = Category.query.filter_by(categoryName=categoryName).first()
    product= Product.query.filter_by(productName=productName,categoryId=category.categoryId).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('addProduct',categoryName=categoryName))

