# -*- coding: utf-8 -*-

import os
from datetime import datetime

import dotenv
import sqlalchemy
import sqlalchemy.orm as orm
from bleach import clean
from flask import flash, redirect
from flask.app import Flask
from flask.globals import request
from flask.globals import session as flask_session
from flask.helpers import url_for
from flask.templating import render_template

from .db import Base, Post, User
from .libs import Evaluator

dotenv.load_dotenv()  # type: ignore


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

engine = sqlalchemy.create_engine(os.environ["DATABASE_URI"])
Base.metadata.create_all(engine)


@app.before_request
def before_request():
    flask_session["SIGN_IN_USER_ID"] = "Anonymous"
    flask_session["SIGN_IN_USER_NAME"] = "Anonymous"


@app.get("/")
def index():
    return render_template(
        "index.html",
        posts=reversed(posts_all()),
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/guideline")
def guideline():
    return render_template("guideline.html")


@app.get("/signin")
def signin():
    return render_template("signin.html")


@app.get("/signup")
def signup():
    return render_template("signup.html")


@app.post("/signin/")
def api_signin():
    data = request.form

    with orm.Session(engine) as session:
        user = session.get(User, data.get("user-id"))
        if user is None or user.id != data.get("user-id"):
            flash("ユーザ名またはパスワードが間違っています。")
            return redirect(url_for("signin"))

        flask_session["SIGN_IN_USER_ID"] = user.id
        flask_session["SIGN_IN_USER_NAME"] = user.name
        return redirect(url_for("index"))


@app.post("/signup/")
def create_new_user():
    data = request.form
    user_id = str(data.get("user-id"))
    user_name = str(data.get("user-name"))
    password = str(data.get("password"))

    with orm.Session(engine) as session:
        user = session.get(User, user_id)
        if user is not None:
            flash("そのIDは既に使われています。")
            return redirect(url_for("signup"))

        new_user = User(
            id=user_id,
            name=user_name,
            password=password,
            created_at=datetime.now(),
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    flask_session["SIGN_IN_USER_ID"] = user_id
    flask_session["SIGN_IN_USER_NAME"] = user_name
    return redirect(url_for("index"))


@app.get("/signout")
def signout():
    del flask_session["SIGN_IN_USER_ID"]
    del flask_session["SIGN_IN_USER_NAME"]
    return redirect(url_for("index"))


@app.get("/posts/")
def posts_all():
    order = request.args.get("ordering", "date-asc")
    match order:
        case "date-asc":
            order = Post.created_at
        case "date-desc":
            order = Post.created_at.desc()
        case "emotion-asc":
            order = Post.emotion_value
        case "emotion-desc":
            order = Post.emotion_value.desc()
        case _:
            order = Post.created_at

    with orm.Session(engine) as session:
        posts = session.query(Post).order_by(order).all()
        return [post.serialize() for post in posts]


@app.get("/posts/<int:post_id>/")
def posts(post_id: int):
    with orm.Session(engine) as session:
        post = session.get(Post, post_id)

        if post is None:
            return {"ok": False}
        else:
            return {
                "ok": True,
                "data": post.serialize(),
            }


@app.post("/posts/")
def create_new_post():
    data = request.form
    content = data.get("content", "")

    if not 0 < len(content) < 140:
        flash("投稿は1文字以上140字以下に制限されています。")
        return redirect(url_for("index"))

    # sanitize
    content = clean(
        content,
        tags=[
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "q",
            "big",
            "b",
            "small",
            "i",
            "u",
            "tt",
            "strike",
        ],
    )

    emotion = Evaluator.evaluate(content)

    with orm.Session(engine) as session:
        author_id = flask_session.get("SIGN_IN_USER_ID") or "Anonymous"  # type: ignore
        new_post = Post(
            author_id=author_id,
            content=content,
            emotion_value=round(emotion.value, 3),
            emotion_label=emotion.label,
            color=f"rgba({emotion.rgb.r}, {emotion.rgb.g}, {emotion.rgb.b}, 0.7)",
            sender_addr=request.remote_addr,
            created_at=datetime.now(),
        )
        session.add(new_post)
        session.commit()
        session.refresh(new_post)

    return redirect(url_for("index"))


@app.delete("/posts/<int:post_id>/")
def delete_post(post_id: int):
    with orm.Session(engine) as session:
        post = session.get(Post, post_id)
        if post is None:
            return {"ok": False, "msg": "投稿が見つかりませんでした。"}
        else:
            session.delete(post)
            session.commit()
            return {"ok": True}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
