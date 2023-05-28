import os
from dotenv import load_dotenv

load_dotenv('.env')

bot_token = os.environ.get('bot_token')
admin_id = int(os.environ.get('admin_id'))
admin_username = os.environ.get('admin_username')
