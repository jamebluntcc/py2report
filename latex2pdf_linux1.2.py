# coding=utf-8
'''
changed on 2016-10-28(add qc dir)
changed on 2016-11-1(update)
changed on 2016-11-3(add report_tmp dir)
version = 1.21
template engine using django templates
function:create mRNA_report
running on linux
'''

import re
import sys
import os
import time
import glob
import django
import subprocess
import configparser
from django.conf import settings
settings.configure(TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.abspath('/home/lxgui/chencheng/report/latex2pdf'),'templates','sequencing_report'),
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
    table_cols = len(thead.strip().split(split))
    tboy = data[1:]
    if len(tboy) > table_rows:
        tboy = tboy[:table_rows]
    f = open(os.path.join(template_dir,output_file),'wt',encoding='UTF-8')
    if table_cols < colunms:
        cols = table_cols
        f.write('\\begin{tabular}{%s}\n'%rep('c',cols))
    else:
        cols = colunms
        f.write('\\begin{tabular}{%s}\n' % rep('c', cols))
    f.write('%s\n'%(r'\toprule'))
    head_list = cut_overlong_table(thead.strip('\n').split(split))[:cols]
    f.write('&'.join(head_list).replace('_','\_').replace('%','\%').replace('#','\#') + r'\\' +'\n')
    f.write('%s\n'%(r'\midrule'))
    for line in tboy:
        each_list = cut_overlong_table(line.strip('\n').split(split))[:cols]
        f.write('&'.join(each_list).replace('_','\_').replace('%','\%').replace('#','\#') + r'\\' +'\n')
    f.write('\\bottomrule\n')
    f.write(r'\end{tabular}')
    f.close()
    return 0

def find_sample_file(dir,pattern):
    file_list = os.listdir(dir)
    first_dir = None
    for each_file in file_list:
        each_file_path = os.path.join(dir, each_file)
        if os.path.isdir(each_file_path):
            first_dir = each_file_path
            break
    if first_dir == None:
        print('there is no dir')
        sys.exit(1)
    file_list = glob.glob(os.path.join(first_dir,pattern))
    if len(file_list)!=1:
        print('ERROR in dir:%s'%dir)
        sys.exit(1)
    else:
        return file_list[0]

def find_merge_plot(dir,pattern):
    merge_plot = glob.glob(os.path.join(dir,pattern))
    if len(merge_plot) != 1:
        print(merge_plot)
        print('ERROR in dir:%s'%dir)
        exit(1)
    return merge_plot[0]

