#coding:UTF-8
'''
this is py2report's pdf_report moudle which a python script generate pdf mRNA report
this version only run on 34
log:
create by chencheng on 2017-06-13
add all href and plot_size on 2017-06-14
add all function doc on 2017-06-16
'''
import os
import sys
import subprocess
from . import mRNA_data_dict,pdf_analysis_path,pdf_jinja_env,pdf_settings,pdf_plots_size_dict

reload(sys)
sys.setdefaultencoding('utf-8')
ref_file_path = '/home/chencheng/myproject/py2report/main/pdf_templates/ref.bib'
def cut_overlong_table(row_list,max_len=int(pdf_settings['max_cell_len'])):
    '''
    param:
    row_list: each analysis part's table rwo list apply in three_line_list function
    max_cell_len: threshold value to cut table cell
    function: cut table cell's length when over 20 chars
    '''
    for i in range(len(row_list)):
        if len(row_list[i]) > max_len:
           row_list[i] = row_list[i][:max_len] + '...'
    return row_list

def three_line_list(input_path,colunms,split='\t'):
    '''
    param:
    input_path: each analysis part's table path
    colunms: threshold value to table colunms
    function: transform each analysis part's table into table_list
    '''
    if input_path:
        with open(input_path,'r+') as f:
            data = f.readlines()
            thead = data[0]
            table_cols = len(thead.strip().split(split))
            tbody = data[1:]
            if len(tbody) > int(pdf_settings['table_rows']):
                tbody = tbody[:int(pdf_settings['table_rows'])]

            if table_cols < colunms:
                cols = table_cols
            else:
                cols = colunms

            table_list = []
            table_begin = '\\begin{tabular}{%s}' %('c'*cols)
            table_list.append(table_begin)

            if cols > 3:
                head_list = cut_overlong_table(thead.strip('\n').split(split))[:cols]
            else:
                head_list = thead.strip('\n').split(split)

            head_str = '&'.join(head_list).replace('_','\_').replace('%','\%').replace('#','\#') + r'\\'
            table_list.append(head_str)
            for line in tbody:
                if cols > 3:
                    each_list = cut_overlong_table(line.strip('\n').split(split))[:cols]
                else:
                    each_list = line.strip('\n').split(split)
                each_str = '&'.join(each_list).replace('_','\_').replace('%','\%').replace('#','\#') + r'\\'
                table_list.append(each_str)
            return table_list
    else:
        return None

def check_file(file_dict,generate_report_path,part):
    '''
    param:
    file_dict:each analysis part's path dict
    generate_report_path:a path where to your analysis's report data
    function:check each path's exists and add generate_report_path into them
    '''
    for key,value in file_dict.items():
        file_dict[key] = os.path.join(generate_report_path,value)
        if not os.path.exists(file_dict[key]):
            if part:
                print '{file} is not find in: {file_path}'.format(file=key,file_path=os.path.dirname(file_dict[key]))
                sys.exit(1)
            else:
                file_dict[key] = None

def run_tex(tex_path):
    '''
    param:
    tex_path:generate pdf report's tex path
    function:transform tex file into pdf file
    '''
    tex_dir = os.path.dirname(tex_path)
    tex_file = os.path.basename(tex_path)
    os.chdir(tex_dir)
    aux_file = tex_file.replace('tex','aux')
    rm_set = ['.aux','.log','.out','.toc','.tmp','.bib','.bbl','.blg','.tex']
    subprocess.call('cp {ref_file} {tex_dir}'.format(ref_file=ref_file_path,tex_dir=tex_dir),shell=True)
    subprocess.call('xelatex {tex_file} > summary'.format(tex_file=tex_file),shell=True)
    subprocess.call('bibtex {aux_file}'.format(aux_file=aux_file),shell=True)
    subprocess.call('xelatex {tex_file} > summary'.format(tex_file=tex_file),shell=True)
    subprocess.call('xelatex {tex_file} > summary'.format(tex_file=tex_file),shell=True)
    for each_file in os.listdir(tex_dir):
        if os.path.splitext(each_file)[1] in rm_set:
            subprocess.call('rm {file}'.format(file=os.path.join(tex_dir,each_file)),shell=True)

    print '---------------------'
    print 'pdf mRNA report done!'
    print '---------------------'

