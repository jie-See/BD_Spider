# 帐号列表
ACCOUNT_LIST = [
15130748268,
17832473383,
15130736634,
18803371614,
15130780904,
18803374132,
15130781424,
17832473006,
]


LIST_URL = 'http://www.bdwork.com/forum.php?mod=forumdisplay&searchtype=&needtype=2&searchindustry=&searcharea=289&searchkey=&fid=2&orderby=dateline&searchtype=&needtype=2&searchindustry=&searcharea=289&searchkey=&orderby=dateline&filter=author&page={}'


DETAIL_URL = 'http://www.bdwork.com/forum.php?mod=viewthread&tid={}&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline'

# Redis
REDIS_CONF = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 6,
    'password': '',
    'decode_responses': True,
}