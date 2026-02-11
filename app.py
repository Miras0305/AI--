from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import time

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

topics = []
posts = {}

@app.route("/")
def index():
    return render_template("index.html", topics=topics)

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    return render_template("topic.html", topic=topics[topic_id], posts=posts.get(topic_id, []))

@app.route("/create-topic", methods=["POST"])
def create_topic():
    title = request.json["title"]
    topic_id = len(topics)
    topics.append({"id": topic_id, "title": title})
    posts[topic_id] = []
    return jsonify({"id": topic_id})

@app.route("/add-post", methods=["POST"])
def add_post():
    data = request.json
    posts[data["topic_id"]].append({
        "author": data["author"],
        "text": data["text"]
    })
    return jsonify({"ok": True})

@app.route("/ai-answer", methods=["POST"])
def ai_answer():
    data = request.json
    topic_id = data["topic_id"]
    question = data["question"]
    time.sleep(2)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты опытный участник форума про гаджеты и технику. Отвечай как человек, понятно и по делу. Не говори, что ты ИИ."},
            {"role": "user", "content": question}
        ]
    )
    answer = response.choices[0].message.content
    posts[topic_id].append({
        "author": "AI Helper 🤖",
        "text": answer
    })
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)