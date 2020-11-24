"""
3. 네이버 푸드윈도 크롤링 - 상품리스트 전체 api 이용
"""

import json
import urllib.request as req
import pandas as pd
from bs4 import BeautifulSoup
import requests

import re
import time


def entire_lst_crawl():
    # 상품 이미지 url 리스트
    img_lst = []

    # 상품명 리스트
    nm_lst = []

    # 가격 리스트
    price_lst = []

    # 별점 리스트
    score_lst = []

    # 리뷰수 리스트
    rev_cnt_lst = []

    # 판매처 리스트
    seller_lst = []

    # 카테고리 리스트
    cat_lst = []

    # 채널id 리스트
    ch_id_lst = []

    # 상품id 리스트
    p_id_lst = []

    # 주요정보, 섭취정보 텍스트 통합
    """
    # 제품타입 리스트
    pd_type_lst = []

    # 섭취방법 리스트
    eat_meth_lst = []

    # 섭취대상 리스트
    eat_targ_lst = []

    # 섭취횟수 리스트
    eat_cnt_lst = []

    # 1일 총 섭취량
    tot_eat_cnt = []

    # 제품용량
    pd_volume_lst = []

    # 주요 기능성(식약처인증)
    main_func_lst = []

    """
    # 주요정보_lst
    main_info_lst = []

    # 섭취정보_lst
    eat_info_lst = []

    # 주요 영양성분 dict 담을 lst
    main_nut_lst = []

    # leaf_Category_lst
    leaf_id_lst = []

    # 상품 인기정보 txt_lst
    pd_pop_lst = []

    base_url = "https://shopping.naver.com"

    # url = base_url + '/v1/special-events?_nc_=1605884400000&vertical=FRESH&subVertical=HEALTHY&page=2&pageSize=1'
    # pagesize => 1000
    # page => 1 ~

    hasmore = 'True'

    # 초기값 세팅
    page = 1
    page_size = 5

    # while hasmore != False:

    # test용
    while page != 2:

        param_url = '/v1/products?_nc_=1605884400000&subVertical=HEALTHY&page={}&pageSize={}&sort=POPULARITY&filter=ALL' \
                    '&displayType=CATEGORY_HOME&includeZzim=true&includeViewCount=false&includeStoreCardInfo=false&' \
                    'includeStockQuantity=false&includeBrandInfo=false&includeBrandLogoImage=false&' \
                    'includeRepresentativeReview=false&' \
                    'includeListCardAttribute=true&includeRanking=true&includeRankingByMenus=true&' \
                    'includeStoreCategoryName=false&includeIngredient=false&menuId=10002562&standardSizeKeys[]=&' \
                    'standardColorKeys[]=&attributeValueIds[]=&attributeValueIdsAll[]=&certifications[]=&menuIds[]=&' \
                    'includeStoreInfoWithHighRatingReview=false'

        url = base_url + param_url.format(page, page_size)
        print(url)

        print("데이터를 불러오는 중입니다...")

        data = req.urlopen(url).read().decode('utf-8')

        dict = json.loads(data)

        print(dict)

        # 상품 리스트
        product_lst = dict.get('products')

        hasmore = dict.get('hasMoreProducts')

        print(hasmore)

        print(product_lst)

        # 상품 이미지, key: images => represontativeImage => true 이면 imageUrl => true
        # 상품명 : name
        # 가격 : mobileDiscountPrice , pcDiscountPrice 일치
        # 별점 : averageReviewScore
        # 리뷰수 : totalReviewCount
        # 판매처 : channel => name
        # 카테고리 : naverShoppingCategory => wholeName

        # 데이터 꺼내기
        for obj in product_lst:

            tmp_lst = []

            print("===============================================")

            # 임시 리스트로 넘기고
            tmp_lst = obj['images']
            # print(tmp_lst)

            # 다중 dict_lst
            for i in range(0, len(tmp_lst), 1):

                # print(tmp_lst[i].get('representativeImage'))
                # 값이 True 여야 대표이미지 url
                # True, False
                if tmp_lst[i].get('representativeImage'):

                    global rep_img_url

                    # print(tmp_lst[i].get('imageUrl'))
                    rep_img_url = tmp_lst[i].get('imageUrl')

                else:

                    pass

            print("상품 이미지 : ", rep_img_url)
            print("상품명 : ", obj['name'])
            print("가격 : ", obj['pcDiscountPrice'])
            print("별점 : ", obj['averageReviewScore'])
            print("리뷰수 : ", obj['totalReviewCount'])
            print("판매처 : ", obj['channel'].get('name'))
            print("카테고리 : ", obj['naverShoppingCategory'].get('wholeName'))

            # 다음동작 : 상세정보 crawl을 위한 id값
            print("채널 id : ", obj['channel'].get('_id'))
            print("상품 id : ", obj['_id'])

            # 상품 이미지 url 리스트
            img_lst.append(rep_img_url)
            # 상품명 리스트
            nm_lst.append(obj['name'])
            # 가격 리스트
            price_lst.append(obj['pcDiscountPrice'])
            # 별점 리스트
            score_lst.append(obj['averageReviewScore'])
            # 리뷰수 리스트
            rev_cnt_lst.append(obj['totalReviewCount'])
            # 판매처 리스트
            seller_lst.append(obj['channel'].get('name'))
            # 카테고리 리스트
            cat_lst.append(obj['naverShoppingCategory'].get('wholeName'))
            # 채널id 리스트
            ch_id_lst.append(obj['channel'].get('_id'))
            # 상품id 리스트
            p_id_lst.append(obj['_id'])

            # 'attributes' 예서 주요정보 및 섭취정보 넘겨줄수있음 + 주요 영양성분 가능
            # 주요정보
            # print("주요정보 :", obj['attributes'])

            tmp_lst2 = obj['attributes']

            # 정보 데이터들이 없을경우 NULL APPEND
            if len(tmp_lst2) == 0:

                """
                pd_type_lst.append('NULL')
                eat_meth_lst.append('NULL')
                eat_targ_lst.append('NULL')
                eat_cnt_lst.append('NULL')
                tot_eat_cnt.append('NULL')
                pd_volume_lst.append('NULL')
                main_func_lst.append('NULL')
                """
                main_info_lst.append('NULL')
                eat_info_lst.append('NULL')
                main_nut_lst.append('NULL')
                leaf_id_lst.append('NULL')
                # break

            else:

                main_nut = {}
                # 주요정보 통합 TEXT
                main_info_text = ''

                # 섭취정보 총합 TEXT
                eat_info_text = ''

                # 8번요소에서 주요영양성분 + 함유량 + 값 얻어낼수 있음
                for j in range(0, len(tmp_lst2), 1):

                    # print(tmp_lst2[j])
                    # 주요영양성분 담을 임시 리스트 tmp_lst3
                    tmp_lst3 = []

                    if tmp_lst2[j].get('name') == '제품타입':

                        print("제품타입 : ", tmp_lst2[j].get('values')[0].get('name'))
                        # pd_type_lst.append(tmp_lst2[j].get('values')[0].get('name'))

                        # 주요정보 텍스트에 제품타입 text 추가
                        main_info_text = main_info_text + '' + tmp_lst2[j].get('values')[0].get('name')

                    elif tmp_lst2[j].get('name') == '섭취방법':

                        print("섭취방법 : ", tmp_lst2[j].get('values')[0].get('name'))
                        # eat_meth_lst.append(tmp_lst2[j].get('values')[0].get('name'))

                        # 섭취정보 텍스트에 섭취방법 추가
                        eat_info_text = eat_info_text + '' + tmp_lst2[j].get('values')[0].get('name')

                    elif tmp_lst2[j].get('name') == '섭취대상':

                        print("섭취대상 : ", tmp_lst2[j].get('values')[0].get('name'))
                        # eat_targ_lst.append(tmp_lst2[j].get('values')[0].get('name'))

                        # 주요정보 텍스트에 섭취대상 text 추가
                        main_info_text = main_info_text + ', ' + tmp_lst2[j].get('values')[0].get('name')

                    elif tmp_lst2[j].get('name') == '섭취횟수':

                        print("섭취횟수: ", tmp_lst2[j].get('values')[0].get('name'))
                        # eat_cnt_lst.append(tmp_lst2[j].get('values')[0].get('name'))

                        # 섭취정보 텍스트에 섭취횟수 추가
                        eat_info_text = eat_info_text + ', ' + tmp_lst2[j].get('values')[0].get('name')

                    elif tmp_lst2[j].get('name') == '1일 총 섭취량':

                        print("1일 총 섭취량: ", tmp_lst2[j].get('values')[0].get('name'))
                        # tot_eat_cnt.append(tmp_lst2[j].get('values')[0].get('name'))

                        # 섭취정보 텍스트에 1일 총 섭취량 추가
                        eat_info_text = eat_info_text + ', ' + tmp_lst2[j].get('values')[0].get('name')

                    elif tmp_lst2[j].get('name') == '제품용량':

                        print("제품용량: ", tmp_lst2[j].get('values')[0].get('name'))
                        # pd_volume_lst.append(tmp_lst2[j].get('values')[0].get('name'))

                        # 주요정보 텍스트에 제품용량 text 추가
                        main_info_text = main_info_text + ', ' + tmp_lst2[j].get('values')[0].get('name')

                    elif tmp_lst2[j].get('name') == '주요 기능성(식약처인증)':

                        print("주요 기능성(식약처인증): ", tmp_lst2[j].get('values')[0].get('name'))
                        # main_func_lst.append(tmp_lst2[j].get('values')[0].get('name'))

                        # 주요정보 텍스트에 주요 기능성(식약처인증) text 추가
                        main_info_text = main_info_text + ', ' + tmp_lst2[j].get('values')[0].get('name')

                    elif tmp_lst2[j].get('name') == '식품품질인증':

                        pass

                    elif tmp_lst2[j].get('name') == '영양소 원료명(식약처고시)':

                        pass

                    else:

                        # key
                        # print(tmp_lst2[j].get('name'))
                        # value
                        # print(tmp_lst2[j].get('values')[0].get('value'))
                        # print(tmp_lst2[j].get('values')[0].get('unit'))
                        try:
                            main_nut[tmp_lst2[j].get('name')] = tmp_lst2[j].get('values')[0].get('value') + \
                                                                tmp_lst2[j].get('values')[0].get('unit')

                            main_nut_text = tmp_lst2[j].get('name') + ' 함유량 ' + tmp_lst2[j].get('values')[0].get(
                                'value') \
                                            + tmp_lst2[j].get('values')[0].get('unit')

                            # print(main_nut_text)

                            # 주요영양성분 모두 담은 dict
                            # print(main_nut)

                        except:

                            # 주요 영양성분 데이터 없을경우
                            main_nut = {}

                print("주요 영양성분 :", main_nut)
                print("주요정보 :", main_info_text)
                print("섭취정보 :", eat_info_text)

                main_nut_lst.append(main_nut)
                main_info_lst.append(main_info_text)
                eat_info_lst.append(eat_info_text)

                # 리프카테고리 아이디 필요 :  print("카테고리 코드 :", obj['naverShoppingCategory'])
                print("leafCategoryId : ", obj['naverShoppingCategory'].get('_id'))
                leaf_id_lst.append(obj['naverShoppingCategory'].get('_id'))

                # 'rankingByMenus' 내에 상품인기정보 순위 및 menuName 얻어 낼수 있음

                # print("상품인기정보 순위 : ", obj['rankingByMenus'])

                pd_pop_text = ''
                for l in range(0, len(obj['rankingByMenus']), 1):

                    # print(obj['rankingByMenus'][l])

                    if obj['rankingByMenus'][l].get('alias') == 'PRODUCT':

                        # print(obj['rankingByMenus'][l].get('menuName'), obj['rankingByMenus'][l].get('ranking'))

                        pd_pop_text = pd_pop_text + ',' + obj['rankingByMenus'][l].get('menuName') + ' ' + \
                                      str(obj['rankingByMenus'][l].get('ranking')) + '위'

                    elif obj['rankingByMenus'][l].get('alias') == 'BENEFIT':
                        # print(obj['rankingByMenus'][l].get('menuName'), obj['rankingByMenus'][l].get('ranking'))

                        pd_pop_text = pd_pop_text + ',' + obj['rankingByMenus'][l].get('menuName') + ' ' + \
                                      str(obj['rankingByMenus'][l].get('ranking')) + '위'

                    elif obj['rankingByMenus'][l].get('alias') == 'TARGET':
                        # print(obj['rankingByMenus'][l].get('menuName'), obj['rankingByMenus'][l].get('ranking'))

                        pd_pop_text = pd_pop_text + ',' + obj['rankingByMenus'][l].get('menuName') + ' ' + \
                                      str(obj['rankingByMenus'][l].get('ranking')) + '위'

                    else:

                        pass

                print("상품 인기정보 : ", pd_pop_text)

                # 맨처음 , 제외
                pd_pop_lst.append(pd_pop_text[1:-1] + "위")

                # pd_pop_lst append 안되는경우 NULL APPEND
                if len(pd_pop_lst) != len(leaf_id_lst):

                    pd_pop_lst.append('NULL')

                else:

                    pass

        page = page + 1

    """
    print(len(p_id_lst))
    print(len(ch_id_lst))
    print(len(img_lst))
    print(len(nm_lst))
    print(len(price_lst))
    print(len(score_lst))
    print(len(rev_cnt_lst))
    print(len(seller_lst))
    print(len(cat_lst))
    print(len(pd_type_lst))
    print(len(eat_meth_lst))
    print(len(eat_targ_lst))
    print(len(eat_cnt_lst))
    print(len(tot_eat_cnt))
    print(len(pd_volume_lst))
    print(len(main_func_lst))
    print(len(main_nut_lst))
    print(len(leaf_id_lst))
    """

    print(len(p_id_lst))
    print(len(ch_id_lst))
    print(len(img_lst))
    print(len(nm_lst))
    print(len(price_lst))
    print(len(score_lst))
    print(len(rev_cnt_lst))
    print(len(seller_lst))
    print(len(cat_lst))
    print(len(main_info_lst))
    print(len(eat_info_lst))
    print(len(main_nut_lst))
    print(len(leaf_id_lst))
    print(len(pd_pop_lst))

    # dict 반환
    """
    item_dict = {"상품 id": p_id_lst, "채널 id": ch_id_lst, "상품이미지": img_lst, "상품명": nm_lst, "가격": price_lst,
                 "별점": score_lst, "리뷰수": rev_cnt_lst, "판매처": seller_lst, "카테고리": cat_lst,
                 "제품타입": pd_type_lst, "섭취방법": eat_meth_lst, "섭취대상": eat_targ_lst, "섭취횟수": eat_cnt_lst,
                 "1일 총 섭취량": tot_eat_cnt, "제품용량": pd_volume_lst, "주요 기능성(식약처인증)": main_func_lst,
                 "주요 영양성분": main_nut_lst, "leafCategoryId": leaf_id_lst}
    """
    item_dict = {"상품 id": p_id_lst, "채널 id": ch_id_lst, "상품이미지": img_lst, "상품명": nm_lst, "가격": price_lst,
                 "별점": score_lst, "리뷰수": rev_cnt_lst, "판매처": seller_lst, "카테고리": cat_lst,
                 "주요정보": main_info_lst, "섭취정보": eat_info_lst,
                 "주요 영양성분": main_nut_lst, "leafCategoryId": leaf_id_lst, "상품 인기정보": pd_pop_lst}

    df = pd.DataFrame(item_dict)

    df.to_excel("3(soup)" + ".xlsx", sheet_name='sheet1')

    return item_dict
