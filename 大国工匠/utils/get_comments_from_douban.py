import re
from urllib import request


# 用于从豆瓣网对应页面获取相关评论信息的函数
def get_comments(target_url):
    # 模拟浏览器请求网页时，设置请求头伪装
    headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3521.2 Safari/537.36')}
    try:
        rep = request.Request(target_url, headers=headers)  # 创建Request对象时通过headers参数设置请求头
        # 调用urlopen()请求目标页面，请求成功会返还一个响应对象
        response = request.urlopen(rep)
        # 可通过urlopen方法返回的响应对象的read()、readline()、readlines()等方法读取响应数据
        html = response.read().decode('utf-8')
        # 定义提取相关信息的正则表达式模式
        comments_reg = r'(?s)<div data-cid=.+?class="hidden">'  # 用于提取评论信息的html代码块
        cmt_avator_src_reg = r'src="([^"]+)"'  # 提取用户头像的链接
        cmt_user_reg = r'<a href="([^"]+)" class="name">([^<]+)</a>'  # 提取评论用户的豆瓣网用户主页及昵称
        cmt_datetime_reg = r'<span content="([^"]+)" class="main-meta">([^<]+)</span>'  # 提取评论的发表时间
        cmt_title_reg = r'<h2><a href="([^"]+)">([^<]+)</a></h2>'  # 提取评论标题及评论详情页链接地址
        cmt_content_reg = r'<div class="short-content">\s*(.*?)\s*&nbsp;'  # 提取评论的简短文本内容
        cmt_list = re.findall(comments_reg, html)  # 先提取所有评论信息的html代码块
        comments = []  # 用于存储所有评论信息的列表
        for c in cmt_list:  # 循环处理每一条评论
            cmt = {
                'data_src': target_url,  # 评论数据的来源
                'avator_src': re.search(cmt_avator_src_reg, c).group(1),  # 用户头像的链接
                'user_page_url': re.search(cmt_user_reg, c).group(1),  # 评论用户的豆瓣网用户主页及
                'user_nick': re.search(cmt_user_reg, c).group(2),  # 评论用户的昵称
                'cmt_datetime': re.search(cmt_datetime_reg, c).group(2),  # 评论的发表时间
                'cmt_page_url': re.search(cmt_title_reg, c).group(1),  # 评论详情页链接地址
                'cmt_title': re.search(cmt_title_reg, c).group(2),  # 评论标题
                'cmt_content': re.search(cmt_content_reg, c, re.DOTALL).group(1)  # 评论的简短文本
            }
            comments.append(cmt)
        return comments
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    url = "https://movie.douban.com/subject/26910902/reviews?sort=time"
    print(get_comments(url))