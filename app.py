from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
app = Flask(__name__)

#config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'university'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize MySQL
mysql = MySQL(app)

#INDEX
@app.route('/')
def index():
    return render_template('home.html')

#Query 1 FORM CLASS
class DetailsForm(Form):
    rno = StringField('Roll Number',[validators.Length(min=1,max=5)])
    name = "-----"
    dept_name ="-----"
    courses=[]
#Query 1 Route
@app.route('/Query1',methods = ['GET','POST'])
def Query1():
    form = DetailsForm(request.form)
    if request.method == 'POST' and form.validate():
        rno = form.rno.data
        cur = mysql.connection.cursor()
        #collecting Student name and dept_name
        result = cur.execute("select name,dept_name from student where ID = %s ",[rno])
        Student = cur.fetchone()
        result = cur.execute("select t.course_id,c.title,c.credits,t.grade from takes t join course c on c.course_id=t.course_id where ID =%s",[rno])
        course = cur.fetchall()
        if result>0:
            form.name=Student["name"]
            form.dept_name=Student["dept_name"]
            form.courses = course
            cur.close()
        else:
            flash("No Such Roll Number Exists",'danger')
            return redirect(url_for('Query1'))

    return render_template('Query1.html', form =form)

#Query 2 class
class SubjectForm(Form):
    word = StringField('Word',[validators.Length(min=1,max=10)])
    subjects=[]
#Query 2 route
@app.route('/Query2', methods=['GET','POST'])
def Query2():
    form = SubjectForm(request.form)
    if request.method == 'POST' and form.validate():
        word = form.word.data
        #create cursor
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT course_id,title FROM course WHERE title LIKE '%{0}%' ".format(word))
        subject = cur.fetchall()
        if(result>0):
            form.subjects = subject
        else:
            flash("Word Not Found !",'danger')
    return render_template('Query2.html', form =form)

#Query 3
@app.route('/Query3')
def Query3():
    #create cursor
    cur = mysql.connection.cursor()
    result = cur.execute("select t.ID,s.name from takes t join student s on t.ID=s.ID where grade='F' group by t.ID having count(t.ID)>=2")
    students = cur.fetchall()

    if result>0:
        return render_template('Query3.html',students = students)
    else:
        msg = 'Error Occured'
        return render_template('Query3.html',msg=msg)
    cur.close()

#Query 4 FORM CLASS
class RegisterForm(Form):
    rno = StringField('Roll Number',[validators.Length(min=1,max=5)])
    name = StringField('Name',[validators.Length(min=1,max=25)])
    dept_name = StringField('Department Name',[validators.Length(min=2,max=20)])

#Query 4
@app.route('/Query4',methods = ['GET','POST'])
def Query4():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        rno = form.rno.data
        name = form.name.data
        dept_name = form.dept_name.data
        cur = mysql.connection.cursor()
        tot_cred=0

        result = cur.execute("select * from department where dept_name = %s ",[dept_name])
        Department = cur.fetchall()
        if result>0:
            try:
                cur.execute("insert into student values(%s,%s,%s,%s)", (rno,name,dept_name,tot_cred))
                mysql.connection.commit()
                flash('Student Record Saved!','success')
                return redirect(url_for('Query4'))
            except :
                flash("Roll Number already Exists",'danger')
                return redirect(url_for('Query4'))
        else:
            flash("No Such Department Exists",'danger')
            return redirect(url_for('Query4'))
        cur.close()
    return render_template('Query4.html', form =form)

if __name__=='__main__':
    app.secret_key ='secret123'
    app.run(debug=True)
