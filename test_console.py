from chance60 import Chance60Service
import random
from database_helper import *

# # 使用當天的日期和基數生成隨機種子，以確保每天的運氣是不同的
# random.seed(int(datetime.now().timestamp()))

# # 生成一個0到100之間的隨機數，作為運氣指數
# luck_index = random.randint(1, 65)

# 從future_telling.db取得資料,亂數取出一筆籤詩
# lots = Chance60Service()
# signPoems = lots.GetCardById(61)
# print(signPoems[1])


# save_context('demo', 'system', '你是一個聊天的好夥伴')

messages = load_context('demo')

if len(messages) == 0:
    save_context('demo', 'system', '你是一個聊天的好夥伴')

print(messages)
