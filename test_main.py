
import pytest
from unittest.mock import patch, MagicMock
from main import fetch_exchange_rates
import requests

def test_fetch_exchange_rates_success():
    # 1. 準備假的 HTML（模擬央行網站回傳的內容）
    mock_html = """
    <html>
        <table>
            <tr><th>日期</th><th>匯率</th></tr>
            <tr><td>2025/09/30</td><td>30.123</td></tr>
            <tr><td>2025/09/29</td><td>30.456</td></tr>
        </table>
    </html>
    """

    # 2. 用 patch 把真的 requests.get 換成假的
    with patch('requests.get') as mock_get:
        # 3. 建立一個假的 response 物件
        mock_response = MagicMock()
        mock_response.status_code = 200  # 模擬成功回應
        mock_response.text = mock_html   # 回傳假的 HTML
        # 4. 設定：當有人呼叫 requests.get() 時，返回這個假物件
        mock_get.return_value = mock_response

        # 5. 執行你的函式（它會用到被 mock 的 requests.get）
        dates, rates = fetch_exchange_rates("http://test.url")

        # 6. 驗證結果
        assert len(dates) == 2
        assert dates[0] == "2025/09/29"  # 檢查是否正確反轉
        assert rates[0] == 30.456

def test_fetch_exchange_rates_network_error():
    """測試網路錯誤時的處理"""
    with patch('requests.get') as mock_get:
        # side_effect: 設定當函式被呼叫時，拋出錯誤
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        # pytest.raises: 檢查是否拋出 SystemExit
        with pytest.raises(SystemExit) as exc_info:
            fetch_exchange_rates("http://test.url")

        # 驗證 exit code 是 1
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

        # 預期會執行 sys.exit(1)
        with pytest.raises(SystemExit):
            fetch_exchange_rates("http://test.url")