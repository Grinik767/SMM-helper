from flask import Flask, render_template, abort, url_for
from data import db_session
import api
import os
from data.users import User
from data.works import Work

app = Flask(__name__, template_folder="templates")
db_session.global_init("db/data.db")
app.register_blueprint(api.blueprint)


@app.route('/<chat_id>/<secret_key>')
def index(chat_id, secret_key):
    db_sess = db_session.create_session()
    check_user = db_sess.query(User).get(int(chat_id))
    if check_user.ident == secret_key:
        works = db_sess.query(Work).filter(Work.chat_id == chat_id).all()
        ready_works = [
            ((url_for('static', filename=f"img/{ph}") for ph in work.photos.split(';')), work.text, work.result) for
            work in works]
        return render_template('jobs.html', title=f'Результаты: {chat_id}', chat_id=chat_id, works=ready_works)
    return abort(404)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)