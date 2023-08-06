# coding:utf-8
import requests
from tools_hjh import other as tools
import os
import time
from tools_hjh.ThreadPool import ThreadPool

    
def main():
    url = 'https://data.elsbbus.com/list.php?name=d9890e5f8eb6cce4014cffc01f008656'
    head = requests.head(url)
    print(head.headers)


class HttpRequest:
    """ 用户向网站提出请求的类 """

    def connect(self, url, headers=None, data=None, proxies=None, encoding='UTF-8'):
        """ 发出get或post请求, 返回状态码 """
        self.url = url.strip()
        self.headers = headers
        self.data = data
        self.proxies = proxies
        
        try:
            if data is None:
                self.response = requests.get(url, headers=headers, proxies=self.proxies, stream=True, allow_redirects=True)
            else:
                self.response = requests.post(url, headers=headers, data=data, proxies=self.proxies, stream=True, allow_redirects=True)
            self.response.encoding = encoding
        except:
            pass
            
        return self.getStatusCode()
                
    def getSize(self):
        """ 返回请求大小，现在如果报错会返回0 """
        try:
            head = requests.head(self.url, headers=self.headers, data=self.data, proxies=self.proxies, timeout=(3.05, 9.05))
            size = int(head.headers['Content-Length'])
        except:
            size = 0
        return size
        
    def getText(self):
        """ 返回请求页面text, 异常返回空字符 """
        try:
            s = self.response.text
        except:
            s = ''
        return s
    
    def getContent(self):
        """ 返回请求页面content, 异常返回空字符 """
        try:
            s = self.response.content
        except:
            s = ''
        return s
    
    def download(self, dstfile, ifCheckSize=True):
        """ 下载请求的文件, 返回文件大小, 下载失败返回0, 不负责断网等问题需要重试相关 """
        path = dstfile.rsplit('/', 1)[0] + '/'
        tools.mkdir(path)
        
        # 判断文件是否已经存在，如果存在且大小一致，视为已下载，不重复下载
        contentSize = self.getSize()
        if contentSize > 0 and os.path.exists(dstfile):
            existsFileSize = os.path.getsize(dstfile)
            if existsFileSize == contentSize:
                return existsFileSize
        elif contentSize == 0:
            ifCheckSize = False
        
        downloadSize = 0
        try:
            with open(dstfile, 'wb') as f:
                for ch in self.response.iter_content(1024 * 64):
                    if ch:
                        downloadSize = downloadSize + f.write(ch)
        except:
            tools.rm(dstfile)
            downloadSize = 0
        finally:
            try:
                f.close()
            except:
                pass
            
        if ifCheckSize:
            if contentSize != downloadSize:
                tools.rm(dstfile)
                downloadSize = 0
                
        return downloadSize
    
    def getStatusCode(self):
        """ 返回请求状态码 """
        try:
            status_code = int(self.response.status_code)
        except:
            status_code = 0
        return status_code
    
    def close(self):
        self.response = None
        self.url = None
        self.headers = None
        self.data = None
    
    def __del__(self):
        self.close()
            
        
