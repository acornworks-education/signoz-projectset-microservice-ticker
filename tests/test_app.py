import pytest
from unittest import mock
from src.ticker import app
import unittest
import json

class TestProcessor(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def client(self):
        self.client = app.app.test_client()

    def test_get_ticker_list(self):
        expected_result = [
            {'ticker': 'AUDKRW=X', 'name': 'FX AUD/KRW'},
            {'ticker': 'AUDEUR=X', 'name': 'FX AUD/EUR'}
        ]

        with mock.patch('src.ticker.processor.get_tickers') as get_tickers_mock:
            get_tickers_mock.return_value = expected_result

            ticker_list_request = self.client.get('/ticker/list')

            actual_result = json.loads(ticker_list_request.data);

            self.assertEqual(len(expected_result), len(actual_result))

            for idx in range(0, len(expected_result)):
                self.assertEqual(expected_result[idx]['ticker'], actual_result[idx]['ticker'])
                self.assertEqual(expected_result[idx]['name'], actual_result[idx]['name'])


    def test_ticker_root_endpoint(self):
        call_body = {'ticker': 'AUDKRW=X', 'name': 'FX AUD/KRW'}

        with mock.patch('src.ticker.processor.add_ticker') as add_ticker_mock:
            with mock.patch('src.ticker.processor.remove_ticker') as remove_ticker_mock:
                self.client.get('/ticker', data=json.dumps(call_body))
                self.assertEqual(0, add_ticker_mock.call_count)
                self.assertEqual(0, remove_ticker_mock.call_count)

                add_ticker_mock.reset_mock()
                remove_ticker_mock.reset_mock()

                add_ticker_mock.return_value = call_body
                self.client.post('/ticker', json=call_body)
                self.assertEqual(1, add_ticker_mock.call_count)
                self.assertEqual(0, remove_ticker_mock.call_count)

                add_ticker_mock.reset_mock()
                remove_ticker_mock.reset_mock()

                remove_ticker_mock.return_value = {'ticker': 'AUDKRW=X'}
                self.client.delete('/ticker', json=call_body)
                self.assertEqual(0, add_ticker_mock.call_count)
                self.assertEqual(1, remove_ticker_mock.call_count)
