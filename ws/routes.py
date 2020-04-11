from flask import abort, jsonify, make_response, request, url_for
from sqlalchemy import or_
from ws import app, db
from ws.models import Tasks

# error handlers

@app.errorhandler(400)
def errors(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def errors(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def errors(error):
    return make_response(jsonify({'error': 'Internal server error'}), 500)


# -------------------------------TASKS-------------------------------
# all results returned in JSON

# request all tasks
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    tasks = Tasks.query.all()

    if tasks == None or tasks == []:
        abort(404)

    return jsonify({'task':[make_public_task(task.to_json()) for task in tasks]})

@app.route('/todo_list', methods=['GET'])
def get_list():
    tasks = Tasks.query.all()

    if tasks == None or tasks == []:
        abort(404)

    return jsonify({'task':[make_public_task(task.to_json()) for task in tasks]})


# request task by id
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Tasks.query.get(task_id)

    if task == None or task == []:
        abort(404)
    return jsonify({'task': make_public_task(task.to_json())})

# post a new task
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    new_id = db.session.query(db.func.max(Tasks.id)).scalar() + 1
    task = Tasks(id=new_id, title=request.json['title'], description=request.json.get('description', ""), done=False )
    db.session.add(task)
    db.session.commit()
    task = Tasks.query.get(new_id)

    return jsonify({"task": make_public_task(task.to_json())}), 201

# update a task by id
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):    
    if not request.json:
        abort(400)
    if 'done' in request.json and (request.json['done'] not in [1, 0]):
        abort(400)

    task = Tasks.query.get(task_id)
    
    if task == None or task == []:
        abort(404)

    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)
    db.session.commit()
    task = Tasks.query.get(task_id)

    return jsonify({"task": make_public_task(task.to_json())})

# delete a task by id
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Tasks.query.get(task_id)
    
    if task == None or task == []:
        abort(404)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'result': True})

# return task uri
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task
