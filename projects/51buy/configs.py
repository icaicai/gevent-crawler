#coding=utf8

name = '51buy'

configs = {
    'thread': 4,   #最大并行线程数
    'headers': {   #附加的HTTP头
        'User-Agent': ''
    },
    'spiders': [{  #
            'id': 'job1',
            'name': 'Entry',  #名称，与Class定义名一样
            'start_urls': ['http://www.51buy.com/portal.html'],   #抓取入口url
            #'allow_domain': '51buy.com',  #
            'proxy': None,  #代理服务器设置
            'sched': {    #调度运行安排配置
                'type': 'cron', #定时运行模式
                'start_time': '2013-03-02 00:15:30',  #开始运行时间
                #'repeat': 2,   #运行次数
                'day': 1,       #天
                'hour': 1,      #小时
                'minute': 1,    #分钟
                'second': 1,    #秒
                #'condition': '' #条件
            }
        }, {
            'name': 'Product',  #
            'sched' : {
                'type': 'interval',   #间隔运行模式
                'days': 0,
                'seconds': 60
            }
        }
    ]
}
