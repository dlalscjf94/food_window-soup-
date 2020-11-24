import entire_lst_crawl
import crawl_detail_info
import crawl_rev_info
import crawl_all_review


def main():

    # 3 = 전체 리스트 크롤링
    item_dict = entire_lst_crawl.entire_lst_crawl()

    # 3 - a 상품별 상세 리스트 크롤링
    # detail_dict = crawl_detail_info.crawl_detail_info(item_dict = item_dict)

    # 3 - b 리뷰정보 및 총점 크롤링
    # rev_info_dict = crawl_rev_info.crawl_rev_info(item_dict = item_dict)

    # 3 - c 모든 리뷰정보 크롤링
    tot_rev_dict = crawl_all_review.crawl_all_review(item_dict = item_dict)


if __name__ == '__main__':


    main()

