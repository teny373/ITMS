import requests

# 定义迪士尼上海的 API 地址（使用实际有效的 park ID）
url = "https://api.themeparks.wiki/v1/entity/shanghai_disneyland/live"


def fetch_wait_times():
    # 发送 GET 请求
    response = requests.get(url)

    if response.status_code == 200:
        # 解析返回的 JSON 数据
        data = response.json()
        if "liveData" in data:
            for ride in data["liveData"]:
                name = ride.get("name", "Unknown Ride")
                wait_time = ride.get("waitTime")

                # 输出每个游乐设施的名称和等待时间
                if isinstance(wait_time, int):
                    print(f"{name}: {wait_time} minutes")
        else:
            print("No live data available.")
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        print(f"Response: {response.text}")


# 调用函数打印等待时间
fetch_wait_times()
