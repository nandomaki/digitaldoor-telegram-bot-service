from unittest.mock import MagicMock, patch
from scripts.datasheet_services import DataSheetServices


def test_update_user_info_append():
    mock_ws = MagicMock()
    mock_ws.find.side_effect = Exception()
    mock_client = MagicMock()
    mock_client.open_by_key.return_value.sheet1 = mock_ws

    with patch('scripts.datasheet_services.gspread.authorize') as auth:
        auth.return_value = mock_client
        with patch('scripts.datasheet_services.Credentials.from_service_account_info'):
            service = DataSheetServices(client=mock_client)
            service.sheet_control = mock_ws
            service.update_user_info('123', nome='test', questao='1', id_questionario='Q1')
            mock_ws.append_row.assert_called()

