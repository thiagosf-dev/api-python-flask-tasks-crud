from crypt import methods

from flask import Flask, jsonify, request
from models.task import Task

# __name__ = __main__
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/about")
def about():
    return "About"


tasks = []
task_id_control = 1


@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(
        id=task_id_control,
        title=data.get("title", ""),
        description=data.get("description", "")
    )
    tasks.append(new_task)
    task_id_control += 1
    return jsonify({
        "message": "Nova tarefa criada com sucesso."
    }), 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }

    return jsonify(output)


@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task_found = None
    for task in tasks:
        if task.id == id:
            task_found = task
            return jsonify(task_found.to_dict())

    return jsonify({
        "message": "Task não encontrada."
    }), 404


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task_found = None
    for task in tasks:
        if task.id == id:
            task_found = task
            break

    if task_found == None:
        return jsonify({
            "message": "Task não encontrada."
        }), 404

    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]

    return jsonify({
        "message": "Task atualizada."
    })


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task_found = None
    for task in tasks:
        if task.id == id:
            task_found = task
            break

    if not task_found:
        return jsonify({
            "message": "Task não encontrada."
        }), 404

    tasks.remove(task_found)

    return jsonify({
        "message": "Task removida."
    })


if __name__ == "__main__":
    app.run(debug=True)
