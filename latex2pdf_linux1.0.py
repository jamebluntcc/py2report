# coding=utf-8
'''
changed on 2016-10-28(add qc dir)
version = 1.20
template engine using django templates
function:create mRNA_report
'''

import re
import sys
import os
import time
import glob
import django
import subprocess
from django.conf import settings
settings.configure(TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.abspath('/home/lxgui/chencheng/report/latex2pdf'),'templates','sequencing_report'),
                 os.path.join(os.path.abspath('/home/lxgui/chencheng/report/latex2pdf'),'templates','data_fig'),
                 os.path.join(os.path.abspath('/home/lxgui/chencheng/report/latex2pdf'),'templates','mRNA_report'),
                 os.path.join(os.path.abspath('/home/lxgui/chencheng/report/latex2pdf'),'templates','data_table')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
])
django.setup()
from django.template import Context
from django.template.loader import get_template

def rep(str,n):
    i = 0
    tmp_str = ''
    while i < n:
        tmp_str = tmp_str + str
        i += 1
    return tmp_str

def create_template(template_file,output_file,context):
    t = get_template(template_file)
    file = t.render(Context(context))
    try:
        f = open(output_file,'w',encoding='UTF-8')
        f.write(file)
        f.close()
    except IOError as e:
        print(e)
        sys.exit(1)

def cut_overlong_table(row_list,max_len=20):
    for i in range(len(row_list)):
        if len(row_list[i]) > max_len:
           row_list[i] = row_list[i][:max_len] + '...'
    return row_list

def three_line_table(input_file,output_file,split,colunms):
    with open(input_file,'rt',encoding='UTF-8') as f:
        data = f.readlines()
    thead = data[0]
    tboy = data[1:len(data)]
    if len(tboy) > table_rows:
        tboy = tboy[:table_rows]
    f = open(os.path.join(template_dir,output_file),'wt',encoding='UTF-8')
    f.write('\\begin{tabular}{%s}\n'%rep('c',colunms))
    f.write('%s\n'%(r'\toprule'))
    head_list = cut_overlong_table(thead.strip('\n').split(split))[:colunms]
    f.write('&'.join(head_list).replace('_','\_').replace('%','\%').replace('#','\#') + r'\\' +'\n')
    f.write('%s\n'%(r'\midrule'))
    for line in tboy:
        each_list = cut_overlong_table(line.strip('\n').split(split))[:colunms]
        f.write('&'.join(each_list).replace('_','\_').replace('%','\%').replace('#','\#') + r'\\' +'\n')
    f.write('\\bottomrule\n')
    f.write(r'\end{tabular}')
    f.close()
    return 0

def find_sample_file(dir,pattern):     
    file_list = os.listdir(dir)
    first_dir = None
    for each_file in file_list:
        each_file_path = os.path.join(dir, each_file).replace('\\','/')
        if os.path.isdir(each_file_path):
            first_dir = each_file_path
            break
    if first_dir == None:
        print('there is no dir')
        sys.exit(1)
    #print(first_dir)
    file_list = glob.glob(os.path.join(first_dir,pattern))
    if len(file_list)!=1:
        print(dir)
        print('THERE IS NOT ONE TABLE YOU NEED,BUT WE ONLY NEED ONE!')
        sys.exit(1)
    else:
        return file_list[0].replace('\\','/')

