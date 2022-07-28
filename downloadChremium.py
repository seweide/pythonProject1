import pyppeteer.chromium_downloader
# pyppeteer.chromium_downloader.download_chromium()
# 这里的 mac 替换成你系统的版本，win32，win64，linux，mac 因为我是 mac 所以这里写mac
# 这个是返回在当前系统下chromium的路径
# print(pyppeteer.chromium_downloader.chromiumExecutable.get("mac"))
# 这个是返回当前系统默认的下载地址
# print(pyppeteer.chromium_downloader.downloadURLs.get("mac"))
print('默认版本是：{}'.format(pyppeteer.__chromium_revision__))
print('可执行文件默认路径：{}'.format(pyppeteer.chromium_downloader.chromiumExecutable.get('mac')))
print('mac平台下载链接为：{}'.format(pyppeteer.chromium_downloader.downloadURLs.get('mac')))