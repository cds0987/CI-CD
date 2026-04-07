import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

from agent import graph
prompt = 'Tôi ở Hà Nội, muốn đi Đà Nẵng cuối tuần này, budget 5 triệu'
result = graph.invoke({"messages": [("user", prompt)]})
final_response = result["messages"][-1].content
print("\n🤖 TravelBuddy: ", final_response)