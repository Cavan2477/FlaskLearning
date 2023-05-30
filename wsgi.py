import os

from dotenv import load_dotenv

# 手动使用python-dotenv写入.env文件的环境变量。
# 并在这个脚本中加载环境变量，导入程序实例以供部署时使用
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from watchlist import app
