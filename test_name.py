import pytest
from unittest.mock import patch, MagicMock
from scanner_handler import CheckQr


@pytest.fixture
def check_qr():
    return CheckQr()


@pytest.mark.parametrize(
    "qr, expected_color",
    [
        ("XXX", "Red",),
        ("XXXXX", "Green",),
        ("XXXXXXX", "Fuzzy Wuzzy",),
        ("XX", None),
    ],
)
def test_check_scanned_device_color_assignment(check_qr, qr, expected_color):
    with patch("scanner_handler.CheckQr.check_in_db", return_value=True):
        check_qr.check_scanned_device(qr)
        assert check_qr.color == expected_color


@pytest.mark.parametrize(
    "qr, db_value, expected_error",
    [
        ("XXXX", True, "Error: Wrong qr length 4"),
        ("XXXXX", None, "Not in DB"),
        ("XXXXXX", None, "Error: Wrong qr length 6"),
    ],
)
def test_check_send_error(check_qr, qr, db_value, expected_error):
    with patch("scanner_handler.CheckQr.check_in_db", return_value=db_value):
        with patch.object(
                CheckQr,
                "send_error",
                wraps=MagicMock()
        ) as mock_send_error:
            check_qr.check_scanned_device(qr)
            if expected_error:
                mock_send_error.assert_called_once_with(expected_error)
            else:
                mock_send_error.assert_not_called()


@pytest.mark.parametrize(
    "qr, db_value, expected_message",
    [
        ("XXX", True, "hallelujah XXX"),
        ("XXXXX", True, "hallelujah XXXXX"),
        ("XX", None, None),
    ],
)
def test_check_can_add_device(check_qr, qr, db_value, expected_message):
    with patch("scanner_handler.CheckQr.check_in_db", return_value=db_value):
        with patch.object(
            CheckQr, "can_add_device", wraps=MagicMock()
        ) as mock_can_add_device:
            check_qr.check_scanned_device(qr)
            if expected_message:
                mock_can_add_device.assert_called_once_with(expected_message)
            else:
                mock_can_add_device.assert_not_called()
