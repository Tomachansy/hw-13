from flask import Flask, request, render_template, send_from_directory, abort
from functions import *

POST_PATH = "posts.json"
data = get_json(POST_PATH)
UPLOAD_FOLDER = "uploads/images"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def page_index():
    tags = get_tags(data)
    return render_template("index.html", tags=sorted(tags))


@app.route("/tag")
def page_tag():
    tag = request.args.get("tag")
    if tag:
        posts = get_post_by_tag(data, tag)
        return render_template("post_by_tag.html", tag=tag, posts=posts)
    return abort(400)


@app.route("/post", methods=["GET", "POST"])
def page_post_create():
    if request.method == "GET":
        return render_template("post_form.html")

    picture = request.files.get("picture")
    content = request.form.get("content")
    if not picture or not content:
        return f"Ошибка загрузки!"

    if request.method == "POST":
        path = f"{UPLOAD_FOLDER}/{picture.filename}"
        post = {"pic": f"/{path}", "content": content}
        picture.save(path)
        get_post(data, post, POST_PATH)
        return render_template("post_uploaded.html", post=post)


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


if __name__ == "__main__":
    app.run(debug=True)
