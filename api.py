import flask
from flask import jsonify
from data import db_session
from flask import request
from data.users import User
from data.works import Work
from random import choice

blueprint = flask.Blueprint(
    'api_db',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user', methods=['POST'])
def user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['chat_id', 'ident']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    check = db_sess.query(User).get(request.json['chat_id'])
    if db_sess.query(User).get(request.json['chat_id']):
        check.ident = request.json['ident']
    else:
        job = User(
            chat_id=request.json['chat_id'],
            ident=request.json['ident']
        )
        db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/work_photos', methods=['POST'])
def work_photos():
    try:
        photos = list(request.files)
        photo_names = []
        for photo in photos:
            f = request.files[photo].read()
            name = f"{make_secret_key()}.jpg"
            with open(f"static/img/{name}", 'wb') as img:
                img.write(f)
            photo_names.append(name)
        return jsonify({'names': photo_names})
    except Exception:
        return jsonify({'error': 'Unexpected error'})


@blueprint.route('/api/work', methods=['POST'])
def work():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['photos', 'text', 'chat_id', 'result']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    work = Work(
        photos=request.json['photos'],
        text=request.json['text'],
        chat_id=request.json['chat_id'],
        result=request.json['result']
    )
    db_sess.add(work)
    db_sess.commit()
    return jsonify({'success': 'OK'})


def make_secret_key():
    alph = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [chr(i) for i in range(48, 58)]
    return ''.join([choice(alph) for _ in range(30)])