if __name__ == '__main__':
    #change it here
    template_dir = '/home/lxgui/chencheng/report/latex2pdf'
    if len(sys.argv) != 2:
        print('python %s + REPORT_DIR'%(sys.argv[0]))
        sys.exit(1)
    REPORT_DIR = sys.argv[1]

    REPORT_DIR_LIST = REPORT_DIR.split('/')
    REPORT_DIR_SHORT = '/'.join(REPORT_DIR_LIST[:len(REPORT_DIR_LIST)-1]) + '/'
    table_rows = 30
    command = configparser.ConfigParser()
    command.read('report_conf.conf')
    project_num = command.get('mRNA','project_num')
    report_name = command.get('mRNA','report_name')
    project_name = command.get('mRNA','project_name')
    # for qc data
    qc_table_01 = None
    for each_one in os.listdir(os.path.join(REPORT_DIR,'qc')):
        if re.search('qc.summary.txt',each_one):
            qc_table_01 = each_one
            three_line_table(os.path.join(os.path.join(REPORT_DIR,'qc'),each_one),
                                 'templates/data_table/01mRNA_qc_data.txt', '\t',colunms = 6)
    if qc_table_01 == None:
        print('No qc.summary data file')
        sys.exit(1)
    #for report_tmp
    report_tmp_dir = os.path.join(REPORT_DIR,'report_tmp')
    list_file = os.listdir(report_tmp_dir)
    all_quality_data_barplot_01 = volcano_plot_05 = None
    cluster_plot_07 = GO_barplot_08 = KEGG_barplot_09 = None
    for each_one in list_file:
        if re.search('all_quality_data_barplot.png', each_one):
            all_quality_data_barplot_01 = os.path.join(report_tmp_dir, each_one)
        elif re.search('volcano_merge_plot.png',each_one):
            volcano_plot_05 = os.path.join(report_tmp_dir,each_one)
        elif re.search('cluster_plot.png',each_one):
            cluster_plot_07 = os.path.join(report_tmp_dir,each_one)
        elif re.search('GO_merge_barplot.png',each_one):
            GO_barplot_08 = os.path.join(report_tmp_dir,each_one)
        elif re.search('KEGG_merge_barplot.png',each_one):
            KEGG_barplot_09 = os.path.join(report_tmp_dir,each_one)

    report_tmp_plot = (all_quality_data_barplot_01,volcano_plot_05,
                        cluster_plot_07,GO_barplot_08,KEGG_barplot_09)
    for each_one in report_tmp_dir:
        if each_one == None:
            print('some plot not in report_tmp_dir:%s'%report_tmp_dir)
            exit(1)

    # for quantification
    quantification_dir = os.path.join(REPORT_DIR,'quantification')
    list_file = os.listdir(quantification_dir)
    sample_correlation_plot_03 = gene_count_table_02 = None
    Gene_merge_plot_02 = PCA_plot_04 = None
    for each_one in list_file:
        if re.search('Gene.expression.png',each_one):
            Gene_merge_plot_02 = os.path.join(quantification_dir, each_one)
        if re.search('Gene.tpm.xls', each_one):
            gene_count_table_02 = os.path.join(quantification_dir, each_one)
            three_line_table(gene_count_table_02,'templates/data_table/02mRNA_gene_count.txt', '\t', colunms=6)
        elif re.search('sample_correlation.plot.png', each_one):
            sample_correlation_plot_03 = os.path.join(quantification_dir, each_one)
        elif re.search('PCA_plot.png',each_one):
            PCA_plot_04 = os.path.join(quantification_dir,each_one)

    plot_files = (gene_count_table_02,Gene_merge_plot_02,PCA_plot_04,sample_correlation_plot_03)
    for each_one in plot_files:
        if each_one == None:
            print('files NoExist,please checkout quantication dir:%s'%quantification_dir)
            print(plot_files)
            exit(1)
    # for enrichment and differential
    difftable_dir = GO_enrichtable_dir = KEGG_enrichtable_dir = None
    volcano_plot_dir = heatmap_dir = None
    GO_barplot_dir = GO_dagplot_dir = None
    KEGG_barplot_dir = KEGG_pathway_dir = None

    for roots, dirs, files in os.walk(REPORT_DIR):
        if re.search('diff_table$', roots):
            difftable_dir = roots
            three_line_table(find_sample_file(difftable_dir,pattern='*results.txt'),
                                'templates/data_table/03mRNA_diff_table.txt','\t',colunms=5)
        elif re.search('volcano_plot$', roots):
            volcano_plot_dir = roots
        elif re.search('heatmap$', roots):
            heatmap_dir = roots
        elif re.search('GO_bar_plot$', roots):
            GO_barplot_dir = roots
        elif re.search('GO_dag_plot$', roots):
            GO_dagplot_dir = roots
        elif re.search('GO_enrich_table$', roots):
            GO_enrichtable_dir = roots
            three_line_table(find_sample_file(GO_enrichtable_dir,pattern='*ALL.GO.enrich.xls'),
                                'templates/data_table/04mRNA_GO_enrichment_table.txt','\t',colunms=7)
        elif re.search('KEGG_bar_plot$', roots):
            KEGG_barplot_dir = roots
        elif re.search('KEGG_enrich_table$', roots):
            KEGG_enrichtable_dir = roots
            three_line_table(find_sample_file(KEGG_enrichtable_dir,pattern='*ALL.KEGG.enrich.xls'),
                                'templates/data_table/05mRNA_KEGG_enrichment_table.txt','\t',colunms=7)
        elif re.search('KEGG_pathway$', roots):
            KEGG_pathway_dir = roots

    all_href_dir = {'difftable_dir':difftable_dir,'GO_enrichtable_dir':GO_enrichtable_dir,
                    'KEGG_enrichtable_dir':KEGG_enrichtable_dir,'volcano_plot_dir':volcano_plot_dir,
                    'heatmap_dir':heatmap_dir, 'GO_barplot_dir':GO_barplot_dir, 'GO_dagplot_dir':GO_dagplot_dir,
                    'KEGG_barplot_dir':KEGG_barplot_dir, 'KEGG_pathway_dir':KEGG_pathway_dir}

    #print(all_href_dir)
    for k,v in all_href_dir.items():
        if v == None:
            print('%s is empty'%k)
            sys.exit(1)

    context = {'project_num': project_num,
               'report_name': report_name,
               'project_name': project_name,
               'all_quality_data_barplot_01': '{./' + all_quality_data_barplot_01.replace(REPORT_DIR_SHORT,'') + '}',
               'Gene_merge_plot_02': '{./' + Gene_merge_plot_02.replace(REPORT_DIR_SHORT,'') + '}',
               'sample_correlation_plot_03': '{./' + sample_correlation_plot_03.replace(REPORT_DIR_SHORT,'') + '}',
               'PCA_plot_04': '{./' + PCA_plot_04.replace(REPORT_DIR_SHORT,'') + '}',
               'diff_table_href': '{run:./' + difftable_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'volcano_plot_05': '{./' + volcano_plot_05.replace(REPORT_DIR_SHORT,'') + '}',
               'volcano_plot_href': '{run:./' + volcano_plot_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'heatmap_plot_06': '{./' + find_merge_plot(heatmap_dir,pattern='Heatmap.png').replace(REPORT_DIR_SHORT,'') + '}',
               'cluster_plot_07': '{./' + cluster_plot_07.replace(REPORT_DIR_SHORT,'') + '}',
               'heatmap_plot_href': '{run:./' + heatmap_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'GO_enrichment_table_href': '{run:./' + GO_enrichtable_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'GO_barplot_08': '{./' + GO_barplot_08.replace(REPORT_DIR_SHORT,'') + '}',
               'GO_barplot_href': '{run:./' + GO_barplot_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'GO_dagplot_BP': '{./' + find_sample_file(GO_dagplot_dir, pattern='ALL.BP.GO.DAG.png').replace(REPORT_DIR_SHORT,'') + '}',
               'GO_dagplot_CC': '{./' + find_sample_file(GO_dagplot_dir, pattern='ALL.CC.GO.DAG.png').replace(REPORT_DIR_SHORT,'') + '}',
               'GO_dagplot_MF': '{./' + find_sample_file(GO_dagplot_dir, pattern='ALL.MF.GO.DAG.png').replace(REPORT_DIR_SHORT,'') + '}',
               'GO_dagplot_href': '{run:./' + GO_dagplot_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'KEGG_enrichment_table_href': '{run:./' + KEGG_enrichtable_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'KEGG_barplot_09': '{./' + KEGG_barplot_09.replace(REPORT_DIR_SHORT,'') + '}',
               'KEGG_barplot_href': '{run:./' + KEGG_barplot_dir.replace(REPORT_DIR_SHORT,'') + '}',
               'KEGG_pathway1': '{./' + find_sample_file(KEGG_pathway_dir, pattern='ALL_pathway').replace(REPORT_DIR_SHORT,'') + '/' +
                               os.listdir(find_sample_file(KEGG_pathway_dir, pattern='ALL_pathway'))[0] + '}',
               'KEGG_pathway2': '{./' + find_sample_file(KEGG_pathway_dir, pattern='ALL_pathway').replace(
                   REPORT_DIR_SHORT, '') + '/' +
                               os.listdir(find_sample_file(KEGG_pathway_dir, pattern='ALL_pathway'))[1] + '}',
               'KEGG_pathway3': '{./' + find_sample_file(KEGG_pathway_dir, pattern='ALL_pathway').replace(
                   REPORT_DIR_SHORT, '') + '/' +
                               os.listdir(find_sample_file(KEGG_pathway_dir, pattern='ALL_pathway'))[2] + '}',
               'KEGG_pathway_href': '{run:./' + KEGG_pathway_dir.replace(REPORT_DIR_SHORT,'') + '}'
               }
    output_tex_file = project_num + '_mRNA_report.tex'
    create_template('mRNA_main.txt',os.path.join(REPORT_DIR_SHORT,output_tex_file), context)
