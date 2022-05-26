class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = "http://q6jjn6yf:pelJeWrUHbFu77DJ_country-France@proxy.proxy-cheap.com:31112"
