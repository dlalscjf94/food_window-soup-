"""
3-b 상품 리뷰정보, 총점 크롤링
"""

import json
import urllib.request as req
import pandas as pd
from bs4 import BeautifulSoup
import requests

import re
import time


# 상품 리뷰정보 3-b
def crawl_rev_info(item_dict):

    # https: // shopping.naver.com / v1 / reviews / evaluations - result?_nc_ = 1605884400000 &
    # originProductNo = 4722629709 & leafCategoryId = 50002441 & merchantNo = 500117304

    df = pd.DataFrame(item_dict)

    ch_id_lst = df['채널 id'].tolist()
    p_id_lst = df['상품 id'].tolist()
    # 다른 구매자들의 평가를 불러오기 위한
    leaf_id_lst = df['leafCategoryId'].tolist()

    print(ch_id_lst)
    print(p_id_lst)

    # 총 평점 lst
    tot_score_lst = []

    # 전체 리뷰수 lst
    rev_cnt_lst = []

    # 다른구매자들 평가 => api 이용

    # 포장 text
    wrap_lst = []

    # 편리 text
    conv_lst = []

    # 유통기한 text
    sl_lst = []

    # url => https://shopping.naver.com/fresh/healthy/stores/(channel_id)/products/(p_id)
    base_url = 'https://shopping.naver.com/fresh/healthy/stores/{}/products/{}'

    # url 만들고 html 파싱 진행
    for i in range(0, len(ch_id_lst), 1):

        url = base_url.format(ch_id_lst[i], p_id_lst[i])

        print("==============================================")

        print(url)

        reqs = requests.get(url)
        html = reqs.text
        soup = BeautifulSoup(html, 'html.parser')
        soup2 = BeautifulSoup(reqs.content, 'html.parser')

        # print(reqs.content)

        rj = soup2.findAll("script")[1]

        # print("rj :", rj)

        rj_txt = str(rj)

        # merchantNo 및 originalProductNo 가져오기
        merchantNo = re.findall(r'"payReferenceKey":"(.*?)"', rj_txt)
        originalProductNo = re.findall(r'"originProductNo":"(.*?)"', rj_txt)
        print("merchantNo : ", merchantNo[0])
        print("originalProductNo : ", originalProductNo[0])

        # 임시 리스트 => 리뷰정보
        tmp_lst = []
        # _3pRsbvMQEy section_statistics
        # _3lzaSoPm-d

        try:
            rev_info = soup.find_all(attrs={'class': '_3lzaSoPm-d'})

            # 통합 text 잘라내기
            rev_info_text = rev_info[0].text
            rev_lst = rev_info_text.split('전체 리뷰수')
            tmp_lst.append(rev_lst[0].replace("사용자 총 평점총 5점 중 ", ""))
            rev_lst2 = rev_lst[1].split("평점 비율")
            tmp_lst.append(rev_lst2[0])

            # tmp_lst[0] => 사용자 총 평점, tmp_lst[1] => 전체 리뷰수
            print(tmp_lst)
            tot_score_lst.append(tmp_lst[0])
            rev_cnt_lst.append(tmp_lst[1])

        except:

            print("리뷰 수 및 평점 데이터가 없습니다.")
            tot_score_lst.append('NULL')
            rev_cnt_lst.append('NULL')


        # 다른구매자들은 이렇게 평가 => api 이용
        # /v1/reviews/evaluations-result?_nc_=1605970800000&originProductNo=2344500224&leafCategoryId=50007030&merchantNo=510102035
        # /v1/reviews/evaluations-result?_nc_=1606057200000&originProductNo=4722629709&leafCategoryId=50002441&merchantNo=500117304

        ev_url = 'https://shopping.naver.com' + '/v1/reviews/evaluations-result?originProductNo={}&leafCategoryId={}&merchantNo={}'

        print(ev_url.format(originalProductNo[0], leaf_id_lst[i], merchantNo[0]))
        eval_url = ev_url.format(originalProductNo[0], leaf_id_lst[i], merchantNo[0])
        data = req.urlopen(eval_url).read().decode('utf-8')
        dict = json.loads(data)

        # print(dict)

        eval_lst = dict.get('productReviewEvaluationVOs')

        if len(eval_lst) == 0:

            print("다름사람 구매 평가 데이터가 없습니다.")

            # 포장
            wrap_lst.append('NULL')

            # 편리
            conv_lst.append('NULL')

            # 유통기한
            sl_lst.append('NULL')


        else:

            tmp_eval_lst = []

            for j in range(0, len(eval_lst), 1):

                # print(eval_lst[j].get('reviewEvaluationValues'))

                tmp_lst2 = eval_lst[j].get('reviewEvaluationValues')

                for k in range(0, len(tmp_lst2), 1):

                    # sortOrder 3 => 가장 비율이 높은 평가만 골라내기, 포장, 편리, 유통기한 순
                    if tmp_lst2[k].get('sortOrder') == 3:

                        print("================================================")
                        print(tmp_lst2[k].get('reviewEvaluationValueName'))
                        print(str(tmp_lst2[k].get('percent')) + '%')
                        print(str(tmp_lst2[k].get('count')) + '명')

                        tmp_text = tmp_lst2[k].get('reviewEvaluationValueName') + ': ' \
                                   + str(tmp_lst2[k].get('percent')) + '%' \
                                   + '(' + str(tmp_lst2[k].get('count')) + '명)'

                        tmp_eval_lst.append(tmp_text)

                    else:

                        pass

            # 포장
            wrap_lst.append(tmp_eval_lst[0])

            # 편리
            conv_lst.append(tmp_eval_lst[1])

            # 유통기한
            sl_lst.append(tmp_eval_lst[2])

        print("=================================================")
        print("사용자 총 평점 : ", tot_score_lst[i])
        print("전체 리뷰 수 : ", rev_cnt_lst[i])
        print("포장 : ", wrap_lst[i])
        print("편리 : ", conv_lst[i])
        print("유통기한 : ", sl_lst[i])

    ch_id_lst = df['채널 id'].tolist()
    p_id_lst = df['상품 id'].tolist()

    rev_info_dict = {"채널 id": ch_id_lst, "상품 id": p_id_lst, "사용자 총 평점": tot_score_lst, "전체 리뷰수": rev_cnt_lst,
                     "포장": wrap_lst, "편리": conv_lst, "유통기한": sl_lst}

    df = pd.DataFrame(rev_info_dict)

    df.to_excel("3_b(soup)" + ".xlsx", sheet_name = 'sheet1')

    return rev_info_dict
