# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth


app = Flask(__name__)
app.config['SECRET_KEY']= 'secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///postdata.db'
db = SQLAlchemy(app)

app.config['BASIC_AUTH_USERNAME'] = 'dakken'
app.config['BASIC_AUTH_PASSWORD'] = '2022'

basic_auth = BasicAuth(app)



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


@app.route('/admin')
@basic_auth.required
def admin():
    return render_template('manage.html', posts=Post.query.all())

@app.route('/del/<int:post_id>')
@basic_auth.required
def delete(post_id):
    db.session.delete(Post.query.get(post_id))
    db.session.commit()
    return redirect('/admin')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@basic_auth.required
def edit(post_id):
    post = Post.query.get(post_id)
    if request.method == 'GET':
        return render_template('edit.html', post=post)
    if request.method == 'POST':
        post.content = request.form.get('content')
        db.session.commit()
        return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)