# coding=utf-8
# import cookielib
import http.cookiejar
import json
import urllib
# import urllib.request
import urllib.request
import urllib.error


class MyWeb:
    """
        模拟一个浏览器
    """

    def __init__(self):
        self.header = {
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        }

        self.cookie = http.cookiejar.CookieJar()  
        self.cookie_support = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.cookie_support,
                                           urllib.request.HTTPHandler)
        urllib.request.install_opener(self.opener)

    def post(self, posturl, dictdata, header):
        """
        模拟post请求

        :param string posturl: url地址
        :param dict dictdata: 发送的数据
        """

        postdata = urllib.urlencode(dictdata)
        request = urllib.request.Request(posturl, postdata, header)
        try:
            content = urllib.request.urlopen(request)
            return content
        except Exception as e:
            print ("post:" + str(e))
            return None

    def postJson(self, posturl, dictdata, header):
        """
        模拟post请求

        :param string posturl: url地址
        :param dict dictdata: 发送的数据
        """
        request = urllib.request.Request(url=posturl, headers=header, data=json.dumps(dictdata).encode())
        try:
            content = urllib.request.urlopen(request)
            return content
        except Exception as e:
            print ("post:" + str(e))
            return None

    def putJson(self, posturl, dictdata, header):
        """
        模拟put请求

        :param string posturl: url地址
        :param dict dictdata: 发送的数据
        """
        request = urllib.request.Request(url=posturl, headers=header, data=json.dumps(dictdata).encode())
        request.get_method = lambda: 'PUT'
        try:
            content = urllib.request.urlopen(request)
            return content
        except Exception as e:
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
        request = urllib.request.Request(url, None, header)
        try:
            content = urllib.request.urlopen(request)
            return content
        except Exception as e:
            print ("open:" + str(e))
            return None

    def get_cookie(self, key):
        for item in self.cookie:
            if key == item.name:
                return item.value
        return ''
