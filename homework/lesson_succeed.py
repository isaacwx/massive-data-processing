from math import sqrt
import re
import os
import time
import multiprocessing as mul
import json
#读入待分析的文件
t=time.time()
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
filename='lesson/199801_clear (1).txt'
list_file=[]
result_all=[]
#利用停用词表，将词分好并保存到向量中
stopwords=[]
result_file='lesson/result_file.json'
fstop=open('lesson/stop_words.txt','r',encoding='utf-8-sig')
for eachWord in fstop:
    eachWord = re.sub("\n", "", eachWord)
    stopwords.append(eachWord)
fstop.close()
with open(filename,encoding='gbk') as f:
    for line in f:
        if line=='' or line==' ' or line=='\n':
            continue
        line=line.replace(" ","")
        line=line.replace("\n","")
        for i in stopwords:
            line=line.replace(i,"")
        line=line.split('/')
        line=line[1:]
        while '' in line:
            line.remove('')
        list_file.append(line)
print(time.time()-t)
t=time.time()
def function(start_input):
    if(start_input+100<=len(list_file)):
        end_input=start_input+100
    else:
        end_input=len(list_file)          
    for a in range(start_input,end_input):
        for b in range(a):
            s1_cut = list_file[a]  
            s2_cut = list_file[b]
            word_set = set(s1_cut).union(set(s2_cut))

            #用字典保存两个分段中出现的所有词并编上号
            word_dict = dict()
            i = 0
            for word in word_set:
                word_dict[word] = i
                i += 1

            #根据词袋模型统计词在每段中出现的次数，形成向量
            s1_cut_code = [0]*len(word_dict)
            for word in s1_cut:
                s1_cut_code[word_dict[word]]+=1

            s2_cut_code = [0]*len(word_dict)
            for word in s2_cut:
                s2_cut_code[word_dict[word]]+=1

            # 计算余弦相似度
            sum = 0
            sq1 = 0
            sq2 = 0
            for i in range(len(s1_cut_code)):
                sum += s1_cut_code[i] * s2_cut_code[i]
                sq1 += s1_cut_code[i] * s1_cut_code[i]
                sq2 += s2_cut_code[i] * s2_cut_code[i]

            if sq1==0 or sq2==0 or sum==0:
                result = 0.0
            else:
                result = sum / (sqrt(sq1*sq2))
            result_all.append(result)
            if a==5000 and b==0:
                print(time.time()-t)
    if a==(len(list_file)-1):
        with open(result_file,'w') as f_1:
            json.dump(result_all,f_1)
    

if __name__ == '__main__':
    pool = mul.Pool(6)
    list=[i for i in range(1,len(list_file),100)]
    pool.map(function, list) 
print(time.time()-t) 
