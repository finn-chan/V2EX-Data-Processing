from crawl import getting_topic_id
from process import cleaning_data, drawing_heatmap, drawing_treemap, drawing_radar_chart, drawing_parallel_coordinates, \
    creating_wordcloud


def main():
    start_page = 20
    end_page = 100
    print('开始爬取数据')
    getting_topic_id.get(start_page, end_page)

    print('开始处理数据')
    # 清洗数据
    cleaning_data.clean()
    # 绘制热力图
    drawing_heatmap.draw()
    # 绘制树形图
    drawing_treemap.draw()
    # 绘制雷达图
    drawing_radar_chart.draw()
    # 平行坐标图
    drawing_parallel_coordinates.draw()
    # 生成词云图
    creating_wordcloud.create()


if __name__ == '__main__':
    main()
