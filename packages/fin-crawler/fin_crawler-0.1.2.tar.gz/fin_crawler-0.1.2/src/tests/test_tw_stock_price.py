import unittest

from fin_crawler.plugins.tw_stock_price import gen_params_example,gen_params,parse

class Test_tw_stock_price(unittest.TestCase):
    
    def test_gen_params_example(self):
        self.assertEqual({'date':'20220922','stock_id':'2330'},gen_params_example())

    def test_gen_params(self):

        # test normal case
        params = gen_params(**{'date':'20220922','stock_id':'2330'})
        self.assertEqual(params['fetch']['url_template'],'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=**date**&stockNo=**stock_id**&_=**time_stamp**')
        self.assertEqual(params['fetch']['url_params']['**date**'],'20220922')
        self.assertEqual(params['fetch']['url_params']['**stock_id**'],'2330')
        self.assertEqual(params['parse']['kwargs']['date'],'20220922')
        self.assertEqual(params['parse']['kwargs']['stock_id'],'2330')
        # test date with -
        params = gen_params(**{'date':'2022-09-22','stock_id':'2330'})
        self.assertEqual(params['fetch']['url_params']['**date**'],'20220922')
        self.assertEqual(params['parse']['kwargs']['date'],'20220922')
        #test invalid date
        with self.assertRaises(ValueError):
            gen_params(**{'date':'2022-09-88','stock_id':'2330'})


    def test_parse(self):
        test_data = {
            'stat':'OK',
            'data':[
                ['111/09/01',
                '42,008,490',
                '20,696,930,527',
                '495.00',
                '495.50',
                '490.00',
                '490.50',
                '-14.50',
                '93,631'],
            ],
            'fields':[
                "日期",
                "成交股數",
                "成交金額",
                "開盤價",
                "最高價",
                "最低價",
                "收盤價",
                "漲跌價差",
                "成交筆數"
            ]
        }
        result = parse(test_data,**{'date':'20220922','stock_id':'2330'})[0]
        self.assertEqual(
            result,
            {'date': '20220901',
            'volume': 42008490.0,
            'trade_amount': 20696930527.0,
            'open': 495.0,
            'high': 495.5,
            'low': 490.0,
            'close': 490.5,
            'spread_value': -14.5,
            'trade_num': 93631.0,
            'stock_id': '2330'}
        )
