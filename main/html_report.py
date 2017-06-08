#coding:UTF-8
'''
this is py2report's html_report moudle which a python script generate html mRNA report
log:
create by chencheng on 2017-05-05
add mapping and rseqc moudles on 2017-05-25
change report dir construction on 2017-06-08
'''
import os
import glob
from ..setting import all_path,enrichment_part,fastqc_part,mapping_part,quantification_part,rseqc_part

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

def html_run(report_path):
    #for fastqc
    replace_dir = report_path.rstrip('/').rsplit('/',1)[0]
    report_dir_name = '_'.join([mRNA_report_dir.rstrip('/').rsplit('/',1)[1],'report'])

    if os.path.exists(os.path.join(report_path,all_path['fastqc_path'])):
        gc_distribution_plots = glob.glob(os.path.join(report_path,fastqc_part['gc_distribution_pattern']))
        reads_quality_plots = glob.glob(os.path.join(report_path,fastqc_part['reads_quality_pattern']))
        fastqc_table = os.path.join(report_path,fastqc_part['fastqc_table'])
        fastqc_list = table2list(fastqc_table)
        #transform to templates_path:
        gc_distribution_plots = [k.replace(replace_dir,'../..') for k in gc_distribution_plots]
        reads_quality_plots = [k.replace(replace_dir,'../..') for k in reads_quality_plots]
        gc_distribution_plots_path = 
    #for mapping
    if os.path.exists(os.path.join(report_path,all_path['mapping_path'])):
        mapping_plot = os.path.join(report_path,mapping_part['mapping_plot'])
        mapping_table = os.path.join(report_path,mapping_part['mapping_table'])
        mapping_list = table2list(mapping_table)
    #for rseqc
    if os.path.exists(os.path.join(report_path,all_path['rseqc_path'])):
        reads_duplication_plots = glob.glob(os.path.join(report_path,rseqc_part['reads_duplication_pattern']))
        genebody_coverage_plots = glob.glob(os.path.join(report_path,rseqc_part['genebody_coverage_pattern']))
        inner_distance_plots = glob.glob(os.path.join(report_path,rseqc_part['inner_distance_pattern']))
        reads_distribution_plots = glob.glob(os.path.join(report_path,rseqc_part['reads_distribution_pattern']))
    #for quantification and diff
    if os.path.exists(os.path.join(report_path,all_path['quantification_path'])):
        volcano_plots = glob.glob(os.path.join(report_path,quantification_part['volcano_plot_pattern']))
        diff_gene_heatmap_plot = os.path.join(report_path,quantification_part['diff_gene_heatmap_plot'])
        gene_expression_plot = os.path.join(report_path,quantification_part['gene_expression_plot'])
        pca_plot = os.path.join(report_path,quantification_part['pca_plot'])
        sample_correlation_plot = os.path.join(report_path,quantification_part['sample_correlation_plot'])
        html_diff_table = os.path.join(report_path,quantification_part['html_diff_table'])
        html_gene_table = os.path.join(report_path,quantification_part['html_gene_table'])
    #for enrichment
    if os.path.exists(os.path.join(report_path,all_path['enrichment_path'])):
        go_table = os.path.join(report_path,enrichment_part['go_table'])
        go_list = table2list(go_table)
        kegg_table = os.path.join(report_path,enrichment_part['kegg_table'])
        kegg_list = table2list(kegg_table)
        go_barplots = glob.glob(os.path.join(report_path,enrichment_part['go_bar_pattern']))
        go_dagplots = glob.glob(os.path.join(report_path,enrichment_part['go_dag_pattern']))
        kegg_barplots = glob.glob(os.path.join(report_path,enrichment_part['kegg_bar_pattern']))
        kegg_pathway_plots = glob.glob(os.path.join(report_path,enrichment_part['kegg_pathway_pattern']))
