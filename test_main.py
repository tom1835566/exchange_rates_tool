
import pytest
from unittest.mock import patch, MagicMock
from main import fetch_exchange_rates
import requests

def test_fetch_exchange_rates_success():
    """測試正常情況下的資料爬取"""
    mock_html = """
    <html>
        <table>
            <tr><th>日期</th><th>匯率</th></tr>
            <tr><td>2025/09/30</td><td>30.123</td></tr>
            <tr><td>2025/09/29</td><td>30.456</td></tr>
        </table>
    </html>
    """

    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        dates, rates = fetch_exchange_rates("http://test.url")

        assert len(dates) == 2
        assert dates[0] == "2025/09/29"  # 應該是反轉後的順序
        assert rates[0] == 30.456

def test_fetch_exchange_rates_network_error():
    """測試網路錯誤時的處理"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with pytest.raises(SystemExit) as exc_info:
            fetch_exchange_rates("http://test.url")

        assert exc_info.value.code == 1

def test_fetch_exchange_rates_empty_table():
    """測試當網頁無資料時的處理"""
    mock_html = """
    <html>
        <table>
            <tr><th>日期</th><th>匯率</th></tr>
        </table>
    </html>
    """

    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        with pytest.raises(SystemExit):
            fetch_exchange_rates("http://test.url")