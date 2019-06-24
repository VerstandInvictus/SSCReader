import mechanize
from bs4 import BeautifulSoup
import pprint
import json


class SSC:
    def __init__(self):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [
            ('User-agent',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
             'KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36)')
        ]
        self.currentpage = None

    def load_post(self, post):
        page = 'https://slatestarcodex.com/{0}'.format(post)
        resp = self.br.open(page)
        print "loaded {0}".format(page)
        soup = BeautifulSoup(resp.read(), 'html.parser')
        self.currentpage = soup

    def parse_comment(self, comment):
        c = comment.find(class_='commentholder')
        authorblock = c.find(class_='comment-author')
        metablock = c.find(class_='comment-meta')
        children = comment.find(class_='children')
        cdict = {
            'author': {
                "name": authorblock.find(class_='fn').string,
                "gravatar_link": authorblock.find(class_='avatar')['src']
            },
            'date': metablock.find('a').string,
            'text': str(c.find(class_='comment-body')),
            'replies': [self.parse_comment(x) for x in children.find(class_='comment')] if children else None
        }
        return cdict

    def extract_level_one_comments(self):
        level_one_comments = self.currentpage.find_all('li', class_='depth-1')
        level_one_parsed = []
        for tc in level_one_comments:
            level_one_parsed.append(self.parse_comment(tc))
        return level_one_parsed


if __name__ == "__main__":
    ssc = SSC()
    ssc.load_post('2019/03/03/open-thread-122-5/')
    pprint.pprint(ssc.extract_level_one_comments())
