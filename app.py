import matplotlib
import requests
from collections import Counter
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import jieba
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import numpy as np


def crawl_data(url):
    # 发送GET请求并获取响应
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    # 利用requests对象的get方法，对指定的url发起请求,该方法会返回一个Response对象
    response = requests.get(url, headers=headers)
    # response = requests.get(url)
    # response.encoding = response.apparent_encoding
    response.encoding = 'utf-8'
    # 确定编码
    # encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
    # 使用BeautifulSoup解析响应文本
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    # 查找ID为"UCAP-CONTENT"的DIV
    # div = soup.find('div', {'id': 'UCAP-CONTENT'})
    # 获取DIV中的文本内容
    content = soup.get_text()
    return content

def create_bar_chart(data, title, x_label, y_label, rotation=45, color='blue'):
    plt.figure(figsize=(10, 6))
    plt.xticks(rotation=rotation)
    plt.bar(data['Word'], data['Frequency'], color=color)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    fig = plt.gcf()
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return image

def generate_pie_chart(data, num):
    labels = data['Word']
    sizes = data['Frequency']
    colors = ['blue', 'green', 'red', 'purple', 'orange']  # 根据你的数据量调整颜色数量
    fig, ax = plt.subplots()
    ax.axis('equal')
    plt.title('扇形图')
    dev_position = [0.1] * num
    plt.pie(sizes,
            labels=labels,
            wedgeprops={'width': 0.7},
            colors=colors,
            autopct='%1.1f%%',
            shadow=True,
            startangle=50,
            explode=dev_position,
            labeldistance=1,
            radius=1.5,
            pctdistance=0.8)
    plt.axis('equal')
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return image

def generate_scatter_plot(data):
    plt.scatter(data['Word'], data['Frequency'], color='#567834')
    plt.xticks(rotation=45)  # 将标签旋转45度
    plt.title('散点图')
    plt.xlabel('x')
    plt.ylabel('y')
    fig = plt.gcf()  # 获取当前图形对象
    fig.canvas.draw()  # 绘制图形
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return image

def generate_line_plot(data):
    plt.plot(data['Word'], data['Frequency'], color='red')
    plt.xticks(rotation=45)  # 将标签旋转45度
    plt.title('折线图')
    plt.xlabel('x')
    plt.ylabel('y')
    fig = plt.gcf()  # 获取当前图形对象
    fig.canvas.draw()  # 绘制图形
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return image

def generate_histogram(data):
    plt.hist(data, bins=max(data), color='red', alpha=0.5)
    plt.title('直方图')
    plt.xlabel('频率值')
    plt.ylabel('该频率数据数')
    fig = plt.gcf()  # 获取当前图形对象
    return fig

def generate_area_chart(data):
    plt.fill_between(data['Word'], data['Frequency'], color='#345678')
    plt.xticks(rotation=45)
    plt.title('面积图')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    fig = plt.gcf()
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return fig, image
def main():
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    # 设置中文字体
    st.set_option('deprecation.showPyplotGlobalUse', False)  # 防止警告信息
    font_path = 'SimHei.ttf'  # 替换为系统支持的中文字体文件路径
    # 使用 Streamlit 构建界面
    st.title('中文文本分词与词频统计:sunglasses:')
    # 输入要爬取的网页 URL
    url = st.text_input('请输入要爬取的网页 URL')
    # 执行爬虫逻辑并获取数据
    if url != '':
        data = crawl_data(url)
        data_utf8 = data.encode('utf-8')  # 如果data已经是字符串，这一步不是必需的
        # 对内容进行分词
        words =  jieba.lcut_for_search(data_utf8)
        # st.text(words)
        # 计算词语频率
        word_counts = Counter(words)
        # 找出出现次数最多的词语
        most_common_words = word_counts.most_common()
        # 构建数据框
        df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])
        #删除长度为一的值一个重复量为一的值

        df = df[~(df['Word'].str.len() == 1)]
        # 手动重新排序行号
        df = df.reset_index(drop=True)
        # 将结果展示在 Streamlit 应用中
        num = st.select_slider('请选择你要查询的数据量：', options=[5, 10 , 15, 20, 25, 30])
        st.write("出现次数最多的词语：")
        top_20_data = df.head(num)
        st.dataframe(top_20_data)

        #词云
        text = ' '.join(top_20_data['Word'])
        wordcloud = WordCloud(width=800,
                  height=400,
                  background_color='white',
                  font_path=font_path,  # 设置中文字体
                  colormap='viridis',  # 设置颜色映射
                  contour_width=1,
                  contour_color='steelblue',  # 设置轮廓颜色
                  max_words=100,  # 最大显示词数
                  max_font_size=80,  # 最大字体大小
                  random_state=42  # 随机状态，以确保每次生成相同的词云
                  ).generate(text)
        # 显示词云
        # 将词云图像转换为Pillow图像
        wordcloud_image = Image.fromarray(wordcloud.to_array())
        # 使用streamlit显示图像
        st.image(wordcloud_image)

        # 创建侧边栏
        st.sidebar.title('选择图像')
        # 创建复选框，包含7种图形的选项
        graph_options = ['直方图', '扇形图', '折线图', '散点图', '条形图', '面积图']
        selected_graphs = st.sidebar.selectbox('选择图像', graph_options)
        plt.figure(figsize=(10, 6))
        # 绘制条形图
        if '条形图' in selected_graphs:
            chart_image = create_bar_chart(top_20_data, '条形图', 'Word', 'Frequency')
            st.sidebar.image(chart_image, caption='条形图')

        # 扇形图
        if '扇形图' in selected_graphs:
            pie_chart_image = generate_pie_chart(top_20_data, num=len(top_20_data))
            # 在Streamlit侧边栏显示图片
            st.sidebar.image(pie_chart_image, caption='扇形图')

        # 散点图
        if '散点图' in selected_graphs:
            scatter_plot_image = generate_scatter_plot(top_20_data)
            # 在Streamlit应用中显示图片
            st.sidebar.image(scatter_plot_image, caption='散点图')

        # 绘制折线图
        if '折线图' in selected_graphs:
            line_plot_image = generate_line_plot(top_20_data)
            # 在Streamlit侧边栏显示图片
            st.sidebar.image(line_plot_image, caption='折线图')

        #条形图
        if '直方图' in selected_graphs:
            histogram_fig = generate_histogram(top_20_data['Frequency'])
            # 在Streamlit侧边栏显示直方图
            st.sidebar.pyplot(histogram_fig)

        #面积图
        if '面积图' in selected_graphs:
            area_fig, area_image = generate_area_chart(top_20_data)
            # 在Streamlit应用的侧边栏中显示面积图
            st.sidebar.image(area_image, caption='面积图')

    else:
        error = '请输入正确的url'
        st.text(error)

if __name__ == "__main__":
    main()
