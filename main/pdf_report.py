#coding:UTF-8
'''
this is py2report's pdf_report moudle which a python script generate pdf mRNA report
log:
create by chencheng on 2017-06-13
add all href and plot_size on 2017-06-14
'''
import os
import sys
from . import mRNA_result_dict,pdf_analysis_path,pdf_jinja_env,pdf_settings,pdf_plots_size_dict

reload(sys)
sys.setdefaultencoding('utf-8')
def cut_overlong_table(row_list,max_len=pdf_settings['max_cell_len']):
    for i in range(len(row_list)):
        if len(row_list[i]) > max_len:
           row_list[i] = row_list[i][:max_len] + '...'
    return row_list

def three_line_list(input_path,split='\t',colunms):
    with open(input_path,'r+') as f:
        data = f.readlines()
        thead = data[0]
        table_cols = len(thead.strip().split(split))
        tbody = data[1:]
        if len(tbody) > pdf_settings['table_rows']:
            tboy = tboy[:pdf_settings['table_rows']]
        if table_cols < colunms:
            cols = table_cols
        else:
            cols = colunms
        table_list = []
        table_begin = '\\begin{tabular}{%s}' %('c'*cols)
        table_list.append(table_begin)
        head_list = cut_overlong_table(thead.strip('\n').split(split))[:cols]
        head_str = '&'.join(head_list).replace('_','\_').replace('%','\%').replace('#','\#') + r'\\'
        table_list.append(head_str)
        for line in tbody:
            each_list = cut_overlong_table(line.strip('\n').split(split))[:cols]
            each_str = '&'.join(each_list).replace('_','\_').replace('%','\%').replace('#','\#') + r'\\'
            table_list.append(each_str)
        return table_list

def check_file(file_dict,generate_report_path):
    for key,value in file_dict.items():
        file_dict[key] = os.path.join(generate_report_path,value)
        if not os.path.exists(file_dict[key]):
            print '{file} is not find in: {file_path}'.format(file=key,file_path=os.path.dirname(file_dict[key]))
            sys.exit(1)
        return file_dict

def create_pdf_report(generate_report_path):
    '''
    param:report path
    '''
    pdf_param_dict = {}
    pdf_param_dict.update(pdf_plots_size_dict)
    pdf_head_dict = dict(project_name=os.path.basename(generate_report_path),
                          report_name=pdf_settings['project_name'],
                          address=pdf_settings['address'],
                          phone=pdf_settings['phone'],
                          logo_path=pdf_settings['logo_path'],
                          pipeline_path=pdf_settings['pipeline_path'],
                          mRNAworkflow_path=pdf_settings['mRNAworkflow_path']
                          )
    pdf_param_dict.updatpdf_param_dict.update()
    #for all table
    ##enrichment part
    enrichment_analysis_path = pdf_analysis_path['enrichment']
    enrichment_analysis_path = check_file(enrichment_analysis_path)
    kegg_list = three_line_list(enrichment_analysis_path['kegg_table_path'],colunms=7)
    go_list = three_line_list(enrichment_analysis_path['go_table_path'],colunms=7)
    enrichment_dict = dict(kegg_begin=kegg_list[0],kegg_head=kegg_list[1],kegg_body=kegg_list[2:],
                                 go_begin=go_list[0],go_head=go_list[1],go_body=go_list[2:],
                                 go_barplot_path=enrichment_analysis_path['go_barplot_path'],
                                 dag_bp_path=enrichment_analysis_path['dag_bp_path'],
                                 dag_cc_path=enrichment_analysis_path['dag_cc_path'],
                                 dag_mf_path=enrichment_analysis_path['dag_mf_path'],
                                 kegg_barplot_path=enrichment_analysis_path['kegg_barplot_path'],
                                 pathview_path=enrichment_analysis_path['pathview_path'])
    pdf_param_dict.update(enrichment_dict)
    ##fastqc part
    fastqc_analysis_path = pdf_analysis_path['fastqc']
    fastqc_analysis_path = check_file(fastqc_analysis_path)
    qc_list = three_line_list(fastqc_analysis_path['qc_table_path'],colunms=6)
    fastqc_dict = dict(qc_begin=qc_list[0],qc_head=qc_list[1],qc_body=qc_list[2:],
                       gc_barplot_path=fastqc_analysis_path['gc_barplot_path'],
                       reads_quality_path=fastqc_analysis_path['reads_quality_path'],
                       )
    pdf_param_dict.update(fastqc_dict)
    ##mapping part
    mapping_analysis_path = pdf_analysis_path['mapping']
    mapping_analysis_path = check_file(mapping_analysis_path)
    mapping_list = three_line_list(mapping_analysis_path['mapping_table_path'],colunms=7)
    mapping_dict = dict(mapping_begin=mapping_list[0],mapping_head=mapping_list[1],mapping_body=mapping_list[2:],
                        mapping_plot_path=mapping_analysis_path)
    pdf_param_dict.update(mapping_dict)
    ##rseqc part
    rseqc_analysis_path = pdf_analysis_path['rseqc']
    rseqc_analysis_path = check_file(rseqc_analysis_path)
    rseqc_dict = dict(genebody_coverage_plot_path=rseqc_analysis_path['genebody_coverage_plot_path'],
                      inner_distance_plot_path=rseqc_analysis_path['inner_distance_plot_path'],
                      read_distribution_plot_path=rseqc_analysis_path['read_distribution_plot_path'])
    pdf_param_dict.update(rseqc_dict)
    ##quantification part
    quantification_analysis_path = pdf_analysis_path['quantification']
    quantification_analysis_path = check_file(quantification_analysis_path)
    gene_count_list = three_line_list(quantification_analysis_path['gene_table_path'],colunms=6)
    quantification_dict = dict(gene_count_begin=gene_count_list[0],
                               gene_count_head=gene_count_list[1],
                               gene_count_body=gene_count_list[2:],
                               correlation_heatmap_path=quantification_analysis_path['correlation_heatmap_path'],
                               gene_expression_path=quantification_analysis_path['gene_expression_path'],
                               pca_plot_path=quantification_analysis_path['pca_plot_path'])
    pdf_param_dict.update(quantification_dict)
    ##diff part
    diff_analysis_path = pdf_analysis_path['diff']
    diff_analysis_path = check_file(diff_analysis_path)
    diff_list = three_line_list(diff_analysis_path['diff_table_path'],colunms=5)
    diff_dict=dict(diff_begin=diff_list[0],diff_head=diff_list[1],diff_body=diff_list[2:],
                   volcano_plot_path=diff_analysis_path['volcano_plot_path'],
                   diff_heatmap_path=diff_analysis_path['diff_heatmap_path'])
    pdf_param_dict.update(diff_dict)

    template = pdf_jinja_env.get_template('mRNA_base')
    pdf_template_path = os.path.join(generate_report_path,'analysis_report')
    if not os.path.exists(pdf_template_path):
        os.makedirs(pdf_template_path)

    with open(os.path.join(pdf_template_path,'rendered_mRNA_report.tex'),'w+') as f:
        f.write(template.render(pdf_param_dict))
    print 'pdf report tex file done!'
