import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

event_path = os.environ.get("GITHUB_EVENT_PATH")
with open(event_path, "r") as f:
    event_data = json.load(f)

issue_title = event_data["issue"]["title"]
issue_body = event_data["issue"]["body"] or ""

llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀なプログラマーです。ユーザーのリクエストに基づいてPythonコードのみを出力してください。解説やMarkdownのコードブロック(```)は含めず、純粋なコードのみを返してください。"),
    ("user", "タイトル: {title}\n詳細: {body}")
])

chain = prompt | llm
res = chain.invoke({"title": issue_title, "body": issue_body}).content

# 返り値がリストの場合と文字列の場合の両方に対応
if isinstance(res, list):
    generated_code = "".join([str(item) for item in res])
else:
    generated_code = str(res)

# マークダウンのコードブロックが含まれている場合は除去
generated_code = generated_code.replace("```python", "").replace("```", "").strip()

with open("generated_output.py", "w") as f:
    f.write(generated_code)

print("AI coding completed.")