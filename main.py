# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///postdata.db'
app.config['SECRET_KEY']= 'secret key'

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False, )
    created_at = db.Column(db.DateTime, nullable=False)


def format_delta(before: datetime, after: datetime) -> str:
    delta = (after - before).seconds
    if (days := delta // 86400):
        return f'{days}日前'
    if (hours := delta // 3600):
        return f'{hours}時間前'
    if (minutes := delta // 60):
        return f'{minutes}分前'
    if (seconds := delta // 1):
        return f'{seconds}秒前'
    return f'ちょっと前'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        now = datetime.now()
        posts = reversed(Post.query.order_by('created_at').all())
        return render_template('index.html',
                               posts=posts,
                               now=now,
                               f=format_delta,
                               draft=session.get('draft', ''))

    if request.method == 'POST':
        content = request.form.get('content')
        if len(content) < 1:
            flash('何か書いてください')
            return redirect('/')
        if 140 < len(content):
            flash('もう少し短くしてください')
            session['draft'] = content
            return redirect('/')

        new_post = Post(content=request.form.get('content'),
                        created_at=datetime.now())

        db.session.add(new_post)
        db.session.commit()
        session['draft'] = ''
        return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin', methods=['GET', 'POST'])
def administrate():
    ...

if __name__ == '__main__':
    app.run(debug=True)