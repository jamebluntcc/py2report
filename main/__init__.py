#coding:UTF-8
import os
import jinja2
from copy import deepcopy
import configparser
'''
init html and pdf configure
'''
#template env config
html_jinja_env = jinja2.Environment(
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'html_templates'))
)
pdf_jinja_env = jinja2.Environment(
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'pdf_templates'))
)
#add each analysis part
configFilePath = os.path.join(os.path.dirname(__file__),'report_conf.conf')
command = configparser.ConfigParser()
command.read(configFilePath)
#all path
mRNA_data_path = command.get('mRNA-report-data','report_data_path')
mRNA_result_path = command.get('mRNA-report-result','report_result_path')
enrichment_path = command.get('mRNA-path','enrichment_path')
fastqc_path = command.get('mRNA-path','fastqc_path')
mapping_path = command.get('mRNA-path','mapping_path')
quantification_path = command.get('mRNA-path','quantification_path')
rseqc_path = command.get('mRNA-path','rseqc_path')

mRNA_data_dict = dict(enrichment=enrichment_path,fastqc=fastqc_path,
					  mapping=mapping_path,quantification=quantification_path,
					  rseqc=rseqc_path)
for key,value in mRNA_data_dict.items():
	mRNA_data_dict[key] = os.path.join(mRNA_data_path,value)

mRNA_result_dict = deepcopy(mRNA_data_dict)
for key,value in mRNA_result_dict.items():
	mRNA_result_dict[key] = os.path.join(mRNA_result_path,value)
