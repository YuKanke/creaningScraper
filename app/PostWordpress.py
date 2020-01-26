# coding=utf-8
import json
import requests
from urllib.parse import urljoin
from datetime import datetime

# WordPressのデータ
WP_URL = 'https://con-cafe.jp/'  # 例: 'https://virtual-surfer.com/'
WP_USERNAME = 'yukke'
WP_PASSWORD = 'aoBc 4qol eNnt GRJE VhYD HfHZ'


def post_article(status, slug, title, content, category_ids, tag_ids, media_id):
   """
   記事を投稿して成功した場合はTrue、失敗した場合はFalseを返します。
   :param status: 記事の状態（公開:publish, 下書き:draft）
   :param slug: 記事識別子。URLの一部になる（ex. slug=aaa-bbb/ccc -> https://wordpress-example.com/aaa-bbb/ccc）
   :param title: 記事のタイトル
   :param content: 記事の本文
   :param category_ids: 記事に付与するカテゴリIDのリスト
   :param tag_ids: 記事に付与するタグIDのリスト
   :param media_id: 見出し画像のID
   :return: レスポンス
   """
   # credential and attributes
   user_ = WP_USERNAME
   pass_ = WP_PASSWORD
   # build request body
   payload = {"status": status,
              "slug": slug,
              "title": title,
              "content": content,
              "date": datetime.now().isoformat(),
              "categories": category_ids,
              "tags": tag_ids}
   if media_id is not None:
       payload['featured_media'] = media_id
   # send POST request
   res = requests.post(urljoin(WP_URL, "wp-json/wp/v2/posts"),
                       data=json.dumps(payload),
                       headers={'Content-type': "application/json"},
                       auth=(user_, pass_))
   print('----------\n件名:「{}」の投稿リクエスト結果:{} res.status: {}'.format(title, res, repr(res.status_code)))
   return res


# 記事を下書き投稿する（'draft'ではなく、'publish'にすれば公開投稿できます。）
post_article('publish', 'test-api-post', 'テストタイトルだよ', 'テスト本文だよ', category_ids=[], tag_ids=[], media_id=None)