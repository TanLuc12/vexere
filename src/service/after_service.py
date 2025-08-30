import json
from datetime import datetime

class AfterServiceFlow:
    def __init__(self, booking_file=r"D:\vexere\data\mock_data.json"):
        self.booking_file = booking_file
        with open(self.booking_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def find_booking(self, booking_id: str):
        """Tìm vé theo booking_id"""
        for b in self.data["bookings"]:
            if b["id"] == booking_id:
                return b
        return None

    def save_data(self):
        """Lưu thay đổi xuống file JSON"""
        with open(self.booking_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def change_departure_time(self, booking_id: str, new_time: str) -> str:
        """Thực hiện đổi giờ khởi hành"""
        booking = self.find_booking(booking_id)
        if not booking:
            return f"Không tìm thấy vé {booking_id}"

        old_time = booking["departure_time"]
        booking["departure_time"] = new_time

        self.save_data()

        return (f" Đã đổi giờ vé {booking_id} thành công!\n"
                f"Tuyến: {booking['route']}\n"
                f"Ngày: {booking['departure_date']}\n"
                f"Giờ cũ: {old_time} → Giờ mới: {new_time}")


if __name__ == "__main__":
    service = AfterServiceFlow()

    print(service.change_departure_time("VXR2024001", "15:00"))
    print(service.change_departure_time("VXR2024002", "18:30"))
