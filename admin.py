# admin.py
import os
from flask import Flask, render_template_string, request, redirect, send_file
from db import SessionLocal, init_db
from models import User, Lead
import io
import pandas as pd

app = Flask(__name__)
init_db()

ADMIN_ID = os.environ.get("ADMIN_ID")  # check in Render

ADMIN_HTML = """
<!doctype html>
<title>Admin panel</title>
<h2>Панель администратора</h2>
<p>Подписчики: {{count}}</p>
<form method="post" action="/broadcast">
  <textarea name="text" rows=4 cols=60 placeholder="Текст рассылки"></textarea><br/>
  <button type="submit">Отправить рассылку</button>
</form>
<form method="get" action="/export">
  <button type="submit">Export CSV (users)</button>
</form>
<h3>Запросы (Leads)</h3>
<ul>
{% for l in leads %}
  <li>{{l.created_at}} — {{l.name}} — {{l.message}} — {{l.phone}}</li>
{% endfor %}
</ul>
"""

@app.route("/")
def index():
    db = SessionLocal()
    try:
        count = db.query(User).filter_by(subscribed=True).count()
        leads = db.query(Lead).order_by(Lead.created_at.desc()).limit(50).all()
    finally:
        db.close()
    return render_template_string(ADMIN_HTML, count=count, leads=leads)

@app.route("/broadcast", methods=["POST"])
def broadcast():
    text = request.form.get("text")
    db = SessionLocal()
    try:
        users = db.query(User).filter_by(subscribed=True).all()
        # Use bot API to send messages (simple direct call)
        import telebot
        bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"))
        for u in users:
            try:
                bot.send_message(u.tg_id, text)
            except:
                pass
    finally:
        db.close()
    return redirect("/")

@app.route("/export")
def export():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        df = pd.DataFrame([{"tg_id":u.tg_id, "name":u.name, "username":u.username, "city":u.city, "subscribed":u.subscribed, "created":u.created_at} for u in users])
    finally:
        db.close()
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    mem = io.BytesIO()
    mem.write(stream.getvalue().encode("utf-8"))
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name="users.csv", mimetype="text/csv")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
