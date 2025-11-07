from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)

# Create DB tables (only the first time)
with app.app_context():
    db.create_all()

# Home Route (List Students)
@app.route('/')
def home():
    students = Student.query.all()
    return render_template('index.html', std=students)

# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        class_name = request.form['class']
        email = request.form['email']

        new_student = Student(name=name, roll=roll, class_name=class_name, email=email)
        db.session.add(new_student)
        db.session.commit()
        flash("✅ Student added successfully!", "success")
        return redirect(url_for('home'))

    return render_template('add.html')

# Edit / Update Student
@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.roll = request.form['roll']
        student.class_name = request.form['class']
        student.email = request.form['email']
        db.session.commit()
        flash("✏️ Student updated successfully!", "info")
        return redirect(url_for('home'))

    return render_template('edit.html', student=student)

# Delete Student
@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("🗑️ Student deleted successfully!", "danger")
    return redirect(url_for('home'))

# Static pages
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
