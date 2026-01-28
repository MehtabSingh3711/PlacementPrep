from flask import Flask, render_template, request, session, redirect, url_for, flash
import math

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'  # Required for session

# --- Helper Logic for Calculator ---
def safe_calculate(expression):
    try:
        # Dangerous in production, but acceptable for this specific local task context
        # We will restrict the namespace to math functions
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        return str(eval(expression, {"__builtins__": None}, allowed_names))
    except Exception as e:
        return "Error"

# --- Helper Logic for Text Editor ---
class TextEditorLogic:
    @staticmethod
    def get_state():
        if 'text_state' not in session:
            session['text_state'] = {
                'text_buffer': [], # List of words
                'undo_stack': [],
                'redo_stack': []
            }
        return session['text_state']

    @staticmethod
    def save_state(state):
        session['text_state'] = state
        session.modified = True

    @staticmethod
    def write(text):
        state = TextEditorLogic.get_state()
        state['undo_stack'].append(state['text_buffer'].copy())
        state['redo_stack'] = [] # Clear redo on new action
        words = text.split()
        state['text_buffer'].extend(words)
        TextEditorLogic.save_state(state)

    @staticmethod
    def undo():
        state = TextEditorLogic.get_state()
        if not state['undo_stack']:
            return "Nothing to undo."
        
        state['redo_stack'].append(state['text_buffer'].copy())
        state['text_buffer'] = state['undo_stack'].pop()
        TextEditorLogic.save_state(state)
        return "Undid last action."

    @staticmethod
    def redo():
        state = TextEditorLogic.get_state()
        if not state['redo_stack']:
            return "Nothing to redo."
        
        state['undo_stack'].append(state['text_buffer'].copy())
        state['text_buffer'] = state['redo_stack'].pop()
        TextEditorLogic.save_state(state)
        return "Redid last action."

    @staticmethod
    def clear():
        session.pop('text_state', None)

# --- Helper Logic for Student List ---
class StudentListLogic:
    @staticmethod
    def get_students():
        if 'students' not in session:
            session['students'] = []
        return session['students']

    @staticmethod
    def save_students(students):
        session['students'] = students
        session.modified = True

    @staticmethod
    def add(s_id, name, grade, position='start'):
        students = StudentListLogic.get_students()
        new_student = {'student_id': int(s_id), 'name': name, 'grade': grade}
        
        # Check for duplicate ID
        if any(s['student_id'] == int(s_id) for s in students):
            return "Error: Student ID already exists."

        if position == 'end':
            students.append(new_student)
        else:
            students.insert(0, new_student)
        
        StudentListLogic.save_students(students)
        return f"Added student {name}."

    @staticmethod
    def delete(s_id):
        students = StudentListLogic.get_students()
        original_len = len(students)
        students = [s for s in students if s['student_id'] != int(s_id)]
        
        if len(students) == original_len:
            return "Student not found."
        
        StudentListLogic.save_students(students)
        return f"Deleted student ID {s_id}."

    @staticmethod
    def search(s_id):
        students = StudentListLogic.get_students()
        for s in students:
            if s['student_id'] == int(s_id):
                return s
        return None

# --- Routes ---

@app.route('/')
def index():
    return redirect(url_for('calculator'))

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if 'calc_history' not in session:
        session['calc_history'] = []
    
    result = None
    expression = ""

    if request.method == 'POST':
        expression = request.form.get('expression', '')
        cmd = request.form.get('cmd')

        if cmd == 'clear':
            expression = ""
        elif cmd == 'calculate':
            result = safe_calculate(expression)
            # Add to history if valid
            if result != "Error":
                session['calc_history'].insert(0, f"{expression} = {result}")
                session.modified = True
                expression = result # allow chaining
        elif cmd in ['add', 'sub', 'mul', 'div', 'pow']:
            map_op = {'add': '+', 'sub': '-', 'mul': '*', 'div': '/', 'pow': '**'}
            expression += map_op[cmd]
        elif cmd == 'sqrt':
             result = safe_calculate(f"sqrt({expression})")
             if result != "Error":
                session['calc_history'].insert(0, f"sqrt({expression}) = {result}")
                session.modified = True
                expression = result
        else:
            # Append number or symbol
            expression += cmd
    
    return render_template('calculator.html', 
                           active_tab='calculator', 
                           expression=expression, 
                           result=result, 
                           history=session['calc_history'])

@app.route('/text-editor', methods=['GET', 'POST'])
def text_editor():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'write':
            text = request.form.get('append_text', '')
            if text:
                TextEditorLogic.write(text)
                flash('Text appended.', 'success')
        elif action == 'undo':
            msg = TextEditorLogic.undo()
            flash(msg, 'info')
        elif action == 'redo':
            msg = TextEditorLogic.redo()
            flash(msg, 'info')
        elif action == 'clear':
            TextEditorLogic.clear()
            flash('Editor cleared.', 'warning')

    state = TextEditorLogic.get_state()
    current_text = " ".join(state['text_buffer'])
    
    return render_template('text_editor.html', 
                           active_tab='text_editor',
                           current_text=current_text,
                           undo_count=len(state['undo_stack']),
                           redo_count=len(state['redo_stack']))

@app.route('/student-list', methods=['GET', 'POST'])
def student_list():
    search_result = None
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            try:
                s_id = request.form.get('student_id')
                name = request.form.get('name')
                grade = request.form.get('grade')
                pos = request.form.get('position')
                msg = StudentListLogic.add(s_id, name, grade, pos)
                if "Error" in msg:
                    flash(msg, 'error')
                else:
                    flash(msg, 'success')
            except ValueError:
                 flash("Invalid input.", 'error')
                 
        elif action == 'delete':
            try:
                s_id = request.form.get('student_id')
                msg = StudentListLogic.delete(s_id)
                if "not found" in msg:
                     flash(msg, 'error')
                else:
                     flash(msg, 'success')
            except ValueError:
                 flash("Invalid ID format.", 'error')

        elif action == 'search':
            try:
                s_id = request.form.get('student_id')
                search_result = StudentListLogic.search(s_id)
                if not search_result:
                    flash(f"Student ID {s_id} not found.", 'error')
            except ValueError:
                 flash("Invalid ID format.", 'error')

    students = StudentListLogic.get_students()
    return render_template('student_list.html', 
                           active_tab='student_list',
                           students=students,
                           search_result=search_result)

if __name__ == '__main__':
    app.run(debug=True)
