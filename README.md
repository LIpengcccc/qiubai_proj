# qiubai_proj
分布式爬虫个人案例
分布式爬虫要点：
1.改写了scrapy的调度器的,使用redis的set来去重和zset来维护请求队列
结够为list嵌套(set(指纹),list(结构化数据),zset(请求队列)）,列表里面嵌套hash
2.一句话把，set里面存了的是身份证号，zset里面存的是请求队列，队列里每个成员有唯一的身份证号,不同的机器就是向zset里面去取出队列中的请求,
并将新的请求放入队列中，且携带唯一的身份证号。

与单机爬虫的区别：
1.分布式爬虫爬完不会立即停掉,可以手动添加start_url,继续跑
2.分布式爬虫去重组件和请求队列和单机爬虫不一样


具体修改要点：
1. settings.py
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

redis连接
REDIS_URL = 'redis://@39.108.209.73:6379'

SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

指纹持久化
SCHEDULER_PERSIST = True

加入scrapy_redis自带的管道
ITEM_PIPELINES = {'scrapy_redis.pipelines.RedisPipeline': 300,}


2. spider中的修改
继承RedisSpider
类变量只有下面的两个
name = 'myspider_redis'
redis_key = 'myspider:start_urls'

把多余的类变量注释掉，比如start_url,allowed_domains之类的全都注释掉


ok，大功告成，就可以跑了


