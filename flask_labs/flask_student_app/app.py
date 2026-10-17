from flask import Flask, render_template, request, redirect, url_for  # type: ignore[reportMissingImports]

app = Flask(__name__)

# Volatile data store: a list of dictionaries kept in RAM.
# It is emptied every time the server stops.
student_database_records = []


def find_student(roll):
    """Return the student dictionary with this roll number, or None."""
    for student in student_database_records:
        if student['roll'] == roll:
            return student
    return None


# CREATE + READ: one function serves the page (GET) and the form (POST)
@app.route('/', methods=['GET', 'POST'])
def student_dashboard_portal():
    error = None
    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        roll_number = request.form.get('roll_number', '').strip()
        department = request.form.get('department', '').strip()
        email = request.form.get('email', '').strip()

        if not (student_name and roll_number):
            error = 'Name and roll number are required.'
        elif find_student(roll_number):
            error = 'Roll number ' + roll_number + ' is already registered.'
        else:
            student_database_records.append({
                'name': student_name,
                'roll': roll_number,
                'department': department,
                'email': email,
            })
            # Post/Redirect/Get: avoids duplicate records on page refresh
            return redirect(url_for('student_dashboard_portal'))

    return render_template('index.html',
                           students=student_database_records,
                           error=error)


# UPDATE: show a pre-filled form (GET) and save the changes (POST)
@app.route('/edit/<roll>', methods=['GET', 'POST'])
def edit_student(roll):
    student = find_student(roll)
    if student is None:
        return redirect(url_for('student_dashboard_portal'))

    error = None
    if request.method == 'POST':
        new_name = request.form.get('student_name', '').strip()
        if not new_name:
            error = 'Name cannot be empty.'
        else:
            student['name'] = new_name
            student['department'] = request.form.get('department', '').strip()
            student['email'] = request.form.get('email', '').strip()
            return redirect(url_for('student_dashboard_portal'))

    return render_template('edit.html', student=student, error=error)


# DELETE: only accepts POST so a link click can never delete by accident
@app.route('/delete/<roll>', methods=['POST'])
def delete_student(roll):
    student = find_student(roll)
    if student:
        student_database_records.remove(student)
    return redirect(url_for('student_dashboard_portal'))


if __name__ == '__main__':
    app.run(debug=True)