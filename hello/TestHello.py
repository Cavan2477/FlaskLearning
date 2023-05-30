import unittest

from hello import say_hello


class SayHelloTestCase(unittest.TestCase):
    # 测试固件 - 测试前准备
    def setUp(self):
        pass

    # 测试固件 - 测试后清理
    def tearDown(self):
        pass

    def test_sayhello(self):
        rv = say_hello()
        # 判定返回值是否与预期相同
        self.assertEqual(rv, 'Hello!')

    def test_sayhello_to_somebody(self):
        name = 'Cavan'
        rv = say_hello(to=name)
        self.assertEqual(rv, f'Hello, {name}!')


if __name__ == '__main__':
    unittest.main()
