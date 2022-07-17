# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth

from libs import (TextScore,
                  format_time_delta,
                  convert_emotion_value_to_text,
                  convert_emotion_value_to_rgba,
                  )


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/posts.db '
db = SQLAlchemy(app)

app.config['BASIC_AUTH_USERNAME'] = 'dakken'
app.config['BASIC_AUTH_PASSWORD'] = 'da2022'

basic_auth = BasicAuth(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    emotion_value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        now = datetime.now()
        posts = reversed(Post.query.order_by('created_at').all())
        return render_template('index.html',
                               posts=posts,
                               now=now,
                               formatter=format_time_delta,
                               classifier=convert_emotion_value_to_text,
                               layer=convert_emotion_value_to_rgba,
                               draft=session.get('draft', ''),
                               )

    if request.method == 'POST':
        content = request.form.get('content')

        # validation
        if not 1 < len(content) < 140:
            flash('投稿は1～140文字に制限されています')
            session['draft'] = content
            return redirect('/')

        new_post = Post(content=content,
                        emotion_value=round(TextScore(content), 3),
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
