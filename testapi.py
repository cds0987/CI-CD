import os
from dotenv import load_dotenv

load_dotenv()

def test_travelbuddy_agent():
    """Test TravelBuddy Agent end-to-end"""
    from agent import graph

    prompt = "Tôi ở Hà Nội, muốn đi Đà Nẵng cuối tuần này, budget 5 triệu"
    result = graph.invoke({"messages": [("user", prompt)]})
    final_response = result["messages"][-1].content

    print(f"\n🤖 TravelBuddy: {final_response}")

    # Kiểm tra response hợp lệ
    assert final_response is not None
    assert len(final_response) > 0