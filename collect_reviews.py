__author__ = 'Patrick'

#!/usr/bin/env python
#encoding=utf8
'''
'''
import sys
import os
import pdb
from HTMLParser import HTMLParser
import urllib
import time
from datetime import datetime
import random

from lib.dbconnect import ConnectDB

proxies = {'http': 'http://104.131.209.71:4444'}

TARGET_ATTRS = set(['class', 'data-short-classes', 'data-original-classes', 'data-docid'])
CATEGORY_ATTR_SET = set([('class', 'child-submenu-link'), ('jsan', '7.child-submenu-link,8.href,0.title'), ('jsl', '$x 5;')])
CATEGORY_ATTR_KEYS = set(['class', 'jsan', 'jsl', 'title', 'href'])

INDEX_URL = 'https://play.google.com/store/apps'

SEPERATOR = '\001'
DATA_DIR = 'data'
IMG_DIR = '%s/img_dir' % DATA_DIR

class CategoryAppsHTMLParser(HTMLParser):

    def __init__(self):
        ''''''
        HTMLParser.__init__(self)

        self.apps = set([])

    def handle_starttag(self, tag, attrs):
        ''''''
        if tag != 'div':
            return
        if len(attrs) != 4:
            return

        keys = set([k for k, _v in attrs])
        if TARGET_ATTRS != set(keys):
            return
        #adds app ID to self.apps set
        self.apps.add(dict(attrs)['data-docid'])

    def getresult(self):
        ''''''
        return self.apps

class CategoryHTMLParser(HTMLParser):
    ''''''
    def __init__(self):
        ''''''
        HTMLParser.__init__(self)

        self.categories = set([])
        self.category_dic = {}

    def handle_starttag(self, tag, attrs):
        ''''''
        if tag == 'a':
            if set([k for k, _v in attrs]) != CATEGORY_ATTR_KEYS:
                return
            if set(attrs) & CATEGORY_ATTR_SET != CATEGORY_ATTR_SET:
                return
            url_dir = dict(attrs)['href']
            #get name of category
            category = os.path.split(url_dir)[1]

            #dic with category as key, URL as value
            self.category_dic[category] = 'https://play.google.com%s' % url_dir

    def getresult(self):
        ''''''
        return self.category_dic

class SingleAppHTMLParser(HTMLParser):
    ''''''

    def __init__(self):
        ''''''
        HTMLParser.__init__(self)

        self.score_tag = None
        self.bar_label = None
        self.to_get_data = False
        self.bar_number = False
        self.rate_number = None

        self.to_get_author = False
        self.to_get_rev_title = False
        self.to_get_rev_text = False
        self.to_get_rev_date = False
        self.dev_reply = False

        self.author = ''

        self.attrs = ''

        self.to_get_title = False
        self.title_attrs = ''

        self.info_dic = {}
        self.review_dic = {} #(date, rating, title, body/text)
        self.dic = [self.info_dic, self.review_dic]

        self.has_gotten_image = False


    def handle_starttag(self, tag, attrs):
        ''''''
        if tag == 'span':
            if len(attrs) != 1:
                return
            #print attrs

            if attrs[0][1] == 'bar-label':
                self.bar_label = True
                return

            if attrs[0][1] == 'star-tiny star-full':
                self.to_get_data = True
                self.attrs = 'star-tiny star-full'
                return

            if attrs[0][1] == 'bar-number':
                self.bar_number = True
                self.attrs = 'bar-number'
                return

            if attrs[0][1] == "author-name":
                if self.dev_reply == True:
                    self.dev_reply = False
                    return
                self.to_get_author = True
                return

            if attrs[0][1] == "review-title":
                self.to_get_rev_title = True
                return

            if attrs[0][1] == "review-date":
                self.to_get_rev_date = True
                return

        elif tag == 'div':
            if len(attrs) < 1:
                return

            if attrs[0][1] == 'developer-reply':
                self.dev_reply = True
                return

            if attrs[0][1] == 'document-title':
                self.to_get_title = True
                return

            # grab number of stars for review
            if attrs[0][1] == 'tiny-star star-rating-non-editable-container' and self.author != '':
                self.dic[1][self.author][1] = attrs[1][1]
                return

            if attrs[0][1] == 'review-text' or attrs[0][1] == 'review-body':
                self.to_get_rev_text = True

            if not attrs and self.title_attrs:
                # attrs empty, self.title_attrs not empty
                self.to_get_title = True
        elif tag == 'img':
            if self.has_gotten_image:
                return
            if ('class', 'cover-image') not in attrs:
                return
            attrs_dic = dict(attrs)
            if 'src' not in attrs_dic:
                return
            self.has_gotten_image = True
            self.dic[0]['img_url'] = attrs_dic['src']

    def handle_data(self, data):
        ''''''
        data = data.strip()
        if data == "":
            return
        if self.to_get_rev_date and self.author != '':
            self.dic[1][self.author][0] = data
            self.to_get_rev_date = False
            return

        if self.to_get_rev_title and self.author != '':
            self.dic[1][self.author][2] = data
            self.to_get_rev_title = False
            return

        if self.to_get_rev_text and self.author != '':
            self.dic[1][self.author][3] = data
            self.author = ''
            self.to_get_rev_text = False
            #print 'Got review'
            return

        if self.to_get_author:
            self.author = data.strip()
            self.dic[1][self.author] = ['','','','']
            self.to_get_author = False
            return

        if self.attrs == 'star-tiny star-full' and self.bar_label and self.to_get_data:
            # strip data of leading/trailing spaces
            # number of stars, 1-5
            self.score_tag = data.strip()

            self.attrs = ''
            return

        if self.attrs == 'bar-number' and self.bar_number:
            # number of ratings per number of stars
            self.rate_number = data.strip()

            # save, then reset everything
            self.dic[0][self.score_tag] = self.rate_number.replace(',', '')
            self.score_tag = None
            self.bar_label = None
            self.to_get_data = False
            self.bar_number = False
            self.rate_number = None

            return

        if self.to_get_title:
            #game name
            self.dic[0]['title'] = data.strip()
            self.to_get_title = False
            self.title_attrs = ''


    def getresult(self):
        ''''''
        return self.dic