def create_pdf_report(generate_report_path,part):
    '''
    param:a path where to your analysis's report data
    function:generate report tex file
    '''
    pdf_param_dict = {}
    pdf_param_dict.update(pdf_plots_size_dict)
    pdf_project_name = generate_report_path.rstrip('/').rsplit('/',1)[1].replace('_','\_')
    pdf_head_dict = dict(project_name=pdf_project_name,
                         report_name=pdf_settings['project_name'],
                         address=pdf_settings['address'],
                         phone=pdf_settings['phone'],
                         logo_path=pdf_settings['logo_path'],
                         pipeline_path=pdf_settings['pipeline_path'],
                         mRNAworkflow_path=pdf_settings['mRNAworkflow_path']
                          )
    pdf_param_dict.update(pdf_head_dict)
    #for all table
    ##enrichment part
    enrichment_analysis_path = pdf_analysis_path['enrichment']
    if os.path.exists(os.path.join(generate_report_path,mRNA_data_dict['enrichment'])):
        check_file(enrichment_analysis_path,generate_report_path,part)
        kegg_list = three_line_list(enrichment_analysis_path['kegg_table_path'],colunms=7)
        go_list = three_line_list(enrichment_analysis_path['go_table_path'],colunms=7)

        if enrichment_analysis_path['dag_bp_path'] and enrichment_analysis_path['dag_cc_path'] and enrichment_analysis_path['dag_mf_path']:
            dag_plots = True
        else:
            dag_plots = False

        enrichment_dict = dict(enrichment = 'enrichment',kegg_begin=kegg_list[0],
                                 kegg_head=kegg_list[1],kegg_body=kegg_list[2:],
                                 go_begin=go_list[0],go_head=go_list[1],go_body=go_list[2:],
                                 go_barplot_path=enrichment_analysis_path['go_barplot_path'],
                                 dag_plots=dag_plots,
                                 dag_bp_path=enrichment_analysis_path['dag_bp_path'],
                                 dag_cc_path=enrichment_analysis_path['dag_cc_path'],
                                 dag_mf_path=enrichment_analysis_path['dag_mf_path'],
                                 kegg_barplot_path=enrichment_analysis_path['kegg_barplot_path'],
                                 pathview_path=enrichment_analysis_path['pathview_path'],
                                 go_table_path=enrichment_analysis_path['go_table_path'],
                                 kegg_table_path=enrichment_analysis_path['kegg_table_path'])
    else:
        enrichment_dict = dict(enrichment = None)
        print '----------------------------------'
        print '-enrichment analysis part missing-'
        print '----------------------------------'
    pdf_param_dict.update(enrichment_dict)
    ##fastqc part
    fastqc_analysis_path = pdf_analysis_path['fastqc']
    if os.path.exists(os.path.join(generate_report_path,mRNA_data_dict['fastqc'])):
        check_file(fastqc_analysis_path,generate_report_path,part)
        qc_list = three_line_list(fastqc_analysis_path['qc_table_path'],colunms=6)
        fastqc_dict = dict(data_stat='data_stat',qc_begin=qc_list[0],qc_head=qc_list[1],qc_body=qc_list[2:],
                       gc_barplot_path=fastqc_analysis_path['gc_barplot_path'],
                       reads_quality_path=fastqc_analysis_path['reads_quality_path'],
                       qc_table_path=fastqc_analysis_path['qc_table_path']
                       )
    else:
        fastqc_dict = dict(data_stat = None)
        print '------------------------------'
        print '-fastqc analysis part missing-'
        print '------------------------------'
    pdf_param_dict.update(fastqc_dict)
    ##mapping part
    mapping_analysis_path = pdf_analysis_path['mapping']
    if os.path.exists(os.path.join(generate_report_path,mRNA_data_dict['mapping'])):
        check_file(mapping_analysis_path,generate_report_path,part)
        mapping_list = three_line_list(mapping_analysis_path['mapping_table_path'],colunms=7)
        mapping_dict = dict(mapping='mapping',mapping_begin=mapping_list[0],
                        mapping_head=mapping_list[1],mapping_body=mapping_list[2:],
                        mapping_plot_path=mapping_analysis_path['mapping_plot_path'],
                        mapping_table_path=mapping_analysis_path['mapping_table_path'])
    else:
        mapping_dict = dict(mapping = None)
        print '-------------------------------'
        print '-mapping analysis part missing-'
        print '-------------------------------'
    pdf_param_dict.update(mapping_dict)
    ##rseqc part
    rseqc_analysis_path = pdf_analysis_path['rseqc']
    if os.path.exists(os.path.join(generate_report_path,mRNA_data_dict['rseqc'])):
        check_file(rseqc_analysis_path,generate_report_path,part)
        rseqc_dict = dict(data_control='data_control',
                      genebody_coverage_plot_path=rseqc_analysis_path['genebody_coverage_plot_path'],
                      inner_distance_plot_path=rseqc_analysis_path['inner_distance_plot_path'],
                      read_distribution_plot_path=rseqc_analysis_path['read_distribution_plot_path'])
    else:
        rseqc_dict = dict(data_control = None)
        print '-----------------------------'
        print '-rseqc analysis part missing-'
        print '-----------------------------'
    pdf_param_dict.update(rseqc_dict)
    ##quantification part
    quantification_analysis_path = pdf_analysis_path['quantification']
    if os.path.exists(os.path.join(generate_report_path,mRNA_data_dict['quantification'])):
        check_file(quantification_analysis_path,generate_report_path,part)
        gene_count_list = three_line_list(quantification_analysis_path['gene_table_path'],colunms=6)
        quantification_dict = dict(quant='quant',
                               gene_count_begin=gene_count_list[0],
                               gene_count_head=gene_count_list[1],
                               gene_count_body=gene_count_list[2:],
                               correlation_heatmap_path=quantification_analysis_path['correlation_heatmap_path'],
                               gene_expression_path=quantification_analysis_path['gene_expression_path'],
                               pca_plot_path=quantification_analysis_path['pca_plot_path'],
                               gene_table_path=quantification_analysis_path['gene_table_path'])
        pdf_param_dict.update(quantification_dict)
        ##diff part
        diff_analysis_path = pdf_analysis_path['diff']
        check_file(diff_analysis_path,generate_report_path,part)
        diff_list = three_line_list(diff_analysis_path['diff_table_path'],colunms=5)
        diff_dict=dict(diff='diff',
                       diff_begin=diff_list[0],diff_head=diff_list[1],diff_body=diff_list[2:],
                       volcano_plot_path=diff_analysis_path['volcano_plot_path'],
                       diff_heatmap_path=diff_analysis_path['diff_heatmap_path'],
                       diff_table_path=diff_analysis_path['diff_table_path'])
        pdf_param_dict.update(diff_dict)
    else:
        quantification_dict = dict(quant = None)
        pdf_param_dict.update(quantification_dict)
        diff_dict = dict(diff = None)
        pdf_param_dict.update(diff_dict)
        print '-------------------------------------------'
        print '-quantification&diff analysis part missing-'
        print '-------------------------------------------'

    template = pdf_jinja_env.get_template('mRNA_base')
    pdf_template_path = os.path.join(generate_report_path,'analysis_report')

    if not os.path.exists(pdf_template_path):
        os.makedirs(pdf_template_path)
    #subprocess.call('cp main/pdf_templates/ref.bib {report_path}'.format(report_path=pdf_template_path))
    with open(os.path.join(pdf_template_path,'mRNA_report.tex'),'w+') as f:
        f.write(template.render(pdf_param_dict))
    print '-------------------------'
    print 'pdf report tex file done!'
    print '-------------------------'
    run_tex(tex_path=os.path.join(pdf_template_path,'mRNA_report.tex'))
