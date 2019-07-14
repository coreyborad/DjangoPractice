from django.test import TestCase
from order.models import Order, Order_item
import csv
import os

# Create your tests here.


class OrderTestCase(TestCase):
    def _log(self, testcase, msg):
        print('[TestCase][' + testcase + '] ' + msg)
        return True

    def setUp(self):
        self._log('setUp', 'Start')

        Order.objects.all().delete()
        with open(os.path.join(os.path.dirname(__file__), 'testdata/order.csv'), newline='', encoding='utf8') as csvfile:
            rows = csv.DictReader(csvfile, delimiter=',')
            for row in rows:
                obj = Order.objects.create(
                    order_id=row['order_id'],
                    customer_id=row['customer_id'],
                    shipping=row['shipping'],
                    created_at=row['created_at'],
                )
                obj.save()

        Order_item.objects.all().delete()
        with open(os.path.join(os.path.dirname(__file__), 'testdata/order_item.csv'), newline='', encoding='utf8') as csvfile:
            rows = csv.DictReader(csvfile, delimiter=',')
            for row in rows:
                obj = Order_item.objects.create(
                    order_id=row['order_id'],
                    product_name=row['product_name'],
                    qty=row['qty'],
                )
                obj.save()

        self._log('setUp', 'Done')

    def test_getShippingInfo(self):
        self._log('getShippingInfo', 'Start')

        except_result = [
            {
                'type': 'freeship',
                'ratio': 0.13,
            },
            {
                'type': 'ship',
                'ratio': 0.87,
            },
        ]
        self.assertEqual(Order._getShippingInfo(), except_result)

        self._log('getShippingInfo', 'Done')

    def test_getCohortInfo(self):
        self._log('getCohortInfo', 'Start')

        except_result = {
            'date_list': ['20180117', '20180118', '20180122', '20180123', '20180124', '20180129', '20180130', '20180201', '20180202', '20180203', '20180205', '20180206', '20180207'],
            'custom_date_list': {
                '20180117': ['15'],
                '20180118': ['3', '15'],
                '20180122': ['15'],
                '20180123': ['15'],
                '20180124': ['15'],
                '20180129': ['15', '10'],
                '20180130': ['10', '16'],
                '20180201': ['16', '15', '10', '12', '8'],
                '20180202': ['10', '16'],
                '20180203': ['10'],
                '20180205': ['15', '10'],
                '20180206': ['10', '15', '12'],
                '20180207': ['10', '15']
            },
            'record': [
                {'customer_id': '15', 'created_date': '20180117'},
                {'customer_id': '3', 'created_date': '20180118'},
                {'customer_id': '3', 'created_date': '20180118'},
                {'customer_id': '3', 'created_date': '20180118'},
                {'customer_id': '15', 'created_date': '20180118'},
                {'customer_id': '15', 'created_date': '20180122'},
                {'customer_id': '15', 'created_date': '20180122'},
                {'customer_id': '15', 'created_date': '20180123'},
                {'customer_id': '15', 'created_date': '20180124'},
                {'customer_id': '15', 'created_date': '20180129'},
                {'customer_id': '10', 'created_date': '20180129'},
                {'customer_id': '10', 'created_date': '20180130'},
                {'customer_id': '10', 'created_date': '20180130'},
                {'customer_id': '10', 'created_date': '20180130'},
                {'customer_id': '10', 'created_date': '20180130'},
                {'customer_id': '10', 'created_date': '20180130'},
                {'customer_id': '10', 'created_date': '20180130'},
                {'customer_id': '16', 'created_date': '20180130'}, {'customer_id': '16',
                                                                    'created_date': '20180201'}, {'customer_id': '15', 'created_date': '20180201'},
                {'customer_id': '10', 'created_date': '20180201'}, {'customer_id': '10',
                                                                    'created_date': '20180201'}, {'customer_id': '10', 'created_date': '20180201'},
                {'customer_id': '10', 'created_date': '20180201'}, {'customer_id': '12',
                                                                    'created_date': '20180201'}, {'customer_id': '10', 'created_date': '20180201'},
                {'customer_id': '10', 'created_date': '20180201'}, {'customer_id': '8',
                                                                    'created_date': '20180201'}, {'customer_id': '8', 'created_date': '20180201'},
                {'customer_id': '10', 'created_date': '20180201'}, {'customer_id': '8',
                                                                    'created_date': '20180201'}, {'customer_id': '16', 'created_date': '20180201'},
                {'customer_id': '10', 'created_date': '20180202'}, {'customer_id': '10',
                                                                    'created_date': '20180202'}, {'customer_id': '16', 'created_date': '20180202'},
                {'customer_id': '10', 'created_date': '20180202'}, {'customer_id': '10',
                                                                    'created_date': '20180202'}, {'customer_id': '10', 'created_date': '20180202'},
                {'customer_id': '10', 'created_date': '20180202'}, {'customer_id': '10',
                                                                    'created_date': '20180202'}, {'customer_id': '10', 'created_date': '20180202'},
                {'customer_id': '10', 'created_date': '20180202'}, {'customer_id': '10',
                                                                    'created_date': '20180202'}, {'customer_id': '10', 'created_date': '20180203'},
                {'customer_id': '15', 'created_date': '20180205'}, {'customer_id': '10',
                                                                    'created_date': '20180205'}, {'customer_id': '10', 'created_date': '20180205'},
                {'customer_id': '10', 'created_date': '20180205'}, {'customer_id': '10',
                                                                    'created_date': '20180205'}, {'customer_id': '15', 'created_date': '20180205'},
                {'customer_id': '10', 'created_date': '20180205'}, {'customer_id': '10',
                                                                    'created_date': '20180205'}, {'customer_id': '10', 'created_date': '20180205'},
                {'customer_id': '10', 'created_date': '20180205'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '15', 'created_date': '20180206'},
                {'customer_id': '10', 'created_date': '20180206'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '10', 'created_date': '20180206'},
                {'customer_id': '10', 'created_date': '20180206'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '10', 'created_date': '20180206'},
                {'customer_id': '10', 'created_date': '20180206'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '10', 'created_date': '20180206'},
                {'customer_id': '10', 'created_date': '20180206'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '10', 'created_date': '20180206'},
                {'customer_id': '10', 'created_date': '20180206'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '10', 'created_date': '20180206'},
                {'customer_id': '10', 'created_date': '20180206'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '15', 'created_date': '20180206'},
                {'customer_id': '10', 'created_date': '20180206'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '10', 'created_date': '20180206'},
                {'customer_id': '10', 'created_date': '20180206'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '12', 'created_date': '20180206'},
                {'customer_id': '10', 'created_date': '20180206'}, {'customer_id': '10',
                                                                    'created_date': '20180206'}, {'customer_id': '10', 'created_date': '20180207'},
                {'customer_id': '10', 'created_date': '20180207'}, {
                    'customer_id': '15', 'created_date': '20180207'}
            ],
            'fortable': {
                '20180117': {'20180118': '100.0%', '20180122': '100.0%', '20180123': '100.0%', '20180124': '100.0%', '20180129': '100.0%', '20180130': '0.0%', '20180201': '100.0%', '20180202': '0.0%', '20180203': '0.0%', '20180205': '100.0%', '20180206': '100.0%', '20180207': '100.0%'},
                '20180118': {'20180122': '50.0%', '20180123': '50.0%', '20180124': '50.0%', '20180129': '50.0%', '20180130': '0.0%', '20180201': '50.0%', '20180202': '0.0%', '20180203': '0.0%', '20180205': '50.0%', '20180206': '50.0%', '20180207': '50.0%'},
                '20180122': {'20180123': '100.0%', '20180124': '100.0%', '20180129': '100.0%', '20180130': '0.0%', '20180201': '100.0%', '20180202': '0.0%', '20180203': '0.0%', '20180205': '100.0%', '20180206': '100.0%', '20180207': '100.0%'},
                '20180123': {'20180124': '100.0%', '20180129': '100.0%', '20180130': '0.0%', '20180201': '100.0%', '20180202': '0.0%', '20180203': '0.0%', '20180205': '100.0%', '20180206': '100.0%', '20180207': '100.0%'},
                '20180124': {'20180129': '100.0%', '20180130': '0.0%', '20180201': '100.0%', '20180202': '0.0%', '20180203': '0.0%', '20180205': '100.0%', '20180206': '100.0%', '20180207': '100.0%'},
                '20180129': {'20180130': '50.0%', '20180201': '100.0%', '20180202': '50.0%', '20180203': '50.0%', '20180205': '100.0%', '20180206': '100.0%', '20180207': '100.0%'},
                '20180130': {'20180201': '100.0%', '20180202': '100.0%', '20180203': '50.0%', '20180205': '50.0%', '20180206': '50.0%', '20180207': '50.0%'},
                '20180201': {'20180202': '40.0%', '20180203': '20.0%', '20180205': '40.0%', '20180206': '60.0%', '20180207': '40.0%'},
                '20180202': {'20180203': '50.0%', '20180205': '50.0%', '20180206': '50.0%', '20180207': '50.0%'},
                '20180203': {'20180205': '100.0%', '20180206': '100.0%', '20180207': '100.0%'},
                '20180205': {'20180206': '100.0%', '20180207': '100.0%'},
                '20180206': {'20180207': '66.67%'},
                '20180207': {}
            }
        }

        self.assertEqual(Order._getCohortInfo(), except_result)

        self._log('getCohortInfo', 'Done')

    def test_getRank(self):
        self._log('getRank', 'Start')

        except_result = [
            {'product_name': '[Aronia] 有機野櫻莓果醬(無添加糖) (225g/罐)', 'count': 36},
            {'product_name':
                '[137 degrees] 咖啡拿鐵杏仁堅果奶 (180ml/罐) {賞味期限: 2018-10-05}', 'count': 13},
            {'product_name': '[137 degrees] 無加糖杏仁堅果奶 (180ml/罐)', 'count': 13}
        ]

        self.assertEqual(Order_item._getRank(), except_result)

        self._log('getRank', 'Done')

    def tearDown(self):
        self._log('tearDown', 'Start')

        Order.objects.all().delete()
        Order_item.objects.all().delete()

        self._log('tearDown', 'Done')
