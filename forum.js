document.addEventListener("DOMContentLoaded", function() {
  const sendBtn = document.getElementById("sendBtn");
  const aiBtn = document.getElementById("aiBtn");

  sendBtn.addEventListener("click", async function() {
    const text = document.getElementById("msg").value.trim();
    if (!text) return alert("Введите сообщение");
    await fetch("/add-post", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ topic_id: topicId, author: "Пользователь", text: text })
    });
    location.reload();
  });

  aiBtn.addEventListener("click", async function() {
    const question = document.getElementById("msg").value.trim();
    if (!question) return alert("Введите вопрос для ИИ");
    const postsDiv = document.getElementById("posts");
    const thinking = document.createElement("div");
    thinking.className = "post ai";
    thinking.innerHTML = "<b>AI Helper 🤖</b><p>Думаю...</p>";
    postsDiv.appendChild(thinking);
    await fetch("/ai-answer", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ topic_id: topicId, question: question })
    });
    location.reload();
  });
});