class httptools():

    @staticmethod
    def getText(url, headers=None, data=None, proxies=None, encoding='UTF-8'):
        req = HttpRequest()
        req.connect(url, headers, data, proxies, encoding=encoding)
        text = req.getText()
        req.close()
        return text

    @staticmethod
    def download(url, dstfile, headers=None, data=None, proxies=None, maxRetryCount=5, nowRetryCount=0, minSize=1024):
        """ 重新指定url等参数，执行下载 """
        url = url.strip()
        req = HttpRequest()
        statusCode = req.connect(url=url, headers=headers, data=data, proxies=proxies)
        if statusCode != 200 and maxRetryCount > nowRetryCount:
            nowRetryCount = nowRetryCount + 1
            req.close()
            time.sleep(0.2)
            size = httptools.download(url, dstfile, headers, data, proxies, maxRetryCount=maxRetryCount, nowRetryCount=nowRetryCount, minSize=minSize)
        elif statusCode != 200 and maxRetryCount <= nowRetryCount:
            size = 0
        elif statusCode == 200:
            size = req.download(dstfile, ifCheckSize=True)
            if size < minSize and maxRetryCount > nowRetryCount:
                nowRetryCount = nowRetryCount + 1
                req.close()
                time.sleep(0.2)
                size = httptools.download(url, dstfile, headers, data, proxies, maxRetryCount=maxRetryCount, nowRetryCount=nowRetryCount, minSize=minSize)
            elif size < minSize and maxRetryCount <= nowRetryCount:
                tools.rm(dstfile)
                size = 0
        return size
    
    @staticmethod
    def downloadM3U8(url, dstfile, headers=None, data=None, proxies=None, maxRetryCount=5, nowRetryCount=0, minSize=1024, theadnum=32, maxFailRate=0.015):
        url = httptools.getLastM3u8(url, headers, data, proxies)
        # 获取上下文
        page = httptools.getText(url, headers, data, proxies)
        # 修正路径
        dstfile = dstfile.replace('\\', '/')
        # 创建临时文件存放文件夹
        if '/' in dstfile and '.' in dstfile:
            m3u8TmpFileDir = dstfile.rsplit('.', 1)[0]
        elif '/' not in dstfile and '.' in dstfile:
            m3u8TmpFileDir = dstfile.split('.')[0]
        elif '/' not in dstfile and '.' not in dstfile:
            m3u8TmpFileDir = dstfile
        tools.mkdir(m3u8TmpFileDir)
        # 取得url的开头网址和url的不包含文件名的url
        urlSplits = url.split('/')
        urlHead = urlSplits[0] + '//' + urlSplits[2]
        urlPath = url.rsplit('/', 1)[0] + '/'
        # 对上下文最换行拆分分析
        lines = page.split('\n')
        key = None
        mode = None
        tsUrls = []
        for idx in range(len(lines)):
            # 如果是加密的ts，得到key
            if lines[idx].startswith('#EXT-X-KEY:'):
                from Crypto.Cipher import AES
                # keyMode = lines[idx].split('METHOD=')[1].split(',')[0]
                keyUrl = lines[idx].split('URI="')[1].split('"')[0]
                if not keyUrl.startswith('http'):
                    keyUrl = urlHead + keyUrl
                key = httptools.getText(keyUrl, headers, data, proxies)
                mode = AES.MODE_CBC
            # 得到tsUrl
            if lines[idx].startswith('#EXTINF:'):
                ts = lines[idx + 1]
                if not ts.startswith('http'):
                    if ts.startswith('/'):
                        ts = urlHead + ts
                    else:
                        ts = urlPath + ts
                tsUrls.append(ts)
                
        # 下载ts文件，记录下载文件路径
        tp = ThreadPool(theadnum)
        tsFilePaths = []
        for idx in range(len(tsUrls) - 1):
            tsfile = m3u8TmpFileDir + '/' + str(idx)
            tp.run(httptools.download, (tsUrls[idx], tsfile, headers, data, proxies, maxRetryCount, nowRetryCount, minSize))
            tsFilePaths.append(tsfile)
        tp.wait()
        
        # 根据成功下载文件的数量判断是否下载完整，定义一个失败率
        downloadedFileNumber = len(os.listdir(m3u8TmpFileDir))
        # print(downloadedFileNumber)
        if len(tsUrls) == 0:
            raise Exception("需要下载的ts文件数量为" + str(len(tsUrls)))
        elif downloadedFileNumber / len(tsUrls) < 1 - maxFailRate:
            raise Exception("需要下载的ts文件数量为" + str(len(tsUrls)) + "，而下载成功的ts文件数量为" + str(downloadedFileNumber))
        
        # 解密并合并文件
        size = 0
        dstfile = open(dstfile, 'wb')
        for tsFilePath in tsFilePaths:
            if os.path.exists(tsFilePath):
                tsfile = open(tsFilePath, "rb")
                tsfileRead = tsfile.read()
                if key is not None:
                    tsfileRead = httptools.aes_decrypt(tsfileRead, key, mode)
                size = size + dstfile.write(tsfileRead)
                tsfile.close()
        tools.rm(m3u8TmpFileDir)
        dstfile.close()
        return size
    
    @staticmethod
    def downloadM3u8(url, dstfile, headers=None, data=None, proxies=None, maxRetryCount=5, nowRetryCount=0, minSize=1024, theadnum=32, maxFailRate=0.015):
        httptools.downloadM3U8(url, dstfile, headers=headers, data=data, proxies=proxies, maxRetryCount=maxRetryCount, nowRetryCount=nowRetryCount, minSize=minSize, theadnum=theadnum, maxFailRate=maxFailRate)
    
    @staticmethod
    def getLastM3U8(url, headers=None, data=None, proxies=None):
        urlSplits = url.split('/')
        urlHead = urlSplits[0] + '//' + urlSplits[2]
        urlPath = url.rsplit('/', 1)[0] + '/'
        page = httptools.getText(url, headers, data, proxies=proxies)
        for line in page.split('\n'):
            if line.endswith('.m3u8'):
                url = line
                if not url.startswith('http'):
                    if url.startswith('/'):
                        url = urlHead + url
                    else:
                        url = urlPath + url
                url = httptools.getLastM3u8(url, headers=headers, data=data, proxies=proxies)
        return url
    
    @staticmethod
    def getSize(url, headers=None, data=None, proxies=None):
        req = HttpRequest()
        req.connect(url, headers, data, proxies)
        size = req.getSize()
        req.close()
        return size
    
    @staticmethod
    def getSizeM3U8(url, headers=None, data=None, proxies=None):
        tpSaveSize = ThreadPool(128)
        fileSizes = []
        page = httptools.getText(url, headers, data, proxies)
        urlSplits = url.split('/')
        urlHead = urlSplits[0] + '//' + urlSplits[2]
        urlPath = url.rsplit('/', 1)[0] + '/'
        lines = page.split('\n')
        tsUrls = []
        for idx in range(len(lines)):
            if lines[idx].startswith('#EXTINF:'):
                ts = lines[idx + 1]
                if not ts.startswith('http'):
                    if ts.startswith('/'):
                        ts = urlHead + ts
                    else:
                        ts = urlPath + ts
                tsUrls.append(ts)
    
        def saveSize(tsUrl, headers, data, proxies):
            try:
                fileSize = httptools.getSize(tsUrl, headers, data, proxies)
            except:
                fileSize = httptools.getSize(tsUrl, headers, data, proxies)
            fileSizes.append(fileSize)
        
        for tsUrl in tsUrls:
            tpSaveSize.run(saveSize, (tsUrl, headers, data, proxies))
            
        while(len(fileSizes) < len(tsUrls)):
            time.sleep(0.5)
            
        tpSaveSize.wait()
        
        return sum(fileSizes)
    
    @staticmethod
    def getTsUrls(url, headers=None, data=None, proxies=None):
        page = httptools.getText(url, headers, data, proxies)
        urlSplits = url.split('/')
        urlHead = urlSplits[0] + '//' + urlSplits[2]
        urlPath = url.rsplit('/', 1)[0] + '/'
        lines = page.split('\n')
        tsUrls = []
        for idx in range(len(lines)):
            if lines[idx].startswith('#EXTINF:'):
                ts = lines[idx + 1]
                if not ts.startswith('http'):
                    if ts.startswith('/'):
                        ts = urlHead + ts
                    else:
                        ts = urlPath + ts
                tsUrls.append(ts)
        return tsUrls
    
    @staticmethod
    def aes_decrypt(b, key, mode):
        """ 根据指定的key和mode使用AES解密字节码 """
        from Crypto.Cipher import AES
        key = key.encode('utf-8')
        aes = AES.new(key, mode)
        return aes.decrypt(b)
    
    @staticmethod
    def N_m3u8DL_CLI(url, dstfile, theadnum=32, exePath='N_m3u8DL-CLI'):
        workDir = os.path.abspath(os.path.dirname(__file__)) + '/' + dstfile.rsplit('/', 1)[0]
        dstfile = dstfile.split('/')[-1]
        cmd = exePath + ' --enableDelAfterDone --workDir ' + workDir + ' --saveName ' + dstfile + ' --maxThreads ' + str(theadnum) + ' ' + url
        os.popen(cmd)


if __name__ == '__main__':
    main()
