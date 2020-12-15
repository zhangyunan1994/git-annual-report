from wordcloud import WordCloud
import jieba
import os


def generate_word_cloud(project_name, lines, temp_path):
    word_cloud_root_path = f"{temp_path}/wordcloud/"
    if not os.path.exists(word_cloud_root_path):
        os.mkdir(word_cloud_root_path)
    word_cloud_path = f'{temp_path}/wordcloud/{project_name}.png'
    if os.path.exists(word_cloud_path):
        return
    str_list = []
    for line in lines:
        if 'Merge branch' in line:
            continue
        for msg in list(jieba.cut(line)):
            str_list.append(msg)

    wc = WordCloud(font_path='SIMYOU.TTF', background_color="white", width=1000, height=860, margin=2)\
        .generate(' '.join(str_list))
    word_cloud_path = f'{temp_path}/wordcloud/{project_name}.png'
    wc.to_file(word_cloud_path)
    return word_cloud_path
