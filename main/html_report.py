#coding:UTF-8
'''
this is py2report's html_report moudle which a python script generate html mRNA report
log:
create by chencheng on 2017-05-05
add mapping and rseqc moudles on 2017-05-25
change report dir construction on 2017-06-08
import function for each part on 2017-06-10
'''
import os
import re
import sys
from . import mRNA_data_dict,mRNA_result_dict,html_jinja_env,pdf_jinja_env
reload(sys)
sys.setdefaultencoding('utf-8')

project_templates_dir = os.path.join(os.path.dirname(__file__),'html_templates')

def table2list(table_path,header=True,split='\t',max_row_num = 30,max_col_num = 100,max_cell_num = 15):
    if os.path.exists(table_path):
        table_list = []
        head_list = []
        with open(table_path,'r+') as f:
            for line in f:
                if header:
                    head_list = line.strip().split(split)
                    head_list = head_list if len(head_list) < max_col_num else head_list[:max_col_num]
                    header = False
                    continue
                body_list = line.strip().split(split)
                body_list = [k[:max_cell_num] for k in body_list]
                body_list = body_list if len(body_list) < max_col_num else body_list[:max_col_num]
                table_list.append(body_list)
        table_list = table_list if len(table_list) < max_row_num else table_list[:max_row_num]
        return [head_list,table_list]
    else:
        print 'no exists {file}'.format(file=table_path)
        sys.exit(1)

def enrichment_analysis(generate_report_path):
    '''
    param:report path
    '''
    enrichment_path = os.path.join(generate_report_path,mRNA_data_dict['enrichment'])
    if not os.path.exists(enrichment_path):
        print "enrichment analysis's dir not exists,please check your input path"
        sys.exit(1)
    go_list = table2list(os.path.join(enrichment_path,'report.go.table.txt'))
    kegg_list = table2list(os.path.join(enrichment_path,'report.kegg.table.txt'))
    sample_num = len(os.listdir(os.path.join(enrichment_path,'go')))
    all_file = []

    for root,dirs,files in os.walk(enrichment_path):
            all_file.extend([os.path.join(root,file) for file in files])

    multiple_plot_pattern = dict(go_barplots='go.enrichment.barplot.png$',
                              kegg_barplots='kegg.enrichment.barplot.png$',
                              dag_plots='ALL.CC.GO.DAG,png$',
                              pathway_plots='pathway.png$')

    multiple_plot_path = dict.fromkeys(multiple_plot_pattern.keys())
    for key,value in multiple_plot_path.items():
        multiple_plot_path[key] = [file.replace(os.path.join(generate_report_path,'analysis_report'),'..') for file in all_file if re.search(multiple_plot_pattern[key],file)]
    multiple_plot_path['pathway_plots'] = multiple_plot_path['pathway_plots'][:sample_num] #cut much more pathway plots

    go_path = os.path.join(mRNA_result_dict['enrichment'],'go')
    go_path = go_path.replace(generate_report_path,'../..')
    kegg_path = os.path.join(mRNA_result_dict['enrichment'],'kegg')
    kegg_path = kegg_path.replace(generate_report_path,'../..')
    #render enrichment emplates:
    template = html_jinja_env.get_template('enrichment_analysis.html')
    html_template_path = os.path.join(generate_report_path,'analysis_report','templates')
    if not os.path.exists(html_template_path):
        os.mkdir(html_template_path)
    with open(os.path.join(html_template_path,'rendered_enrichment_analysis.html'),'w+') as f:
		f.write(template.render(title = '富集分析',
		go_header=go_list[0],go_enrichment_table=go_list[1],
		all_go_enrichment_plot_path = multiple_plot_path['go_barplots'],
		all_dag_plot_path = multiple_plot_path['dag_plots'],
		kegg_header = kegg_list[0],kegg_enrichment_table = kegg_list[1],
		all_kegg_enrichment_plot_path = multiple_plot_path['kegg_barplots'],
		all_kegg_pathway_plot_path = multiple_plot_path['pathway_plots'],
		go_table_path = go_path,
		kegg_table_path = kegg_path,
		all_go_enrichment_plot_dir = kegg_path,
		all_dag_plot_dir = go_path,
		all_kegg_enrichment_plot_dir = kegg_path,
		all_kegg_pathway_plot_dir = kegg_path
		))

def fastqc_analysis(generate_report_path):
    '''
    param:report path
    '''
    fastqc_path = os.path.join(generate_report_path,mRNA_data_dict['fastqc'])
    if not os.path.exists(fastqc_path):
        print "fastqc analysis's dir not exists,please check your input path"
        sys.exit(1)
    qc_list = table2list(os.path.join(fastqc_path,'fastqc_general_stats.txt'))

    all_file = []
    for root,dirs,files in os.walk(fastqc_path):
            all_file.extend([os.path.join(root,file) for file in files])

    multiple_plot_pattern = dict(gc_plots='.gc_distribution.line.png$',
                                 reads_quality_plots='.reads_quality.bar.png$')

    multiple_plot_path = dict.fromkeys(multiple_plot_pattern.keys())
    for key,value in multiple_plot_path.items():
        multiple_plot_path[key] = [file.replace(os.path.join(generate_report_path,'analysis_report'),'..') for file in all_file if re.search(multiple_plot_pattern[key],file)]

    fastqc_stat_path = mRNA_result_dict['fastqc']
    fastqc_stat_path = fastqc_stat_path.replace(generate_report_path,'../..')
    gc_plot_path = os.path.join(mRNA_result_dict['fastqc'],'gc_plot')
    gc_plot_path = gc_plot_path.replace(generate_report_path,'../..')
    reads_quality_path = os.path.join(mRNA_result_dict['fastqc'],'reads_quality_plot')
    reads_quality_path = reads_quality_path.replace(generate_report_path,'../..')

    html_template_path = os.path.join(generate_report_path,'analysis_report','templates')
    if not os.path.exists(html_template_path):
        os.makedirs(html_template_path)
    #render fastqc templates:
    template = html_jinja_env.get_template('data_control.html')
    with open(os.path.join(html_template_path,'rendered_data_control.html'),'w+') as f:
        f.write(template.render(title = '数据质控',
        header=qc_list[0],qc_table=qc_list[1],
        all_quality_data_barplot_path = multiple_plot_path['reads_quality_plots'],
        qc_table_path=fastqc_stat_path,
        quality_barplot_dir=reads_quality_path
        ))

#def mapping_analysis()
