import sqlite3
from flask import abort, g, flash, redirect, request, render_template, url_for, Flask

# configuration
DATABASE = 'userstory.db'
SECRET_KEY = 'Y\xf6\xf2j\xc9\xc5\xbc\xde{\xae\x9a\xc8\x8dZ0\x9e\x14\xb6\x90\xd7\x02\x03\xf0\x1a'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


# Working with SQLite3

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


# The application Views


@app.route('/')
def list_user_story():
    """
    Returns a list of user stories.
    """
    stories = query_db('select * from userstory order by ordinal')
    return render_template("index.html", stories=stories)


@app.route('/add', methods=['POST'])
def add_user_story():
    """
    Add a new user story.
    """
    who = request.form.get('who')
    what = request.form.get('what')
    why = request.form.get('why')
    if not (who and what and why):
        abort(400)
    g.db.execute('insert into userstory (who, what, why, ordinal) values (?, ?, ?, 0)',
            [who, what, why])
    g.db.commit()
    flash('A new user story has been created', 'success')
    return redirect(url_for('list_user_story'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user_story(id):
    g.db.execute('delete from userstory where id = ?', [id])
    g.db.commit()
    flash('You deleted the user story.', 'success')
    return redirect(url_for('list_user_story'))


if __name__ == '__main__':
    app.run("0.0.0.0")
