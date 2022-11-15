from unittest import mock
from src.ticker import processor
import unittest

class TestProcessor(unittest.TestCase):
    @mock.patch('psycopg2.connect')
    def test_get_tickers(self, mock_connect):
        expected = [
            ('AUDKRW=X', 'FX AUD/KRW'),
            ('^KS11', 'KOSPI 200 Index')
        ]

        mock_connect().__enter__().cursor().__enter__().fetchall.return_value = expected

        return_list = processor.get_tickers()
        
        assert len(return_list) == 2
        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with('SELECT TICKER, NAME FROM TRADE.TICKER')

        assert return_list[0]['ticker'] == expected[0][0]
        assert return_list[1]['ticker'] == expected[1][0]

        assert return_list[0]['name'] == expected[0][1]
        assert return_list[1]['name'] == expected[1][1]
    
    @mock.patch('psycopg2.connect')
    def test_add_ticker(self, mock_connect):
        exception_cases = [
            {'name': 'Dummy name'},
            {'ticker': None},
            {'ticker': ''}
        ]

        for exception_case in exception_cases:
            with self.assertRaises(BaseException) as ex:
                processor.add_ticker(exception_case)
            
            self.assertEqual('KEY_TICKER_NAME_SHOULD_BE_DEFINED', ex.exception.args[0], msg='Failed for %s' % str(exception_case))
        
        success_cases = [
            {'ticker': '^GSPC', 'name': 'S&P500 Index'},
            {'ticker': '^GSPC'}
        ]

        for success_case in success_cases:
            mock_connect.reset_mock()
            
            processor.add_ticker(success_case)
            sql_queries = [
                'INSERT INTO TRADE.TICKER(TICKER, NAME) VALUES(''%(ticker)s'', ''%(name)s'') ON CONFLICT(TICKER) DO UPDATE SET TICKER=EXCLUDED.TICKER',
                'SELECT TICKER, NAME FROM TRADE.TICKER WHERE TICKER=%(ticker)s'
            ]

            self.assertEqual(2, mock_connect().__enter__().cursor().__enter__().execute.call_count)

            for idx in range(0, 2):
                self.assertEqual(sql_queries[idx], mock_connect().__enter__().cursor().__enter__().execute.mock_calls[idx].args[0])
                self.assertEqual(success_case, mock_connect().__enter__().cursor().__enter__().execute.mock_calls[idx].args[1])

    @mock.patch('psycopg2.connect')
    def test_remove_ticker(self, mock_connect):
        exception_cases = [
            {'name': 'Dummy name'},
            {'ticker': None},
            {'ticker': ''}
        ]

        for exception_case in exception_cases:
            with self.assertRaises(BaseException) as ex:
                processor.remove_ticker(exception_case)
            
            self.assertEqual('KEY_TICKER_SHOULD_BE_DEFINED', ex.exception.args[0], msg='Failed for %s' % str(exception_case))

        mock_connect.reset_mock()
        success_case = {'ticker': '^GSPC'}
        
        processor.remove_ticker(success_case)
        sql_query = 'DELETE FROM TRADE.TICKER WHERE TICKER=%(ticker)s'

        self.assertEqual(1, mock_connect().__enter__().cursor().__enter__().execute.call_count)
        self.assertEqual(sql_query, mock_connect().__enter__().cursor().__enter__().execute.mock_calls[0].args[0])
        self.assertEqual(success_case, mock_connect().__enter__().cursor().__enter__().execute.mock_calls[0].args[1])