#run xelatex:
    ref_file= os.path.join(template_dir,'templates/mRNA_report/')+'ref.bib'
    os.chdir(REPORT_DIR_SHORT)
    output_aux_file = output_tex_file.replace('tex','aux')
    tex_list = glob.glob(os.path.join(REPORT_DIR_SHORT,output_tex_file))
    rm_set = ('.aux','.log','.out','.toc','.tex','.tmp','.bib','.bbl','.blg')
    
    if len(tex_list) == 1:
        subprocess.call('cp %s ./' %ref_file,shell=True)
        subprocess.call('xelatex %s > summary.tmp' %output_tex_file,shell=True)
        subprocess.call('bibtex %s > summary.tmp' %output_aux_file, shell=True)
        subprocess.call('xelatex %s > summary.tmp' % output_tex_file, shell=True)
        subprocess.call('xelatex %s > summary.tmp' % output_tex_file, shell=True)
        for each_file in os.listdir(REPORT_DIR_SHORT):
            if os.path.splitext(each_file)[1] in rm_set:
                subprocess.call('rm %s' %each_file,shell=True)
    else:
        print('Not one tex file in %s!'%REPORT_DIR_SHORT)
        sys.exit(1)

   # os.chdir(REPORT_DIR)
   # subprocess.call('rm -rf report_tmp/',shell=True)
    subprocess.call('echo mRNA report done!', shell=True)

