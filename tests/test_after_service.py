import pytest
import json
import os
from src.service.after_service import AfterServiceFlow

def test_change_departure_time():
    mock_file = r"D:\vexere\data\mock_data.json"

    service = AfterServiceFlow(mock_file)
    result = service.change_departure_time("VXR2024001", "15:00")
    assert "15:00" in result
