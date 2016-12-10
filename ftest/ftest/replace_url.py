# -*- coding: utf-8 -*-   
#with open('../test.csv', 'rb') as f:
    #reader = csv.reader(f)
    #for row in reader:
        #print row[2]
import sys
reload(sys)
sys.setdefaultencoding("utf-8")       
import json
import re
import os

with open('../test.json','rb') as f:
    #data = f.read()
    #os.chdir('../html')
    j = json.load(f)
    
    for d in j:
        w_str = ""
        html_file = d['html_name']
        #print type(html_file)
        os.chdir('../html')
        with open(html_file,'r') as rf:
            for line in rf:
                if re.search(d['pic_url'], line):
                    line=re.sub(d['pic_url'], '../pic/'+d['pic_local'],line)
                    #re.sub(pattern, repl, string)
                w_str+=line 
                #print w_str
        #dir_path='../html_new'    
        #if not os.path.exists(dir_path):
        #    os.makedirs(dir_path)   
        #os.chdir(dir_path)
        with open(html_file,'w') as wf:
            wf.write(w_str)