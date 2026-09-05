import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

event_path = os.environ.get("GITHUB_EVENT_PATH")
with open(event_path, "r") as f:
    event_data = json.load(f)

issue_title = event_data["issue"]["title"]
issue_body = event_data["issue"]["body"] or ""

# エラーメッセージの指定通り gemini-3.6-flash に変更
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀なプログラマーです。ユーザーのリクエストに基づいてPythonコードのみを出力してください。解説やMarkdownのコードブロック(```)は含めず、純粋なコードのみを返してください。"),
    ("user", "タイトル: {title}\n詳細: {body}")
])

chain = prompt | llm
generated_code = chain.invoke({"title": issue_title, "body": issue_body}).content

with open("generated_output.py", "w") as f:
    f.write(generated_code)

print("AI coding completed.")