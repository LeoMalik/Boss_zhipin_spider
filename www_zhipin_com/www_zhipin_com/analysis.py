# coding=utf-8
import pandas as pd
from wordcloud import ImageColorGenerator, WordCloud  # 导入wordcloud
import jieba.analyse
import matplotlib.pyplot as plt
import re

FILE_NAME = 'analysis.txt'
RESULT_NAME = 'result.txt'

analysis_file = open(FILE_NAME, 'w', encoding='utf-8')


def fromat_data():
    print("正在处理数据")
    path = 'jobs.jobs_python.csv'
    jobs_info = pd.read_csv(path)
    # store
    detail = jobs_info['detail']
    for each in detail:
        analysis_file.write(each.strip())
    analysis_file.close()
    # analysis
    content = open(FILE_NAME, 'rb').read()
    jieba.analyse.set_stop_words('stopwords.txt')
    data = jieba.analyse.extract_tags(content, topK=100, withWeight=True)
    with open(RESULT_NAME, 'w') as fw:
        for k, v in data:
            # print(k,v)
            fw.write("%s,%f\n" % (k, v))

    # generate wordcloud
    with open(RESULT_NAME, 'r') as f:
        mytext = f.read()
        wordcloud = WordCloud(collocations=False, font_path='c:\Windows\Fonts\simhei.ttf',
                              max_font_size=100, background_color="black", random_state=50).generate(mytext)
        # wordcloud.recolor(color_func=image_colors)
        print('成功!')
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        wordcloud.to_file('all_hotwords.png')


fromat_data()
