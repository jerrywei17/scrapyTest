import scrapy
import json


class ProxyExampleSpider(scrapy.Spider):
    name = 'proxy_example'
    allowed_domains = ['www.us-proxy.org']
    start_urls = ['http://www.us-proxy.org/']

    def parse(self, response):
        trs = response.css('#proxylisttable tr')
        for tr in trs:
            tds = tr.css('td')
            if len(tds) > 6:
                ip = tds[0].css('::text').get()
                port = tds[1].css('::text').get()
                ifScheme = tds[6].css('::text').get()
                if ifScheme == 'yes':
                    scheme = 'https'
                else:
                    scheme = 'http'
                proxy = "%s://%s:%s" % (scheme, ip, port)
                meta = {
                    'port': port,
                    'proxy': proxy,
                    'dont_retry': True,
                    'download_timeout': 3,
                    '_proxy_scheme': scheme,
                    '_proxy_ip': ip
                }
                print(meta)
                yield scrapy.Request('https://httpbin.org/ip', callback=self.proxy_check_available, meta=meta, dont_filter=True)
        pass

    def proxy_check_available(self, response):
        print(response.text)
        proxy_ip = response.meta['_proxy_ip']
        if proxy_ip == json.loads(response.text)['origin']:
            yield {
                'scheme': response.meta['_proxy_scheme'],
                'proxy': response.meta['proxy'],
                'prot': response.meta['port'],
            }
