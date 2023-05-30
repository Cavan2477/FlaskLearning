import unittest

from watchlist import app, db
from watchlist.commands import forge, initdb
from watchlist.models import User, Movie


class WatchlistTestCase(unittest.TestCase):
    def setUp(self):
        # 更新配置：开启测试模式，并使用内存数据库
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')

        # 创建数据库和表
        db.create_all()

        # 创建测试数据，一个用户，一个电影条目
        user = User(name='Admin', username='admin')

        user.set_password('111111')

        movie = Movie(title='Test Movie Title', year='2009')

        # 使用add_all()方法一次添加多个模型实例，传入列表
        db.session.add_all([user, movie])
        db.session.commit()

        # 务必创建测试客户端与命令运行器，否则可能无法进行单元测试 By CavanLiu
        # 创建测试客户端
        self.client = app.test_client()

        # 创建测试命令运行器
        self.runner = app.test_cli_runner()

    def tearDown(self):
        # 清除数据库对话
        db.session.remove()

        # 清除数据库表
        db.drop_all()

    # 测试程序实例是否存在 done
    def test_app_exist(self):
        self.assertIsNotNone(app)

    # done
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        response = self.client.get('/nothing')

        data = response.get_data(as_text=True)

        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)

        self.assertIn('Test\'s Watchlist', data)
        self.assertIn('Test Movie Title', data)
        self.assertEqual(response.status_code, 200)

    # 用户登录账号测试
    def login(self):
        self.client.post('/login', data=dict(username='admin', password='111111'), follow_redirects=True)

    # 创建新条目
    def test_create_item(self):
        self.login()

        # 测试创建条目操作
        response = self.client.post('/', data=dict(title='New Movie', year='2019'), follow_redirects=True)

        data = response.get_data(as_text=True)
        self.assertIn('Item Created.', data)
        self.assertIn('New Movie', data)

        # 测试创建条目操作， 但电影标题为空
        response = self.client.post('/', data=dict(title='', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid input.', data)

        response = self.client.post('/', data=dict(title='New Movie', year=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid input.', data)

    # 更新条目
    def test_update_item(self):
        self.login()

        # 测试更新页面
        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Edit item', data)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2019', data)

        # 测试更新条目操作
        response = self.client.post('/movie/edit/1', data=dict(title='New Movie Edited', year='2019'),
                                    follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item updated', data)
        self.assertIn('New Movie Edited', data)

        # 测试更新条目操作：但电影标题为空
        response = self.client.post('/movie/edit/1', data=dict(title='', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Updated.', data)
        self.assertIn('Invalid input.', data)

        # 测试更新条目操作：但电影年份为空
        response = self.client.post('/movie/edit/1', data=dict(title='New Movie Edit Again', year=''),
                                    follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Updated.', data)
        self.assertNotIn('New Movie Edit Again', data)
        self.assertIn('Invalid input.', data)

    def test_delete_item(self):
        self.login()

        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item deleted.', data)
        self.assertNotIn('Test Movie Title', data)

    def test_login_protect(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)

    def test_login(self):
        response = self.client.post('/login', dict(username='admin', password='111111'), follow_redirects=True)
        data = response.get_data(as_text=True)

        self.assertIn('Login success.', data)
        self.assertIn('Logout', data)
        self.assertIn('Settings', data)
        self.assertIn('Delete', data)
        self.assertIn('Edit', data)
        self.assertIn('<form method="post">', data)

        # 测试使用错误的密码登录
        response = self.client.post('/login', data=dict(
            username='admin',
            password='222222'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用错误的用户名登录
        response = self.client.post('/login', data=dict(
            username='wrong',
            password='111111'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用空用户名登录
        response = self.client.post('/login', data=dict(
            username='',
            password='111111'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input.', data)

        # 测试使用空密码登录
        response = self.client.post('/login', data=dict(
            username='admin',
            password=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input.', data)

    def test_logout(self):
        self.login()

        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Goodbye.', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('<form method="post">', data)

        # 测试设置

    def test_settings(self):
        self.login()

        # 测试设置页面
        response = self.client.get('/settings')
        data = response.get_data(as_text=True)
        self.assertIn('Settings', data)
        self.assertIn('Your Name', data)

        # 测试更新设置
        response = self.client.post('/settings', data=dict(
            name='Cavan',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Settings updated.', data)
        self.assertIn('Grey Li', data)

        # 测试更新设置，名称为空
        response = self.client.post('/settings', data=dict(
            name='',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Settings updated.', data)
        self.assertIn('Invalid input.', data)

    # 测试虚拟数据
    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('Done.', result.output)
        self.assertNotEqual(Movie.query.count(), 0)

    # 测试初始化数据库
    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)

    # 测试生成管理员账户
    def test_admin_command(self):
        db.drap_all()
        db.create_all()

        result = self.runner.invoke(args=['admin', '--username', 'Cavan', '--password', '111111'])

        self.assertIn('Creating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'Cavan')
        self.assertTrue(User.query.first().validate_password('111111'))

    # 测试更新管理员账户
    def test_admin_command_update(self):
        # 使用 args 参数给出完整的命令参数列表
        result = self.runner.invoke(args=['admin', '--username', 'peter', '--password', '222222'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'Peter')
        self.assertTrue(User.query.first().validate_password('222222'))


if __name__ == '__main__':
    unittest.main()
