#coding=utf-8
import re
import os
import sys
import django
import glob
from django.conf import settings

table_rows = 30
template_dir = '/home/lxgui/chencheng/report/latex2pdf'
reload(sys)
sys.setdefaultencoding('utf-8')

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

def create_mRNA_file_map(mRNA_report_dir):
    # qc dir
    qc_dir = os.path.join(mRNA_report_dir, 'qc')
    qc_file = os.path.join(qc_dir, 'qc.summary.txt')

    # assembly dir
    assembly_dir = os.path.join(mRNA_report_dir, 'assembly')
    assembly_gene_length_plot = os.path.join(assembly_dir, 'Gene_length_distribution.png')
    assembly_isoform_length_plot = os.path.join(assembly_dir, 'Isoform_length_distribution.png')
    assembly_stat_table = os.path.join(assembly_dir, 'Trinity.stat.txt')

    # report_tmp_dir
    report_tmp_dir = os.path.join(mRNA_report_dir, 'report_tmp')
    all_quality_data_barplot = os.path.join(report_tmp_dir, 'all_quality_data_barplot.png')
    volcano_example_plot = os.path.join(report_tmp_dir, 'volcano_example_plot.png')
    cluster_example_plot = os.path.join(report_tmp_dir, 'cluster_plot.png')
    go_example_plot = os.path.join(report_tmp_dir, 'GO_example_barplot.png')
    kegg_example_plot = os.path.join(report_tmp_dir, 'KEGG_example_barplot.png')
    diff_table = os.path.join(report_tmp_dir,'diff.table.txt')
    # quantification
    quantification_dir = os.path.join(mRNA_report_dir, 'quantification')
    sample_correlation_plot = os.path.join(quantification_dir, 'sample_correlation.plot.png')
    pca_plot = os.path.join(quantification_dir, 'PCA_plot.png')
    gene_merge_plot = os.path.join(quantification_dir, 'Gene_expression.png')
    gene_count_table = os.path.join(quantification_dir, 'Gene.tpm.xls')

    mRNA_report_file_info = {'qc_summary_txt': qc_file, 'Trinity_stat_txt': assembly_stat_table,
                             'diff_table_txt':diff_table,
                             'Isoform_length_distribution': assembly_isoform_length_plot,
                             'Gene_length_distribution': assembly_gene_length_plot,
                             'all_quality_data_barplot': all_quality_data_barplot,
                             'volcano_example_plot': volcano_example_plot,
                             'cluster_example_plot': cluster_example_plot, 'GO_example_plot': go_example_plot,
                             'KEGG_example_plot': kegg_example_plot, 'Gene_expression_plot': gene_merge_plot,
                             'Gene_tmp_xls': gene_count_table, 'sample_correlation_plot': sample_correlation_plot,
                             'PCA_plot': pca_plot}
    return  mRNA_report_file_info

def create_mRNA_dir_map(mRNA_report_dir):
    # enrichment and differential
    target_dir = dict.fromkeys(['diff_table$', 'volcano_plot$', 'heatmap$', 'GO_bar_plot$',
                                'GO_dag_plot$', 'GO_enrich_table$', 'KEGG_bar_plot$',
                                'KEGG_enrich_table$', 'KEGG_pathway$'])

    for roots, dirs, files in os.walk(mRNA_report_dir):
        for key, value in target_dir.items():
            if re.search(key, roots):
                target_dir[key] = roots

    difftable_dir = target_dir['diff_table$']
    volcano_plot_dir = target_dir['volcano_plot$']
    heatmap_dir = target_dir['heatmap$']
    go_barplot_dir = target_dir['GO_bar_plot$']
    kegg_barplot_dir = target_dir['KEGG_bar_plot$']
    go_dagplot_dir = target_dir['GO_dag_plot$']
    go_enrichtable_dir = target_dir['GO_enrich_table$']
    kegg_enrichtable_dir = target_dir['KEGG_enrich_table$']
    kegg_pathway_dir = target_dir['KEGG_pathway$']

    mRNA_report_dir_info = {'difftable_dir': difftable_dir, 'volcano_plot_dir': volcano_plot_dir,
                            'heatmap_dir': heatmap_dir, 'go_barplot_dir': go_barplot_dir,
                            'kegg_barplot_dir': kegg_barplot_dir, 'go_dagplot_dir': go_dagplot_dir,
                            'go_enrichtable_dir': go_enrichtable_dir,
                            'kegg_enrichtable_dir': kegg_enrichtable_dir, 'kegg_pathway_dir': kegg_pathway_dir}

    return mRNA_report_dir_info

def create_template(template_file,output_file,context):
    t = get_template(template_file)
    file = t.render(Context(context))
    f = open(output_file,'w+')
    f.write(file)
    f.close()
    return 0

def cut_overlong_table(row_list,max_len=20):
    for i in range(len(row_list)):
        if len(row_list[i]) > max_len:
           row_list[i] = row_list[i][:max_len] + '...'
    return row_list

def three_line_table(input_file,output_file,split,colunms):
    with open(input_file,'r+') as f:
        data = f.readlines()
    thead = data[0]
    table_cols = len(thead.strip().split(split))
    tboy = data[1:]
    if len(tboy) > table_rows:
        tboy = tboy[:table_rows]
    f = open(os.path.join(template_dir,output_file),'w+')
    if table_cols < colunms:
        cols = table_cols
        f.write('\\begin{tabular}{%s}\n'%('c'*cols))
    else:
        cols = colunms
        f.write('\\begin{tabular}{%s}\n' %('c'*cols))
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

def find_sample_file(dir,pattern):
    sample_dir_list = [k for k in os.listdir(dir) if os.path.isdir(os.path.join(dir,k))]
    if len(sample_dir_list) == 0:
        print 'this is no sample dir in {dir}'.format(dir=dir)
        sys.exit(1)
    all_match = glob.glob(os.path.join(dir, sample_dir_list[0], pattern))
    if os.path.isfile(os.path.join(dir,sample_dir_list[0],all_match[0])) and len(all_match) == 1:
        return os.path.join(dir,sample_dir_list[0],all_match[0])
    elif os.path.isdir(os.path.join(dir,sample_dir_list[0],all_match[0])) and len(all_match) == 1:
        file_list = os.listdir(os.path.join(dir,sample_dir_list[0],all_match[0]))[:3]
        return [os.path.join(dir,sample_dir_list[0],pattern,k) for k in file_list]
    else:
        print 'no match file or dir in {dir}'.format(dir=os.path.join(dir,sample_dir_list[0]))
        sys.exit(1)
