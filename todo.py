from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__,template_folder='templates')


todos = [
    {"id": 1, "name": "item1","done": False},
    {"id": 2, "name": "item2","done": False},
    {"id": 3, "name": "item3","done": False}
]

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    new_todo = {
        "id": len(todos) + 1,
        "name": request.form['name'],
        "done": False
    }
    todos.append(new_todo)
    return redirect(url_for('index'))

@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if request.method == "POST":
        todo["name"] = request.form["name"]
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo, index=todo_id)
    
@app.route('/delete/<int:todo_id>', methods=['POST',"GET"])
def delete(todo_id):
    # del todos[todo_id - 1]
    # return redirect(url_for('index'))
    
    # Find the todo item by its ID
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo:
        todos.remove(todo)  # Safely remove the todo item
    return redirect(url_for('index'))

@app.route("/check/<int:todo_id>", methods=["POST","GET"])
def check(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo:
        todo["done"] = not todo["done"]
    return redirect(url_for('index'))

@app.route("/clear", methods=["POST","GET"])
def clear():
    global todos
    todos = [todo for todo in todos if not todo["done"]]
    return redirect(url_for('index'))

@app.route("/clear_all", methods=["POST","GET"])
def clear_all():
    global todos
    todos = []
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)
