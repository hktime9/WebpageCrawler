# WebpageCrawler
A simple python based webpage crawler and downloader
based on the BeautifulSoup and requests libraries.
It needs two command line arguments:
1) The url you want to crawl
2) the flag: -i or -e
with the url provided in the format: 
http://www.carameltechstudios.com/
and the appropriate flag:
-i: for crawling internal links only
-e: for crawling internal and external links
The crawler crawls the url and downloads the pages
in the ./DownloadedPages
