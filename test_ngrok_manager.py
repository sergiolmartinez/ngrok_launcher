import unittest
from unittest.mock import patch, MagicMock
import ngrok_manager


class TestNgrokManager(unittest.TestCase):

    @patch('ngrok_manager.subprocess.Popen')
    @patch('ngrok_manager.is_ngrok_installed')
    def test_start_ngrok_default(self, mock_is_installed, mock_popen):
        """Test starting Ngrok with a default dynamic URL."""
        # Mock ngrok is installed
        mock_is_installed.return_value = True
        mock_popen.return_value.pid = 12345

        # Call the function
        ngrok_manager.start_ngrok(8080)

        # Check if subprocess.Popen was called with the correct command
        mock_popen.assert_called_once_with("ngrok http 8080", shell=True)

    @patch('ngrok_manager.subprocess.Popen')
    @patch('ngrok_manager.is_ngrok_installed')
    def test_start_ngrok_custom_domain(self, mock_is_installed, mock_popen):
        """Test starting Ngrok with a custom static domain."""
        # Mock ngrok is installed
        mock_is_installed.return_value = True
        mock_popen.return_value.pid = 12345

        # Call the function with a custom domain
        ngrok_manager.start_ngrok(8080, domain="custom.ngrok.io")

        # Check if subprocess.Popen was called with the correct command
        mock_popen.assert_called_once_with(
            "ngrok http --domain=custom.ngrok.io 8080", shell=True)

    @patch('ngrok_manager.psutil.process_iter')
    def test_stop_ngrok(self, mock_process_iter):
        """Test stopping Ngrok and killing the process tree."""
        # Mock process iteration to simulate finding a process named "ngrok"
        mock_proc = MagicMock()
        mock_proc.info = {'pid': 12345, 'name': 'ngrok'}
        mock_process_iter.return_value = [mock_proc]

        # Mock process behavior
        mock_parent_proc = MagicMock()
        mock_parent_proc.children.return_value = []
        with patch('ngrok_manager.psutil.Process', return_value=mock_parent_proc):
            ngrok_manager.stop_ngrok()

        # Ensure the process and its children are terminated
        mock_parent_proc.terminate.assert_called_once()

    @patch('ngrok_manager.requests.get')
    def test_get_ngrok_info_success(self, mock_get):
        """Test fetching Ngrok tunnel info successfully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tunnels": [{
                "public_url": "http://example.ngrok.io",
                "metrics": {"http": {"count": 10}},
                "status": "online"
            }]
        }
        mock_get.return_value = mock_response

        # Call the function and check results
        info = ngrok_manager.get_ngrok_info()
        self.assertEqual(info['public_url'], "http://example.ngrok.io")
        self.assertEqual(info['requests_count'], 10)
        self.assertEqual(info['status'], "online")

    @patch('ngrok_manager.requests.get')
    def test_get_ngrok_info_no_tunnels(self, mock_get):
        """Test fetching Ngrok tunnel info with no active tunnels."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"tunnels": []}
        mock_get.return_value = mock_response

        info = ngrok_manager.get_ngrok_info()
        self.assertIsNone(info)

    @patch('ngrok_manager.requests.get')
    def test_get_ngrok_info_connection_error(self, mock_get):
        """Test fetching Ngrok tunnel info when Ngrok API is unreachable."""
        mock_get.side_effect = ngrok_manager.requests.exceptions.ConnectionError

        with self.assertRaises(RuntimeError):
            ngrok_manager.get_ngrok_info()

    @patch('ngrok_manager.requests.get')
    def test_get_ngrok_url_success(self, mock_get):
        """Test fetching Ngrok URL successfully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tunnels": [{
                "public_url": "http://example.ngrok.io"
            }]
        }
        mock_get.return_value = mock_response

        url = ngrok_manager.get_ngrok_url()
        self.assertEqual(url, "http://example.ngrok.io")

    @patch('ngrok_manager.requests.get')
    def test_get_ngrok_url_no_tunnels(self, mock_get):
        """Test fetching Ngrok URL with no active tunnels."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"tunnels": []}
        mock_get.return_value = mock_response

        url = ngrok_manager.get_ngrok_url()
        self.assertIsNone(url)

    @patch('ngrok_manager.requests.get')
    def test_get_ngrok_url_connection_error(self, mock_get):
        """Test fetching Ngrok URL when Ngrok API is unreachable."""
        mock_get.side_effect = ngrok_manager.requests.exceptions.ConnectionError

        with self.assertRaises(RuntimeError):
            ngrok_manager.get_ngrok_url()


if __name__ == '__main__':
    unittest.main()
