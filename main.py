import math
import os
import re
from nltk.corpus import stopwords

def loadDataSet(path):
    """
    读取文本库中的文本内容以字典形式输出

    :param path: 文本库地址
    :return: 文本库字典｛文本名1：文本内容1，文本名2：文本内容2...｝
    """
    # 将文件夹内的文本全部导入程序
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    all_docu_dic = {}  # 接收文档名和文档内容的词典
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            f = open(path + "/" + file, encoding='UTF-8-sig')  # 打开文件
            iter_f = iter(f)  # 创建迭代器
            strr = ""
            for line in iter_f:  # 遍历文件，一行行遍历，读取文本
                strr = strr + line
            all_docu_dic[file] = strr.strip('.')   # 去除末尾的符号.
    print("文件库：")
    print(all_docu_dic)
    return all_docu_dic

def dealDataSet(all_docu_dic):
    """
    处理文件库字典的数据

    :param all_docu_dic:文本库字典｛文本名1：文本内容1，文本名2：文本内容2...｝
    :return: 1.all_words_set 文本库的词库｛word1,word2,...｝
             2.words_num_dic 文本词数字典｛txt1:{word1:num1,word2:num2},...｝
    """
    all_words = []
    all_docu_cut = {}  # 分完词后的dic(dic嵌套list)

    stop_words = stopwords.words('english')    # 原始停用词库
    # #停用词的扩展
    # print(len(stop_words))
    # extra_words = [' ']#新增的停用词
    # stop_words.extend(extra_words)#最后停用词
    # print(len(stop_words))

    # 计算所有文档总词库和分隔后的词库
    for filename, content in all_docu_dic.items():
        cut = re.split("[!? '.),(+-=。:]", content)  # 分词
        new_cut = [w for w in cut if w not in stop_words if w]  # 去除停用词，并且去除split后产生的空字符
        all_docu_cut[filename] = new_cut  # 键为文本名，值为分词完成的list
        all_words.extend(new_cut)
    all_words_set = set(all_words)  # 转化为集合形式

    # 计算各文本中的词数
    words_num_dic = {}
    for filename, cut in all_docu_cut.items():
        words_num_dic[filename] = dict.fromkeys(all_docu_cut[filename], 0)
        for word in cut:
            words_num_dic[filename][word] += 1
    # print("词库：")
    # print(all_words_set)
    print("文件分词库：")
    print(all_docu_cut)
    return all_words_set, words_num_dic     # 返回词库和文档词数字典

def computeTF(in_word, words_num_dic):
    """
    计算单词in_word在每篇文档的TF

    :param in_word: 单词
    :param words_num_dic: 文本词数字典｛txt1:{word1:num1,word2:num2},...｝
    :return: tfDict: 单词in_word在所有文本中的tf值字典 ｛文件名1：tf1,文件名2：tf2,...｝
    """
    allcount_dic = {}   # 各文档的总词数
    tfDict = {}     # in_word的tf字典
    # 计算每篇文档总词数
    for filename, num in words_num_dic.items():
        count = 0
        for value in num.values():
            count += value
        allcount_dic[filename] = count
    # 计算tf
    for filename, num in words_num_dic.items():
        if in_word in num.keys():
            tfDict[filename] = num[in_word] / allcount_dic[filename]
    return tfDict

def computeIDF(in_word, words_num_dic):
    """
    计算in_word的idf值

    :param in_word: 单词
    :param words_num_dic: 文本词数字典｛txt1:{word1:num1,word2:num2},...｝
    :return: 单词in_word在整个文本库中的idf值
    """
    docu_count = len(words_num_dic)     # 总文档数
    count = 0
    for num in words_num_dic.values():
        if in_word in num.keys():
            count += 1
    return math.log10((docu_count) / (count + 1))

def computeTFIDF(in_word, words_num_dic):
    """
    计算in_word在每篇文档的tf-idf值

    :param in_word: 单词
    :param words_num_dic: 文本词数字典｛txt1:{word1:num1,word2:num2},...｝
    :return: tfidf_dic:单词in_word在所有文本中的tf-idf值字典 ｛文件名1：tfidf1,文件名2：tfidf2,...｝
    """
    tfidf_dic = {}
    idf = computeIDF(in_word, words_num_dic)
    tf_dic = computeTF(in_word, words_num_dic)
    for filename, tf in tf_dic.items():
        tfidf_dic[filename] = tf * idf
    return tfidf_dic

def text_save(filename, data, word):
    """
    对检索词word的字典输出到filename的文件中

    :param filename:输出文本的文件名
    :param data: 字典类型
    :param word: 关键词
    """
    fp = open("D:/study/B4/" + filename, 'a')
    fp.write("关键词:" + str(word) + '\n')
    for line in data:
        for a in line:
            s = str(a)
            fp.write('\t' + s)
            fp.write('\t')
        fp.write('\n')
    fp.close()

def sortOut(dic):
    """
    对字典内容按照value值排序，并保留value值

    :param dic: 字典
    :return: 嵌套元组的list
    """
    return sorted(dic.items(), key=lambda item: item[1], reverse=True)

if __name__ == '__main__':
    # 载入文件
    print("\t默认文本库路径为：D:/study/B4/data")
    print("\t搜索结果文本路径为：D:/study/B4/result")
    path = "D:/study/B4/data"   # 文本库路径
    all_docu_dic = loadDataSet(path)  # 加载文本库数据到程序中
    words_set, words_num_dic = dealDataSet(all_docu_dic)    # 处理数据返回值1.文本词库（已去除停用词），2.各文本词数的词典
    n = 0   # 记录搜索次数
    a = -1  # 控制程序终止的变量
    while a != 0:
        in_words = input("搜索：")
        input_list = re.split("[!? '. ),(+-=。:]", in_words)
        k = 0  # 用于记录单次输入的有效关键词的个数
        n += 1
        for i in range(len(input_list)):
            if input_list[i] in words_set:
                k += 1
                tfidf_dic = computeTFIDF(input_list[i], words_num_dic)  # 单词的tfidf未排序字典
                # 控制台输出
                print("关键词:" + input_list[i])
                print(sortOut(tfidf_dic)[0:5])  # 输出前五个相关文本
                # 文本输出
                text_save("result" + str(n) + ".txt", sortOut(tfidf_dic)[0:5], input_list[i])  # 将排序后的tfidf字典保存到文件中
        if k == 0:
            print("无任何搜索结果")
        a = input("任意键继续搜索，'0'退出:")
        print("-------------------------------------")


