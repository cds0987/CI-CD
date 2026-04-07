from langchain_core.tools import tool
from data import FLIGHTS_DB, HOTELS_DB


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    # Tra cứu FLIGHTS_DB với key (origin, destination)
    flights = FLIGHTS_DB.get((origin, destination))

    # Nếu không tìm thấy → thử tra ngược (destination, origin)
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))

    # Nếu cũng không có → trả về thông báo
    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    # Format danh sách chuyến bay dễ đọc, giá có dấu chấm phân cách
    result = f"Các chuyến bay từ {origin} đến {destination}:\n"
    for i, f in enumerate(flights, 1):
        price_fmt = f"{f['price']:,}".replace(",", ".")
        result += (
            f"{i}. {f['airline']} | "
            f"{f['departure']} → {f['arrival']} | "
            f"Hạng: {f['class']} | "
            f"Giá: {price_fmt}đ\n"
        )
    return result


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    # Tra cứu HOTELS_DB[city]
    hotels = HOTELS_DB.get(city)

    if not hotels:
        return f"Không tìm thấy thông tin khách sạn tại {city}."

    # Lọc theo max_price_per_night
    affordable = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

    # Nếu không có kết quả → thông báo rõ ràng
    if not affordable:
        price_fmt = f"{max_price_per_night:,}".replace(",", ".")
        min_price = min(h["price_per_night"] for h in hotels)
        min_fmt = f"{min_price:,}".replace(",", ".")
        return (
            f"Không tìm thấy khách sạn tại {city} "
            f"với giá dưới {price_fmt}đ/đêm. "
            f"Hãy thử tăng ngân sách (giá thấp nhất: {min_fmt}đ/đêm)."
        )

    # Sắp xếp theo rating giảm dần
    affordable.sort(key=lambda h: h["rating"], reverse=True)

    # Format đẹp
    price_fmt = f"{max_price_per_night:,}".replace(",", ".")
    result = f"Khách sạn tại {city} (tối đa {price_fmt}đ/đêm), sắp xếp theo rating:\n"
    for i, h in enumerate(affordable, 1):
        p_fmt = f"{h['price_per_night']:,}".replace(",", ".")
        result += (
            f"{i}. {h['name']} | "
            f"{'⭐' * h['stars']} | "
            f"Khu vực: {h['area']} | "
            f"Rating: {h['rating']} | "
            f"Giá: {p_fmt}đ/đêm\n"
        )
    return result


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
        định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    # Parse chuỗi expenses thành dict {tên: số_tiền}
    expense_dict = {}
    try:
        for item in expenses.split(","):
            item = item.strip()
            if ":" not in item:
                continue
            name, amount = item.split(":", 1)
            expense_dict[name.strip()] = int(amount.strip())
    except Exception:
        return "Lỗi: định dạng expenses không hợp lệ. VD: 'vé_máy_bay:890000,khách_sạn:650000'"

    # Tính tổng chi phí
    total_expense = sum(expense_dict.values())

    # Tính số tiền còn lại
    remaining = total_budget - total_expense

    def fmt(n):
        return f"{n:,}".replace(",", ".")

    # Format bảng chi tiết
    result = "Bảng chi phí:\n"
    for name, amount in expense_dict.items():
        result += f"  - {name}: {fmt(amount)}đ\n"
    result += f"  ---\n"
    result += f"  Tổng chi:   {fmt(total_expense)}đ\n"
    result += f"  Ngân sách:  {fmt(total_budget)}đ\n"
    result += f"  Còn lại:    {fmt(remaining)}đ\n"

    # Nếu âm → cảnh báo
    if remaining < 0:
        result += f"\n⚠️ Vượt ngân sách {fmt(abs(remaining))}đ! Cần điều chỉnh."
    else:
        result += f"\n✅ Còn dư {fmt(remaining)}đ để chi tiêu ăn uống, tham quan."

    return result