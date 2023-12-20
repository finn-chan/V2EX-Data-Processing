from crawl import getting_topic_id
from process import cleaning_data, drawing_heat_map


def main():
    # start_page = 20
    # end_page = 100
    # print('开始爬取数据')
    # getting_topic_id.get(start_page, end_page)

    print('开始处理数据')
    # # 清洗数据
    # cleaning_data.clean()
    # 绘制热力图
    drawing_heat_map.draw()


if __name__ == '__main__':
    main()
