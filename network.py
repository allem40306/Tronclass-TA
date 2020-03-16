# coding=utf-8
import cookielib
import json
import urllib
import urllib2


class MyWeb:
    """
        模拟一个浏览器
    """

    def __init__(self):
        self.header = {
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        }

        self.cookie = cookielib.CookieJar()
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookie_support,
                                           urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)

    def post(self, posturl, dictdata, header):
        """
        模拟post请求

        :param string posturl: url地址
        :param dict dictdata: 发送的数据
        """

        postdata = urllib.urlencode(dictdata)
        request = urllib2.Request(posturl, postdata, header)
        try:
            content = urllib2.urlopen(request)
            return content
        except Exception, e:
            print ("post:" + str(e))
            return None

    def postJson(self, posturl, dictdata, header):
        """
        模拟post请求

        :param string posturl: url地址
        :param dict dictdata: 发送的数据
        """
        request = urllib2.Request(url=posturl, headers=header, data=json.dumps(dictdata).encode())
        try:
            content = urllib2.urlopen(request)
            return content
        except Exception, e:
            print ("post:" + str(e))
            return None

    def putJson(self, posturl, dictdata, header):
        """
        模拟put请求

        :param string posturl: url地址
        :param dict dictdata: 发送的数据
        """
        request = urllib2.Request(url=posturl, headers=header, data=json.dumps(dictdata).encode())
        request.get_method = lambda: 'PUT'
        try:
            content = urllib2.urlopen(request)
            return content
        except Exception, e:
            print ("post:" + str(e))
            return None

    def get(self, url, header):
        """
        模拟get请求

        :param url: url地址
        :param header: 请求头
        :return content: 常使用read的方法来读取返回数据
        :rtype : instance or None
        """
        request = urllib2.Request(url, None, header)
        try:
            content = urllib2.urlopen(request)
            return content
        except Exception, e:
            print ("open:" + str(e))
            return None

    def get_cookie(self, key):
        for item in self.cookie:
            if key == item.name:
                return item.value
        return ''
