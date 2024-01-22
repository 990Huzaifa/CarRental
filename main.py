import os
import re
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'new sec'

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'car_rental'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





mysql = MySQL(app)

# Function to check a hashed password
def check_password(hashed_password, password):
    return pbkdf2_sha256.verify(password, hashed_password)

def fetch(table):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM `{}`'.format(table))
    data_list = cur.fetchall()
    mysql.connection.commit()
    return data_list

def fetch_by_id(table, id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM `{}` WHERE id = %s'.format(table), (id,))
    data_list = cur.fetchone()
    mysql.connection.commit()
    return data_list

def count(table):
    cur=mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM `{}`'.format(table))
    count_result = cur.fetchone()[0]
    mysql.connection.commit()
    return count_result

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_brand(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT name FROM brand WHERE id = %s', (id,))
    brand = cur.fetchone()
    if brand:
        return brand[0]
    else:
        return 'not found'

def get_result(id, table, col):
    cur = mysql.connection.cursor()
    query = 'SELECT {} FROM `{}` WHERE id = %s'.format(col, table)
    cur.execute(query, (id,))
    data = cur.fetchone()
    mysql.connection.commit()
    return data[0] if data else None

def related_car(brand_id,id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM car WHERE brand_id = %s AND id != %s LIMIT 3', (brand_id, id, ))
    brand = cur.fetchall()
    mysql.connection.commit()
    return brand

# index required fucntions

def items(table, limit):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM {} ORDER BY id DESC LIMIT %s'.format(table), (int(limit),))
    data_list = cur.fetchall()
    mysql.connection.commit()
    return data_list

def testimonial():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM testimonials WHERE status="active" LIMIT 5')
    data_list=cur.fetchall()
    mysql.connection.commit()
    return data_list

def paginate_data(data, page_size=6):
    page = request.args.get('page', 1, type=int)
    total_items = len(data)
    total_pages = (total_items + page_size - 1) // page_size

    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, total_items)

    paginated_data = data[start_index:end_index]

    return paginated_data, total_pages, page, total_items

# user view



    

@app.route('/')
def index():
    contact=fetch('contact_details')
    general=fetch('general')
    car_count = count('car')
    user_count = count('user')
    car_item=items('car',5)
    services_item=items('services',3)
    testimonials=testimonial()
    return render_template('index.html',contact=contact,general=general,car_count=car_count,user_count=user_count,services_item=services_item,car_item=car_item,get_brand=get_brand,testimonials=testimonials)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin'in session:
        return redirect('profile')
    else:
        msg = ''
        contact=fetch('contact_details')
        general=fetch('general')
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM user WHERE email = %s', (email, ))
            user = cur.fetchone()

            if user:
                stored_password = user[4]

                if check_password(stored_password, password):
                    
                    user_type = user[5]
                    if(user_type == 'customer'):
                        session['type'] =user_type
                        session['loggedin'] = True
                        session['id'] = user[0]
                        session['name'] = user[1]
                        msg = 'Login successful'
                        return redirect(url_for('profile'))

                    else:
                        session['type'] =user_type
                        session['loggedin'] = True
                        session['id'] = user[0]
                        session['name'] = user[1]
                        msg = 'Login successful'
                        return redirect(url_for('dashboard'))
                else:
                    msg = 'Incorrect password!'
            else:
                msg = 'User not found!'
    return render_template('login.html', msg=msg,contact=contact,general=general)

@app.route('/register', methods = ['GET','POST'])
def register():
    msg = ''
    contact=fetch('contact_details')
    general=fetch('general')
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']      
        acc_type = 'customer'     
        hash_password = pbkdf2_sha256.hash(password)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE fullname = %s AND email =%s ', (fullname, email, ))
        user = cur.fetchone()
        if user:
            msg = 'username or email already exists!'
        elif not fullname or not email or not hash_password:
            msg = 'Please fill out the form!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid Email'
        elif not re.match(r'[a-zA-Z0-9]+', fullname):
            msg = 'Username must contain only characters and numbers!'        
        else:
            cur.execute('INSERT INTO user (fullname, email, phone, password, account_type) VALUES (%s, %s, %s, %s, %s)', (fullname, email, phone, hash_password, acc_type))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
         
    return render_template('register.html', msg=msg,contact=contact,general=general)

@app.route('/contact',methods = ['GET','POST'])
def contact():
    msg=''
    contact=fetch('contact_details')
    general=fetch('general')
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        subject=request.form['subject']
        message=request.form['message']
        if not re.match(r'[a-zA-Z0-9]+',name) and not re.match(r'[a-zA-Z0-9]+',subject):
            msg = 'Username or subject must contain only characters and numbers!'
        else:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO contact (name, email, subject, message) VALUES (%s, %s, %s, %s)',(name, email, subject, message, ))
            mysql.connection.commit()
            msg='Thanks for your feedback'
    return render_template('contact.html',contact=contact,general=general,msg=msg)

@app.route('/about')
def about():
    contact=fetch('contact_details')
    general=fetch('general')
    car_count = count('car')
    user_count = count('user')
    testimonials=testimonial()
    return render_template('about.html',contact=contact,general=general,car_count=car_count,user_count=user_count,testimonials=testimonials)

@app.route('/services')
def services():
    data=fetch('services')
    contact=fetch('contact_details')
    general=fetch('general')
    return render_template('services.html',data=data,contact=contact,general=general)

@app.route('/cars' , endpoint='cars')
def cars():
    data_list = fetch('car')
    paginated_data, total_pages, current_page, total_items = paginate_data(data_list)

    contact = fetch('contact_details')
    general = fetch('general')

    return render_template('car.html', data_list=paginated_data, get_brand=get_brand, contact=contact, general=general, total_pages=total_pages, current_page=current_page, total_items=total_items)

@app.route('/car/<string:id>')
def car(id):
    data=fetch_by_id('car',id)
    contact=fetch('contact_details')
    general=fetch('general')
    return render_template('car-single.html',data=data,contact=contact,general=general,get_brand=get_brand,related_car=related_car)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    title='profile'
    contact=fetch('contact_details')
    general=fetch('general')
    if('loggedin' in session and session['type'] == 'admin'):
        return redirect(url_for('dashboard'))
    elif('loggedin' in session and session['type'] == 'customer'):
        user_id=session['id']
        data = fetch_by_id('user',user_id)
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM booking WHERE user_id = %s',(user_id,))
        booking_history = cur.fetchall()
        mysql.connection.commit()
        return render_template('profile.html',title=title,data=data,booking_history=booking_history,get_result=get_result,contact=contact,general=general)
    return redirect(url_for('login'))

@app.route('/booknow/<string:id>',methods = ['GET','POST'])
def booknow(id):
    if ('loggedin' in session and session['type']=='customer'):
        services = fetch('services')
        data=fetch_by_id('car',id)
        contact=fetch('contact_details')
        general=fetch('general')
        if request.method == 'GET':
            return render_template('book_now.html',data=data,services=services,contact=contact,general=general)
        elif request.method == 'POST':
            pointA = request.form['pointa']
            pointB = request.form['pointb']
            pickupdate = request.form['pickupdate']
            pickuptime = request.form['pickuptime']
            service_id = request.form['service']
            user_id=session['id']
            data2=fetch_by_id('services',service_id)
            data3=fetch_by_id('user',user_id)
            phone=data3[3]
            price=data2[2]
            ex_charges=data[3]
            t_amount=price+ex_charges
            status='request'
            cur=mysql.connection.cursor()
            cur.execute('INSERT INTO booking (car_id, user_id, departure, arrival, phone, pickup_date, pickup_time, service_id, t_amount, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (id,user_id,pointA,pointB,phone,pickupdate,pickuptime,service_id,t_amount,status,))
            mysql.connection.commit()
            return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/posttestimonial',methods=['GET','POST'])
def post_testimonial():
    if request.method == 'POST':
        if request.method == 'POST':
            name=request.form['fullname']
            occupation=request.form['occupation']
            message=request.form['message']
            status='inactive'
            if not re.match(r'[a-zA-Z0-9]+',name) and not re.match(r'[a-zA-Z0-9]+',occupation):
                msg = 'Username or subject must contain only characters and numbers!'
            else:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO testimonials (fullname, occupation, message, status) VALUES (%s, %s, %s, %s)',(name, occupation, message, status,))
                mysql.connection.commit()
    return redirect('profile')

@app.route('/editprofile/<string:id>',methods=['GET','POST'])
def edit_profile(id):
    if request.method == 'POST':
        if request.method == 'POST':
            name=request.form['fullname']
            email=request.form['email']
            phone=request.form['phone']
            if not re.match(r'[a-zA-Z0-9]+',name):
                msg = 'Username must contain only characters and numbers!'
            else:
                cur = mysql.connection.cursor()
                cur.execute('UPDATE user SET fullname = %s, email = %s, phone = %s WHERE id = %s',(name,email,phone,id,))
                mysql.connection.commit()
    return redirect(url_for('profile'))

@app.route('/cancel/<string:id>', methods=['POST','GET'])
def cancel_booking(id):
    status = 'cancel'
    cur=mysql.connection.cursor()
    cur.execute('UPDATE booking SET status = %s WHERE id = %s',(status,id))
    mysql.connection.commit()
    return redirect(url_for('profile'))

# admin view


@app.route('/dashboard')
def dashboard():
    title='dashboard'
    if('loggedin' in session and session['type'] == 'admin'):
        car_count = count('car')
        user_count = count('user')
        booking_count = count('booking')
        contact_count = count('contact')
        return render_template('admin/dashboard.html',title=title,car_count=car_count,booking_count=booking_count,contact_count=contact_count,user_count=user_count)
    elif('loggedin' in session and session['type'] == 'customer'):
        return redirect(url_for('profile'))
    return redirect(url_for('login'))
    
@app.route('/setting', methods = ['POST','GET'])
def setting():
    title='dashboard'
    if('loggedin' in session and session['type']=='admin'):
        general=fetch('general')
        contact_info=fetch('contact_details')
        return render_template('admin/setting.html',title=title,general=general,contact_info=contact_info)
    return redirect(url_for('profile'))

@app.route('/addbrand', methods = ['GET','POST'])
def addbrand():
    title='Add brand'
    if('loggedin' not in session):
        return redirect(url_for('login'))
    msg=''
    if request.method == 'POST':
        brand_name = request.form['brand']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO brand (name) VALUES(%s)', (brand_name, ))
        mysql.connection.commit()
        msg = 'You have successfully registered!'
    return render_template('admin/add_brand.html',title=title,msg=msg)

@app.route('/brandlist')
def brandlist():
    if('loggedin' not in session):
        return redirect(url_for('login'))
    title='Brand List'
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM brand')
    data_list = cur.fetchall()
    mysql.connection.commit()
    return render_template('admin/brand_list.html',title=title,data_list=data_list)

@app.route('/addcar', methods = ['GET','POST'])
def addcar():
    if('loggedin' not in session):
        return redirect(url_for('login'))
    title='Add Car'
    msg=''
    brand_list=fetch('brand')
    if request.method == 'POST':
        brand_id = request.form['brand_id']
        name = request.form['name']
        ex_charges = request.form['ex_charges']
        seaters = request.form['seaters']
        model = request.form['model']
        
        # Check if the post-upload field is in the request and is a valid file
        if 'post-upload' in request.files and allowed_file(request.files['post-upload'].filename):
            img = request.files['post-upload']
            # Save the file to the specified folder
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO car (brand_id, name, extra_charges, seaters, model, img) VALUES(%s, %s, %s, %s, %s, %s)', (brand_id, name, ex_charges, seaters, model, filename))
            mysql.connection.commit()
            msg = 'Car successfully registered!'
        else:
            msg = 'Invalid file format. Please upload a valid image file.'
    return render_template('admin/add_car.html',title=title,msg=msg,brand_list=brand_list)

@app.route('/deletecar/<string:id>', methods = ['GET'])
def deletecar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM car WHERE id = %s',(id,))
    mysql.connection.commit()
    return redirect(url_for('carlist'))

@app.route('/editcar/<string:id>', methods = ['GET', 'POST'])
def editcar(id):
    brand_list=fetch('brand')
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM car WHERE id = %s',(id,))
        item = cur.fetchone()
        return render_template('admin/edit_car.html',item=item,brand_list=brand_list)
    elif request.method == 'POST':
        brand_id = request.form['brand_id']
        name = request.form['name']
        ex_charges = request.form['ex_charges']
        seaters = request.form['seaters']
        model = request.form['model']
        # get img
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM car WHERE id = %s',(id,))
        item = cur.fetchone()
        old_img = item[6]
        if 'edit-post-upload' in request.files and allowed_file(request.files['edit-post-upload'].filename):
            img = request.files['edit-post-upload']
            # Save the file to the specified folder
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #  delete old img
            if old_img:
                old_img_path = os.path.join(app.config['UPLOAD_FOLDER'], old_img)
                if os.path.exists(old_img_path):
                    os.remove(old_img_path)
            
            cur.execute('UPDATE car SET brand_id=%s, name=%s, extra_charges=%s, seaters=%s, model=%s, img=%s WHERE id = %s',(brand_id,name,ex_charges,seaters,model,filename,id))
            mysql.connection.commit()  # Commit the transaction
            cur.close()
        else:
            cur.execute('UPDATE car SET brand_id=%s, name=%s, extra_charges=%s, seaters=%s, model=%s, img=%s WHERE id = %s',(brand_id, name, ex_charges, seaters, model, old_img, id))
            mysql.connection.commit()  # Commit the transaction
            cur.close()

        return redirect(url_for('carlist'))
        
@app.route('/deletebrand/<string:id>', methods = ['GET'])
def deletebrand(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM brand WHERE id = %s',(id,))
    mysql.connection.commit()
    return redirect(url_for('brandlist'))

@app.route('/editbrand/<string:id>', methods = ['GET', 'POST'])
def editbrand(id):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM brand WHERE id = %s',(id,))
        item = cur.fetchone()
        return render_template('admin/edit_brand.html',item=item)
    elif request.method == 'POST':
        name = request.form['brand']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE brand SET name=%s WHERE id = %s',(name, id))
        mysql.connection.commit()  # Commit the transaction
        cur.close()

        return redirect(url_for('brandlist'))

@app.route('/carlist')
def carlist():
    if('loggedin' not in session):
        return redirect(url_for('login'))
    title='Car List'
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM car')
    data_list = cur.fetchall()
    mysql.connection.commit()
    return render_template('admin/car_list.html',title=title,data_list=data_list,get_brand=get_brand)

@app.route('/addservice', methods = ['POST', 'GET'])
def addservice():
    if('loggedin' not in session):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name=request.form['name']
        charges=request.form['charges']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO services(name, price)VALUES(%s, %s)',(name, charges))
        mysql.connection.commit()
    return render_template('admin/add_services.html')

@app.route('/servicelist', methods = ['POST', 'GET'])
def servicelist():
    if('loggedin' not in session):
        return redirect(url_for('login'))
    data = fetch('services')
    return render_template('admin/services_list.html',data=data)

@app.route('/userlist', methods = ['POST', 'GET'])
def userlist():
    if('loggedin' not in session):
        return redirect(url_for('login'))
    data = fetch('user')
    return render_template('admin/user_list.html',data=data)

@app.route('/testimonialslist')
def testimonialslist():
    if('loggedin' not in session):
        return redirect(url_for('login'))
    data = fetch('testimonials')
    return render_template('admin/testimonials_list.html',data=data)

@app.route('/managetestimonial/<string:id>', methods = ['POST', 'GET'])
def managetestimonial(id):
    if request.method == 'GET':
        data=fetch_by_id('testimonials',id)
        return render_template('admin/manage_testimonials.html',data=data,get_result=get_result)
    elif request.method == 'POST':
        status=request.form['status']
        cur=mysql.connection.cursor()
        cur.execute('UPDATE testimonials SET status = %s WHERE id = %s',(status,id))
        mysql.connection.commit()
        return redirect(url_for('testimonialslist'))

@app.route('/contactlist', methods = ['POST', 'GET'])
def contactlist():
    if('loggedin' not in session):
        return redirect(url_for('login'))
    data = fetch('contact')
    return render_template('admin/contact_list.html',data=data)

@app.route('/editservice/<string:id>', methods = ['POST', 'GET'])
def editservice(id):
    if request.method == 'GET':
        data=fetch_by_id('services',id)
        return render_template('admin/edit_services.html',data=data)
    elif request.method == 'POST':
        name=request.form['name']
        charges=request.form['charges']
        cur=mysql.connection.cursor()
        cur.execute('UPDATE services SET name = %s, price = %s WHERE id = %s',(name, charges,id))
        mysql.connection.commit()
    return redirect(url_for('servicelist'))

@app.route('/bookings')
def bookings():
    if('loggedin' not in session):
        return redirect(url_for('login'))
    data=fetch('booking')
    return render_template('admin/bookings.html',data=data,get_result=get_result)

@app.route('/updatebooking/<string:id>', methods = ['POST', 'GET'])
def updatebooking(id):
    if request.method == 'GET':
        data=fetch_by_id('booking',id)
        return render_template('admin/update_booking.html',data=data,get_result=get_result,get_brand=get_brand)
    elif request.method == 'POST':
        status=request.form['status']
        cur=mysql.connection.cursor()
        cur.execute('UPDATE booking SET status = %s WHERE id = %s',(status,id))
        mysql.connection.commit()
        return redirect(url_for('bookings'))

@app.route('/deleteservice/<string:id>', methods = ['POST', 'GET'])
def deleteservice(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM services WHERE id = %s',(id))
    mysql.connection.commit()
    return redirect(url_for('servicelist'))

# site setting for admin

@app.route('/general',methods=['GET','POST'])
def general():
    if request.method == 'POST':
        id = request.form['id']
        if id != '':
            id=request.form['id']
            site_title=request.form['site_title']
            site_description=request.form['site_description']
            site_tags=request.form['tags']
            m_mode = request.form.get('maintainance')
            value=''
            if m_mode =='maintainance' :
                value = 'checked'  
            cur=mysql.connection.cursor()
            cur.execute('UPDATE general SET site_title=%s, site_description=%s, site_tag=%s, mm=%s WHERE id = %s',(site_title,site_description,site_tags,value,id))
            mysql.connection.commit()
        else:
            site_title=request.form['site_title']
            site_description=request.form['site_description']
            site_tags=request.form['tags']
            m_mode = request.form.get('maintainance')
            value=''
            if m_mode =='maintainance' :
                value = 'checked' 
            
            cur=mysql.connection.cursor()
            cur.execute('INSERT INTO general (site_title, site_description, site_tag, mm) VALUES (%s, %s, %s, %s)',(site_title, site_description, site_tags, value, ))
            mysql.connection.commit()
    return redirect('setting')

@app.route('/contactinfo',methods=['GET','POST'])
def contactinfo():
    if request.method == 'POST':
        id = request.form['id']
        if id != '':
            id=request.form['id']
            email=request.form['email']
            location=request.form['location']
            phone=request.form['phone']
            m_mode = request.form.get('form')
            value=''
            if m_mode =='form' :
                value = 'checked'  
            cur=mysql.connection.cursor()
            cur.execute('UPDATE contact_details SET email=%s, phone=%s, location=%s, form=%s WHERE id = %s',(email,phone,location,value,id))
            mysql.connection.commit()
        else:
            email=request.form['email']
            location=request.form['location']
            phone=request.form['phone']
            m_mode = request.form.get('form')
            value=''
            if m_mode =='form' :
                value = 'checked' 
            
            cur=mysql.connection.cursor()
            cur.execute('INSERT INTO contact_details (email, phone, location, form) VALUES (%s, %s, %s, %s)',(email, phone, location, value, ))
            mysql.connection.commit()
    return redirect('setting')

@app.route('/resetpass',methods=['GET','POST'])
def reset_pass():
    if request.method == 'POST':
        id=request.form['id']
        password=request.form['password']
        hash_password = pbkdf2_sha256.hash(password)
        cur = mysql.connection.cursor()
        cur.execute('UPDATE user SET password = %s WHERE id = %s',(hash_password,id))
        mysql.connection.commit()
        return redirect(url_for('setting'))



if __name__ == "__main__":
    app.run(debug=True)