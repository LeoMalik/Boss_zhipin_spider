from www_zhipin_com.middlewares.resource import PROXIES

import random


class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        print("this is ip:" + str(proxy))
        request.meta["proxy"] = "http://" + str(proxy)