if __name__ == '__main__':
    #change it here
    template_dir = '/home/lxgui/chencheng/report/latex2pdf'
    if len(sys.argv) != 2:
        print('python %s + REPORT_DIR'%(sys.argv[0]))
        sys.exit(1)
    REPORT_DIR = sys.argv[1]

    REPORT_DIR_LIST = REPORT_DIR.split('/')
    #print(REPORT_DIR_LIST)
    REPORT_DIR_SHORT = '/'.join(REPORT_DIR_LIST[:len(REPORT_DIR_LIST)-1]) + '/'
    #REPORT_DIR_SHORT = REPORT_DIR_SHORT.replace('\\','/')
    table_rows = 30

    data_stat_table = None
    for each_one in os.listdir(os.path.join(REPORT_DIR,'qc').replace('\\','/')):
        if re.search('qc.summary.txt',each_one):
            data_stat_table = each_one
            three_line_table(os.path.join(os.path.join(REPORT_DIR,'qc'),each_one),
                                 'templates/data_table/readcount.txt', '\t',colunms = 6)
    if data_stat_table == None:
        print('No data_stat file')
        sys.exit(1)

    # for quantification
    no_href_dir = os.path.join(REPORT_DIR,'quantification').replace('\\','/')
    list_file = os.listdir(no_href_dir)
    Gene_expression_plot = sample_correlation_plot = read_count_table = None
    for each_one in list_file:
        if re.search('readcount', each_one):
            read_count_table = os.path.join(no_href_dir, each_one).replace('\\', '/')
        elif re.search('Gene_expression.png', each_one):
            Gene_expression_plot = os.path.join(no_href_dir, each_one).replace('\\', '/')
        elif re.search('sample_correlation.plot.png', each_one):
            sample_correlation_plot = os.path.join(no_href_dir, each_one).replace('\\', '/')

    if read_count_table == None:
        print('No read_count file')
        sys.exit(1)
    elif Gene_expression_plot == None:
        print('No Gene expression file')
        sys.exit(1)
    elif sample_correlation_plot == None:
        print('no sample corrlation file')
        sys.exit(1)

    # for enrichment and differential
    # ����ڴ��ڳ����ӵ��ļ�
    difftable_dir = GO_enrichtable_dir = KEGG_enrichtable_dir = None
    volcano_plot_dir = heatmap_dir = None
    GO_barplot_dir = GO_dagplot_dir = None
    KEGG_barplot_dir = KEGG_pathway_dir = None

    for roots, dirs, files in os.walk(REPORT_DIR):
        if re.search('diff_table$', roots):
            difftable_dir = roots.replace('\\', '/')
            three_line_table(find_sample_file(difftable_dir,pattern='*results.txt'),
                                'templates/data_table/diff_table.txt','\t',colunms=5)
        elif re.search('volcano_plot$', roots):
            volcano_plot_dir = roots.replace('\\', '/')
        elif re.search('heatmap$', roots):
            heatmap_dir = roots.replace('\\', '/')
        elif re.search('GO_bar_plot$', roots):
            GO_barplot_dir = roots.replace('\\', '/')
        elif re.search('GO_dag_plot$', roots):
            GO_dagplot_dir = roots.replace('\\', '/')
        elif re.search('GO_enrich_table$', roots):
            GO_enrichtable_dir = roots.replace('\\', '/')
            three_line_table(find_sample_file(GO_enrichtable_dir,pattern='*ALL.GO.enrich.xls'),
                                'templates/data_table/GO_enrichment_table.txt','\t',colunms=7)
        elif re.search('KEGG_bar_plot$', roots):
            KEGG_barplot_dir = roots.replace('\\', '/')
        elif re.search('KEGG_enrich_table$', roots):
            KEGG_enrichtable_dir = roots.replace('\\', '/')
            three_line_table(find_sample_file(KEGG_enrichtable_dir,pattern='*ALL.KEGG.enrich.xls'),
                                'templates/data_table/KEGG_enrichment_table.txt','\t',colunms=7)
        elif re.search('KEGG_pathway$', roots):
            KEGG_pathway_dir = roots.replace('\\', '/')

    all_href_dir = {'difftable_dir':difftable_dir,'GO_enrichtable_dir':GO_enrichtable_dir,
                    'KEGG_enrichtable_dir':KEGG_enrichtable_dir,'volcano_plot_dir':volcano_plot_dir,
                    'heatmap_dir':heatmap_dir, 'GO_barplot_dir':GO_barplot_dir, 'GO_dagplot_dir':GO_dagplot_dir,
                    'KEGG_barplot_dir':KEGG_barplot_dir, 'KEGG_pathway_dir':KEGG_pathway_dir}

    #print(all_href_dir)
    for k,v in all_href_dir.items():
        if v == None:
            print('%s is empty'%k)
            sys.exit(1)

    context = {'project_num': 'OM-mRNA-15-Medicago\_truncatula',
               'report_name': 'mRNA Analysis Report',
               'project_name': 'mRNA Report',
               'gene_expression_plot': '{./' + Gene_expression_plot.replace(REPORT_DIR_SHORT,'') + '}',
               'sample_cor_matrix': '{./' + sample_correlation_plot.replace(REPORT_DIR_SHORT,'') + '}',
               'diff_table_href': '{run:./' + difftable_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'volcano_plot': '{./' + find_sample_file(volcano_plot_dir,pattern='*png').replace(REPORT_DIR_SHORT,'') + '}',
               'volcano_plot_href': '{run:./' + volcano_plot_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'heatmap_plot': '{./' + heatmap_dir.replace(REPORT_DIR_SHORT,'') + '/Heatmap.png' + '}',
               'heatmap_plot_href': '{run:./' + heatmap_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'GO_enrichment_table_href': '{run:./' + GO_enrichtable_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'GO_barplot': '{./' + find_sample_file(GO_barplot_dir, pattern='*ALL.GO.bar.png').replace(REPORT_DIR_SHORT,'') + '}',
               'GO_barplot_href': '{run:./' + GO_barplot_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'GO_dagplot': '{./' + find_sample_file(GO_dagplot_dir, pattern='ALL.BP.GO.DAG.png').replace(REPORT_DIR_SHORT,'') + '}',
               'GO_dagplot_href': '{run:./' + GO_dagplot_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'KEGG_enrichment_table_href': '{run:./' + KEGG_enrichtable_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'KEGG_barplot': '{./' + find_sample_file(KEGG_barplot_dir, pattern='*ALL.KEGG.bar.png').replace(REPORT_DIR_SHORT,'') + '}',
               'KEGG_barplot_href': '{run:./' + KEGG_barplot_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'KEGG_pathway': '{./' + find_sample_file(KEGG_pathway_dir, pattern='ALL_pathway').replace(REPORT_DIR_SHORT,'') + '/' +
                               os.listdir(find_sample_file(KEGG_pathway_dir, pattern='ALL_pathway'))[0] + '}',
               'KEGG_pathway_href': '{run:./' + KEGG_pathway_dir.replace(REPORT_DIR_SHORT,'') + '}'
               }
    output_tex_file = 'mRNA_analysis_report.tex'
    create_template('mRNA_main.backup',os.path.join(REPORT_DIR_SHORT,output_tex_file), context)
    #print(os.path.join(REPORT_DIR_SHORT,output_tex_file))

#run xelatex:
    os.chdir(REPORT_DIR_SHORT)
    tex_list = glob.glob(os.path.join(REPORT_DIR_SHORT,output_tex_file))
    rm_set = ('.aux','.log','.out','.tex','.toc','.tmp')
    if len(tex_list) == 1:
        subprocess.call('xelatex %s' %output_tex_file,shell=True)
        subprocess.call('xelatex %s' %output_tex_file, shell=True)
        for each_file in os.listdir(REPORT_DIR_SHORT):
            if os.path.splitext(each_file)[1] in rm_set:
                subprocess.call('rm %s' %each_file,shell=True)
        subprocess.call('echo all done!',shell=True)
    else:
        print('match more than one tex file!')
        sys.exit(1)

