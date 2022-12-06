from typing import Union
from fastapi import FastAPI
from datetime import datetime
from pytz import timezone
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf

# model = tf.keras.models.load_model('best_train.h5')
app = FastAPI()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

station = {}
for idx, s in enumerate(['시청', '을지로입구', '을지로3가', '을지로4가', '동대문역사문화공원', '신당', '상왕십리', '왕십리', '한양대', '뚝섬', '성수', '건대입구', '구의', '강변', '잠실나루', '잠실', '신천', '종합운동장', '삼성', '선릉', '역삼', '강남', '교대', '서초', '방배', '사당', '낙성대', '서울대입구', '봉천', '신림', '신대방', '구로디지털단지', '대림', '신도림', '문래', '영등포구청', '당산', '합정', '홍대입구', '신촌(지하)', '이대', '아현', '충정로', '잠실새내']):
    station[s] = idx
day = {
    '평일': 0,
    '토요일': 1,
    '일요일': 2
}
updown = {
    '내선': 0,
    '상선': 1,
    '외선': 2,
    '하선': 3
}

model = tf.keras.models.load_model('train.h5')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_item(loc: Union[str, None] = None):
    print(station, loc)
    s = [0]*44
    s[station[loc]] = 1

    d = [0]*3
    now = datetime.now(timezone('Asia/Seoul'))
    t = now.weekday()
    if 0 <= t <= 4:
        d[0] = 1
    elif t == 5:
        d[1] = 1
    elif t == 6:
        d[2] = 1
    s.extend(d)

    k = [0]*5
    s.extend(k)

    nowTime = now.hour*60 + now.minute

    answer = []
    for addTime in [0, 30, 60]:
        calTime = nowTime + addTime

        if 330 <= calTime <= 1410:
            s[-1] = calTime
            predict = model.predict([s])
            if predict <= 34:
                answer.append('GOOD')
            elif predict <= 66:
                answer.append('SOSO')
            else:
                answer.append('BAD')
        else:
            answer.append('CLOSE')

    return {"NOW": answer[0], 'AFTER30': answer[1], 'AFTER60': answer[2]}
