import requests
from collections import Counter
import streamlit as st
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import jieba





from wordcloud import WordCloud



def crawl_data(url):
    # 发送GET请求并获取响应
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    # 利用requests对象的get方法，对指定的url发起请求,该方法会返回一个Response对象
    response = requests.get(url, headers=headers)
    # response = requests.get(url)
    response.encoding = response.apparent_encoding
    # 确定编码
    encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
    # 使用BeautifulSoup解析响应文本
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding=encoding)
    # 查找ID为"UCAP-CONTENT"的DIV
    # div = soup.find('div', {'id': 'UCAP-CONTENT'})
    # 获取DIV中的文本内容
    content = soup.get_text()
    return content
def main():
    # 使用 Streamlit 构建界面
    st.title('中文文本分词与词频统计:sunglasses:')
    # 输入要爬取的网页 URL
    url = st.text_input('请输入要爬取的网页 URL')
    # 执行爬虫逻辑并获取数据
    if url != '':
        data = crawl_data(url)
        # 对内容进行分词
        words =  jieba.lcut_for_search(data)
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
        num = st.select_slider('请选择你要查询的数据量：', options=[1, 5, 10 , 15, 20, 25, 30])
        st.write("出现次数最多的词语：")
        top_20_data = df.head(num)
        st.dataframe(top_20_data)
        # with open('content.txt', 'w', encoding='utf-8') as f:
        #     f.write(str(top_20_data))
        #词云
        text = ' '.join(top_20_data['Word'])
        wordcloud = WordCloud(width=800,
                              height=400,
                              background_color='white',
                              font_path=r'C:\Users\p\AppData\Local\Microsoft\Windows\Fonts\仿宋_GB2312.ttf').generate(text)
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

        # 绘制柱状图
        if '条形图' in selected_graphs:
            plt.figure(figsize=(10, 6))
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
            plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
            # 设置横坐标标签的角度
            plt.xticks(rotation=45)  # 将标签旋转45度
            plt.bar(top_20_data['Word'], top_20_data['Frequency'], color='blue')
            plt.title('直方图')
            plt.xlabel('Word')
            plt.ylabel('Frequency')
            # 将图形对象直接传递给 st.pyplot()
            # st.pyplot(plt.gcf())  # 'gcf' 代表 get current figure
            # 将图形放入侧边栏
            st.sidebar.pyplot(plt.gcf())

        # 扇形图
        if '扇形图' in selected_graphs:
            labels = top_20_data['Word']
            sizes = top_20_data['Frequency']
            colors = ['blue', 'green', 'red', 'purple', 'orange']  # 根据你的数据量调整颜色数量
            fig1, ax1 = plt.subplots()
            # ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title('扇形图')
            dev_position = [0.1]*num
            plt.pie(sizes,
                    labels=labels,
                    wedgeprops={'width':0.7},
                    colors=colors,
                    autopct='%1.1f%%',
                    shadow=True,
                    startangle=50,
                    explode=dev_position,
                    labeldistance=1,
                    radius=1.5,
                    pctdistance=0.8)
            plt.axis('equal')
            # st.pyplot(plt.gcf())
            st.sidebar.pyplot(plt.gcf())

        # 散点图
        if '散点图' in selected_graphs:
            plt.figure(figsize=(10, 6))
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
            plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
            plt.scatter(top_20_data['Word'], top_20_data['Frequency'], color='#567834')
            plt.xticks(rotation=45)  # 将标签旋转45度
            plt.title('散点图')
            plt.xlabel('x')
            plt.ylabel('y')
            st.sidebar.pyplot(plt.gcf())

        # 绘制折线图
        if '折线图' in selected_graphs:
            plt.figure(figsize=(10, 6))
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
            plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
            plt.plot(top_20_data['Word'], top_20_data['Frequency'], color='red')
            plt.xticks(rotation=45)  # 将标签旋转45度
            plt.title('折线图')
            plt.xlabel('x')
            plt.ylabel('y')
            st.sidebar.pyplot(plt.gcf())

        #条形图
        if '直方图' in selected_graphs:
            plt.figure(figsize=(10, 6))
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
            plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
            # 示例数据
            data = top_20_data['Frequency']
            # 绘制直方图
            plt.hist(data, bins=max(top_20_data['Frequency']), color='red', alpha=0.5)
            # 设置标题和标签
            plt.title('直方图')
            plt.xlabel('频率值')
            plt.ylabel('该频率数据数')
            # 显示直方图
            st.sidebar.pyplot(plt.gcf())


        #面积图
        if '面积图' in selected_graphs:
            plt.figure(figsize=(10, 6))
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
            plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
            plt.fill_between(top_20_data['Word'], top_20_data['Frequency'], color='#345678')
            plt.xticks(rotation=45)  # 将标签旋转45度
            plt.title('面积图')
            plt.xlabel('Word')
            plt.ylabel('Frequency')
            st.sidebar.pyplot(plt.gcf())

    else:
        error = '请输入正确的url'
        st.text(error)

if __name__ == "__main__":
    main()