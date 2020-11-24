"""
3_c 모든 리뷰정보 크롤링
"""

import json
import urllib.request as req
import pandas as pd
from bs4 import BeautifulSoup
import requests

import re
import time


def crawl_all_review(item_dict):

    # shopping.naver.com/v1/reviews/paged-reviews?page=1&pageSize=20&merchantNo={}&originProductNo={}&sortType=REVIEW_RANKING
    # 리뷰 : api 이용

    df = pd.DataFrame(item_dict)

    # url을 얻어내기 위한 채널 id 및 상품 id 가져오기
    ch_id_lst = df['채널 id'].tolist()
    p_id_lst = df['상품 id'].tolist()

    # url => https://shopping.naver.com/fresh/healthy/stores/(channel_id)/products/(p_id)
    base_url = 'https://shopping.naver.com/fresh/healthy/stores/{}/products/{}'

    tot_review_lst = []

    for i in range(0, len(ch_id_lst), 1):

        review_dict_lst = []

        url = base_url.format(ch_id_lst[i], p_id_lst[i])

        print("==============================================")

        print(url)

        res = requests.get(url=url)
        soup = BeautifulSoup(res.content, "html.parser")

        rj = soup.findAll("script")[1]

        # print("rj :", rj)

        rj_txt = str(rj)

        # merchantNo 및 originalProductNo 가져오기
        merchantNo = re.findall(r'"payReferenceKey":"(.*?)"', rj_txt)
        originalProductNo = re.findall(r'"originProductNo":"(.*?)"', rj_txt)
        print("merchantNo : ", merchantNo[0])
        print("originalProductNo : ", originalProductNo[0])

        page_cnt = 0
        errcode = 1

        review_dict = {}

        while errcode != 0:

            # pagesize => max=> 20
            # rev url = > shopping.naver.com/v1/reviews/paged-reviews?page=1&pageSize=20&merchantNo={}&originProductNo={}&sortType=REVIEW_RANKING
            rev_url = 'https://shopping.naver.com/v1/reviews/paged-reviews?' \
                      'page={}' \
                      '&pageSize=20' \
                      '&merchantNo={}' \
                      '&originProductNo={}' \
                      '&sortType=REVIEW_RANKING'

            page_cnt = page_cnt + 1
            rev_url = rev_url.format(page_cnt, merchantNo[0], originalProductNo[0])

            print(rev_url)
            print(page_cnt)
            # time.sleep(3)

            try:

                data = req.urlopen(rev_url).read().decode('utf-8')
                dict = json.loads(data)

                rev_lst = dict.get('contents')

                for j in range(0, len(rev_lst), 1):

                    # eview_dict["채널 id"] = ch_id_lst[i]

                    # review_dict["상품 id"] = p_id_lst[i]

                    print("===============================================================================")
                    # 별점 : reviewScore
                    print("별점 : ", rev_lst[j].get("reviewScore"))
                    review_dict["별점"] = rev_lst[j].get("reviewScore")

                    # 작성일 : createDate
                    print("작성일 : ", rev_lst[j].get("createDate"))
                    review_dict["작성일"] = rev_lst[j].get("createDate")

                    # 리뷰내용 : reviewContent
                    print("리뷰내용 : ", rev_lst[j].get("reviewContent"))
                    review_dict["리뷰내용"] = rev_lst[j].get("reviewContent")

                    # 사진 url : attachUrl
                    print("사진url : ", rev_lst[j].get("attachUrl"))
                    review_dict["사진url"] = rev_lst[j].get("attachUrl")

                review_dict_lst.append(review_dict)

            except Exception as e :

                print(e)
                errcode = 0
                print("errcode : ", errcode)

                print(review_dict_lst)

        tot_review_lst.append(review_dict_lst)

    tot_rev_dict = {"채널 id": ch_id_lst, "상품 id": p_id_lst, "모든 리뷰": tot_review_lst}

    df = pd.DataFrame(tot_rev_dict)

    df.to_excel("3_c(soup)" + ".xlsx", sheet_name= 'sheet1')

    return tot_rev_dict
