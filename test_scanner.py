import pytest
from unittest.mock import patch
from refs.scanner_handler import CheckQr

class TestQrScannerFlow:
    # valid QR lengths, device in DB
    @pytest.mark.parametrize(
        "qr_input, expected_color",
        [
            ("abc", "Red"),
            ("abcde", "Green"),
            ("abcdefg", "Fuzzy Wuzzy")
        ],
        ids=["QR_len_3", "QR_len_5", "QR_len_7"]
    )
    @patch.object(CheckQr, "check_in_db", return_value=True)
    def test_valid_qr_colors(self, mock_db, qr_input, expected_color):
        scanner = CheckQr()
        scanner.check_scanned_device(qr_input)
        assert scanner.color == expected_color, f"Expected {expected_color} for QR '{qr_input}', got {scanner.color}"

    # invalid QR lengths, no color assigned
    @pytest.mark.parametrize(
        "qr_input, expected_error",
        [
            ("a", f"Error: Wrong qr length 1"),
            ("ab", f"Error: Wrong qr length 2"),
            ("abcd", f"Error: Wrong qr length 4"),
            ("abcdef", f"Error: Wrong qr length 6"),
            ("abcdefgh", f"Error: Wrong qr length 8")
        ],
        ids=["QR_len_1", "QR_len_2", "QR_len_4", "QR_len_6", "QR_len_8"]
    )
    @patch.object(CheckQr, "check_in_db", return_value=True)
    @patch.object(CheckQr, "send_error")
    def test_invalid_qr_length(self, mock_send_error, mock_db, qr_input, expected_error):
        scanner = CheckQr()
        scanner.check_scanned_device(qr_input)
        mock_send_error.assert_called_once_with(expected_error)
        assert scanner.color is None, f"Color should be None for invalid QR '{qr_input}'"

    # valid length, device not in DB
    @pytest.mark.parametrize(
        "qr_input",
        [
            ("abc"),      # Length 3
            ("abcde"),    # Length 5
            ("abcdefg")   # Length 7
        ],
        ids=["QR_len_3_not_in_db", "QR_len_5_not_in_db", "QR_len_7_not_in_db"]
    )
    @patch.object(CheckQr, "check_in_db", return_value=None)
    @patch.object(CheckQr, "send_error")
    def test_device_not_in_db(self, mock_send_error, mock_db, qr_input):
        scanner = CheckQr()
        scanner.check_scanned_device(qr_input)
        mock_send_error.assert_called_once_with("Not in DB")

    # device added successfully
    @pytest.mark.parametrize(
        "qr_input",
        [
            ("abc"),
            ("abcde"),
            ("abcdefg")
        ],
        ids=["QR_len_3_success", "QR_len_5_success", "QR_len_7_success"]
    )
    @patch.object(CheckQr, "check_in_db", return_value=True)
    @patch.object(CheckQr, "can_add_device")
    def test_device_added_success(self, mock_can_add_device, mock_db, qr_input):
        scanner = CheckQr()
        scanner.check_scanned_device(qr_input)
        mock_can_add_device.assert_called_once_with(f"hallelujah {qr_input}")
