import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('.env')

ADMIN_LIST = []  # [os.getenv('ADMIN_LIST')]  # admin ID
TOKEN = os.getenv('TOKEN')  # TOKEN
SOCIAL_LINKS = ['https://t.me/ikar_factor', 'https://t.me/factor_books', 'https://t.me/factorbooks']
SOCIAL_TEXT_BUTTONS = ['IKAR | Factor Books', 'Factor Books', '\"Factor Books\" nashiryoti']


db = RedisDict('all')
print(db)

# 5684649553