def unique_apps():
    ''''''
    conn = ConnectDB(conn_cfg='cfg/db.cfg', db='appdb', dbtype='postgresql')

    sql = '''CREATE TABLE tmp(appid text, appname text, username text,
                date_posted text, score text, review_title text, review_content text);
                INSERT INTO tmp SELECT DISTINCT * FROM review_table;
                DROP TABLE review_table;
                ALTER TABLE tmp RENAME TO review_table;'''
    conn.cursor.execute(sql)
    conn.conn.commit()

def crawl_apps():
    ''''''
    # get apps category list
    sender = urllib.urlopen(INDEX_URL, proxies=proxies)

    #list of strings, lines of HTML code from INDEX_URL
    index_html = sender.read().split('\n')

    # parse category list
    parser = CategoryHTMLParser()
    for i, target_line in enumerate(index_html):
        target_line = target_line.strip()
        try:
            parser.feed(target_line)
        except:
            continue
    category_dic = parser.getresult()

    app_dic = {}

    conn = ConnectDB(conn_cfg='cfg/db.cfg', db='appdb', dbtype='postgresql')

    last_spot = False

    # parse each category
    for category, c_url in category_dic.iteritems():
        print category
        if category != "GAME_ADVENTURE" and not last_spot:
            continue
        last_spot = True

        sender = urllib.urlopen(c_url, proxies=proxies)

        #HTML split into lines
        category_page = sender.read().split('\n')

        apps = set([])
        category_apps_parser = CategoryAppsHTMLParser()
        for target_line in category_page:
            try:
                #remove leading or trailing spaces
                target_line = target_line.strip()
                category_apps_parser.feed(target_line)
            except:
                continue
        tmp_set = category_apps_parser.getresult()

        apps |= tmp_set

        # parse each app's rating info
        for app in apps:
            app_url = 'https://play.google.com/store/apps/details?id=%s' % app
            print app_url
            sender = urllib.urlopen(app_url, proxies=proxies)
            app_page = sender.read().split('\n')

            info_dic = {}

            single_parser = SingleAppHTMLParser()
            for target_line in app_page:
                try:
                    single_parser.feed(target_line.decode('utf8'))
                except Exception:
                    raise

            tmp_info_dic = single_parser.getresult()[0]
            tmp_review_dic = single_parser.getresult()[1]
            tmp_info_dic['last_changed_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            info_dic.update(tmp_info_dic)
            app_dic[app] = (tmp_info_dic, tmp_review_dic)

            for username in app_dic[app][1]:
                sql = '''INSERT INTO small_review(appid, appname, username, date_posted, score, review_title,
                        review_content)
                        values(%s,%s,%s,%s,%s,%s,%s);'''
                conn.cursor.execute(sql, (app, app_dic[app][0]['title'], username, app_dic[app][1][username][0],
                                app_dic[app][1][username][1], app_dic[app][1][username][2],
                                app_dic[app][1][username][3]))
                conn.conn.commit()

            time.sleep(random.randint(0, 2))
            break

    return app_dic

if __name__ == '__main__':
    crawl_apps()
    unique_apps()

# C1.prototype.o = function(c) {
#   var d = c ? c : this.a;
#   d && NU(this, d, J1(d) + 1);
#   c && (this.a = c)
# }
# s = y.handle = function(e) {
#   return st === t || e && st.event.triggered === e.type ? t : st.event.dispatch.apply(s.elem, arguments)
# }

# if (typeof ircs == 'undefined'){jQuery('body').one('onPressPlay',function(){ircs();});}else {ircs();}

#ssh -i apptracking-us-e.pem root@10.0.2.207
#psql --host 10.0.2.207 --port 5432 -U apppg -d appdb
