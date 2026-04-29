from flask import Flask, render_template, request, Response, redirect, url_for, session

from generator import generate_runbook
from retriever import retrieve_documents
from models import db, RunbookHistory

app = Flask(__name__)
import os 
app.secret_key = "runbookgen_secret_key"

USERNAME = "admin"
PASSWORD = "admin123"

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

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/", methods=["GET"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    query = request.form.get("issue", "").strip()
    use_llm = False

    if not query:
        return render_template(
            "index.html",
            error="Please enter a system issue, for example: Apache service not starting on RHEL.",
        )

    try:
        docs = retrieve_documents(query, top_k=3, max_results=5)
        result, mode = generate_runbook(query, docs, use_llm=use_llm)

        history = RunbookHistory(issue=query, result=result, mode=mode)
        db.session.add(history)
        db.session.commit()

    except Exception as exc:
        docs = []
        mode = "Error"
        result = f"Error while generating runbook: {exc}"

    return render_template("result.html", query=query, result=result, docs=docs, mode=mode)


@app.route("/history")
def history():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    items = RunbookHistory.query.order_by(RunbookHistory.created_at.desc()).all()
    return render_template("history.html", items=items)


@app.route("/export", methods=["POST"])
def export():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    content = request.form.get("content", "")
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=runbook.txt"}
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)