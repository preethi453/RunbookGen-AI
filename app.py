from flask import Flask, render_template, request, Response, redirect, url_for, session
from generator import generate_runbook
from retriever import retrieve_documents
from models import db, RunbookHistory, User

app = Flask(__name__)
app.secret_key = "runbookgen_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///runbooks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = User(
            name=request.form.get("name"),
            email=request.form.get("email"),
            username=request.form.get("username"),
            password=request.form.get("password")
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user:
            return f"Password: {user.password}"
        return render_template("forgot.html", error="User not found")

    return render_template("forgot.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    query = request.form.get("issue")

    docs = retrieve_documents(query)
    result, mode = generate_runbook(query, docs, use_llm=False)

    history = RunbookHistory(issue=query, result=result, mode=mode)
    db.session.add(history)
    db.session.commit()

    return render_template("result.html", query=query, result=result, docs=docs, mode=mode)


@app.route("/history")
def history():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    items = RunbookHistory.query.all()
    return render_template("history.html", items=items)


@app.route("/export", methods=["POST"])
def export():
    content = request.form.get("content")
    return Response(content, mimetype="text/plain",
                    headers={"Content-Disposition": "attachment;filename=runbook.txt"})


if __name__ == "__main__":
    app.run(debug=True)
