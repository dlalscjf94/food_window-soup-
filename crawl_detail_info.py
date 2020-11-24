"""
3_a 상품 상세정보 크롤링
"""
import json
import urllib.request as req
import pandas as pd
from bs4 import BeautifulSoup
import requests

import re
import time


# 상품 상세정보 크롤링 3-a
def crawl_detail_info(item_dict):

    # 성분정보
    a_lst = []
    b_lst = []
    c_lst = []
    d_lst = []
    e_lst = []
    f_lst = []
    g_lst = []
    h_lst = []
    i_lst = []
    j_lst = []
    k_lst = []

    df = pd.DataFrame(item_dict)

    # 채널 아이디 및 상품 id 이용
    ch_id_lst = df['채널 id'].tolist()
    p_id_lst = df['상품 id'].tolist()

    # 주요정보 리스트
    main_info_lst = df['주요정보'].tolist()

    # 섭취정보 리스트
    eat_info_lst = df['섭취정보'].tolist()

    # 주요 영양성분
    main_nut_lst = df['주요 영양성분'].tolist()

    # 상품 인기정보 1
    pd_pop_info1 = df['상품 인기정보'].tolist()

    # 강세 txt
    pd_pop_1 = []

    # 6개월 내 구매수량
    pd_pop_2 = []

    # 재 구매자
    pd_pop_3 = []

    print(ch_id_lst)
    print(p_id_lst)

    # url => https://shopping.naver.com/fresh/healthy/stores/(channel_id)/products/(p_id)
    base_url = 'https://shopping.naver.com/fresh/healthy/stores/{}/products/{}'

    # url 만들고 html 파싱 진행
    for i in range(0, len(ch_id_lst), 1):

        url = base_url.format(ch_id_lst[i], p_id_lst[i])

        print(url)

        print("==============================================================================")

        reqs = requests.get(url)

        html = reqs.text

        soup = BeautifulSoup(html, 'html.parser')

        # print(html)
        """
        tbody = (soup.select('#content > div._2XqUxGzKDE > div._1TqaScMR_E > div:nth-child(6) > table '
                                          '> tbody > tr:nth-child(1) > td > table > tbody > tr'))

        for i in range(0, len(tbody), 1):

            print(tbody[i].text)
        """

        # tr 태그
        tbody = soup.find_all(['tr'])

        tmp_lst1 = []

        for j in range(0, len(tbody), 1):

            # print(tbody[i].text)

            tmp_lst1.append(tbody[j].text)

        # tmp_lst2 => 정제된 리스트
        tmp_lst2 = []
        # 'tr' 태그만 봅아온 리스트 내에서 데이터 뽑아내기
        for k in range(0, len(tmp_lst1), 1):

            if tmp_lst1[k][0:6] == '식품의 유형':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("식품의 유형", ""))

            elif tmp_lst1[k][0:4] == '제조업소':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("제조업소", ""))

            elif tmp_lst1[k][0:3] == '소재지':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("소재지", ""))

            elif tmp_lst1[k][0:5] == '제조연월일':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("제조연월일", ""))

            elif tmp_lst1[k][0:14] == '유통기한 또는 품질유지기한':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("유통기한 또는 품질유지기한", ""))

            elif tmp_lst1[k][0:12] == '포장단위별 용량(중량)':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("포장단위별 용량(중량)", ""))

            elif tmp_lst1[k][0:8] == '포장단위별 수량':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("포장단위별 수량", ""))

            elif tmp_lst1[k][0:9] == '원재료명 및 함량':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("원재료명 및 함량", ""))

            elif tmp_lst1[k][0:4] == '영양정보':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("영양정보", ""))

            elif tmp_lst1[k][0:4] == '기능정보':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("기능정보", ""))

            elif tmp_lst1[k][0:32] == '섭취량, 섭취방법, 섭취시 주의사항 및 부작용 발생 가능성':

                # print(tmp_lst1[k])
                tmp_lst2.append(tmp_lst1[k].replace("섭취량, 섭취방법, 섭취시 주의사항 및 부작용 발생 가능성", ""))

            else:

                pass

        # 표가 존재했다면
        if len(tmp_lst2) == 11:

            a_lst.append(tmp_lst2[0])
            b_lst.append(tmp_lst2[1])
            c_lst.append(tmp_lst2[2])
            d_lst.append(tmp_lst2[3])
            e_lst.append(tmp_lst2[4])
            f_lst.append(tmp_lst2[5])
            g_lst.append(tmp_lst2[6])
            h_lst.append(tmp_lst2[7])
            i_lst.append(tmp_lst2[8])
            j_lst.append(tmp_lst2[9])
            k_lst.append(tmp_lst2[10])

        else:

            # 성분정보
            a_lst.append('NULL')
            b_lst.append('NULL')
            c_lst.append('NULL')
            d_lst.append('NULL')
            e_lst.append('NULL')
            f_lst.append('NULL')
            g_lst.append('NULL')
            h_lst.append('NULL')
            i_lst.append('NULL')
            j_lst.append('NULL')
            k_lst.append('NULL')

        print("==============================================================================")

        # 주요정보
        """
        # _1IkrxTsbbm, dqPodmtbRV,. _3ubd1lJ-_1
        ing_data = soup.select(".shopping .dqPodmtbRV")
        print(ing_data)

        # (ad_soup.find("ul",{"class":"Menu"}).find_all("li")[2].find("span", {"class": "value"}))

        for l in range(0, len(ing_data), 1):

            print(ing_data[l].text)
        """
        # 상품 인기정보
        """
            bb_axis = driver.find_element_by_class_name('bb-axis')

            bax0 = bb_axis.find_element_by_class_name('bb-axis-0')

            print("상품 인기정보 1 : ", bax0.text)

            bax1 = bb_axis.find_element_by_class_name('bb-axis-1')

            print("상품 인기정보 2 : ", bax1.text)

            bax2 = bb_axis.find_element_by_class_name('bb-axis-2')

            print("상품 인기정보 3 : ", bax2.text)

        """
        # 상품인기정보 임시 lst
        tmp_lst3 = []

        try:
            # 상품 인기정보 class : _3yGgD82GwU, jymtp5wb7-
            hot_info = soup.find_all(attrs={'class':'jymtp5wb7-'})

            # 1건
            h_info_text = hot_info[0].text

            h_info_lst = h_info_text.split(".")

            tmp_lst3.append(h_info_lst[0] + '.')

            h_info_lst2 = h_info_lst[1].split("6개월 내 구매수량")

            tmp_lst3.append(h_info_lst2[0])

            tmp_lst3.append(h_info_lst2[1].replace("재 구매자", ""))

            print("==============================================================================")
            # print(tmp_lst2)
            # 강세 txt, 6개월 내 구매수량, 재구매자 수
            # print(tmp_lst3)

            pd_pop_1.append(tmp_lst3[0])
            pd_pop_2.append(tmp_lst3[1])
            pd_pop_3.append(tmp_lst3[2])

        except:

            print("상품인기정보가 없습니다.")
            pd_pop_1.append('NULL')
            pd_pop_2.append('NULL')
            pd_pop_3.append('NULL')

        print("식품의 유형 :", a_lst[i])
        print("제조업소 :", b_lst[i])
        print("소재지 :", c_lst[i])
        print("제조연월일 :", d_lst[i])
        print("유통기한 :", e_lst[i])
        print("포장단위별 용량 :", f_lst[i])
        print("포장단위별 수량 :", g_lst[i])
        print("원재료명 및 함량 :", h_lst[i])
        print("영양정보 :", i_lst[i])
        print("기능정보 :", j_lst[i])
        print("섭취량, 섭취방법, 섭취시 주의사항 :", k_lst[i])
        print("주요정보 : ", main_info_lst[i])
        print("섭취정보 : ", eat_info_lst[i])
        print("주요 영양성분 : ", main_nut_lst[i])
        print("상품 인기정보 : ", pd_pop_info1[i])
        print("강세 text : ", pd_pop_1[i])
        print("6개월 내 구매수량 : ", pd_pop_2[i])
        print("재 구매자 : ", pd_pop_3[i])

        print("===============================================================================")

    detail_dict = {"채널 id": ch_id_lst, "상품 id": p_id_lst,
                   "식품의 유형": a_lst, "제조업소": b_lst, "소재지": c_lst, "제조연월일": d_lst, "유통기한": e_lst,
                   "포장단위별 용량": f_lst, "포장단위별 수량": g_lst, "원재료명 및 함량": h_lst, "영양정보": i_lst,
                   "기능정보": j_lst, "섭취량, 섭취방법, 섭취시 주의사항": k_lst, "주요정보": main_info_lst,
                   "섭취정보": eat_info_lst, "주요 영양성분": main_nut_lst, "상품 인기정보": pd_pop_info1,
                   "강세 text": pd_pop_1, "6개월 내 구매수량": pd_pop_2, "재 구매자": pd_pop_3}

    df = pd.DataFrame(detail_dict)

    df.to_excel("3_a(soup)" + ".xlsx", sheet_name='sheet1')

    return detail_dict
