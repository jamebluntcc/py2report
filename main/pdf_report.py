#coding:UTF-8
'''
this is py2report's pdf_report moudle which a python script generate pdf mRNA report
log:
create by chencheng on 2017-06-13
'''
import os
import sys
from . import mRNA_result_dict,pdf_analysis_path,pdf_jinja_env

reload(sys)
sys.setdefaultencoding('utf-8')
