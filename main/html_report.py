#coding:UTF-8
'''
this is py2report's html_report moudle which a python script generate html mRNA report
this version only run on 34
log:
create by chencheng on 2017-05-05
add mapping and rseqc moudles on 2017-05-25
change report dir construction on 2017-06-08
import function for each part on 2017-06-10
add all function doc on 2017-06-16
'''
import os
import re
import sys
from . import mRNA_data_dict,mRNA_result_dict,html_jinja_env
reload(sys)
sys.setdefaultencoding('utf-8')

def check_modules(generate_report_path):
    '''
    param:
    generate_report_path:a path where to your analysis's report data
    function:check each analysis moudle whether its missing
    '''
    analysis_modules = dict(mapping='mapping',rseqc='rseqc',
                            quantification='quantification',
                            enrichment='enrichment',
                            fastqc='fastqc')
    for key,value in analysis_modules.items():
        if not os.path.exists(os.path.join(generate_report_path,mRNA_data_dict[value])):
            del analysis_modules[key]

    return analysis_modules


def get_multiple_plots(pattern_dict,generate_report_path,all_file):
    '''
    param:
    pattern_dict:each analysis part's plots pattern
    generate_report_path:a path where to your analysis's report data
    all_file:all analysis part's paths(plots path)
    function:link report data's path when generate each analysis moudle
    '''
    multiple_plot_path = dict.fromkeys(pattern_dict.keys())
    for key,value in multiple_plot_path.items():
        multiple_plot_path[key] = [file.replace(os.path.join(generate_report_path,'analysis_report'),'..') for file in all_file if re.search(pattern_dict[key],file.rsplit('/',1)[1])]
    return multiple_plot_path

def table2list(table_path,header=True,split='\t',max_row_num = 30,max_col_num = 100,max_cell_num = 15):
    '''
    param:
    table_path:each analysis part's table path
    other params:threshold values for control table
    function:transform table to list
    '''
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

def enrichment_analysis(generate_report_path,analysis_modules):
    '''
    param:
    generate_report_path:a path where to your analysis's report data
    analysis_modules:a dict for mRNA report exists analysis moudles
    function:create enrichment analysis moudle
    '''
    enrichment_path = os.path.join(generate_report_path,mRNA_data_dict['enrichment'])
    if not os.path.exists(enrichment_path):
        print "enrichment analysis part missing"
        return
    go_list = table2list(os.path.join(enrichment_path,'report.go.table.txt'))
    kegg_list = table2list(os.path.join(enrichment_path,'report.kegg.table.txt'))
    sample_num = len(os.listdir(os.path.join(enrichment_path,'go')))

    all_file = []
    for root,dirs,files in os.walk(enrichment_path):
            all_file.extend([os.path.join(root,file) for file in files])

    multiple_plot_pattern = dict(go_barplots='go.enrichment.barplot.png$',
                              kegg_barplots='kegg.enrichment.barplot.png$',
                              dag_plots='ALL.CC.GO.DAG.png$',
                              pathway_plots='.pathview.png$')

    multiple_plot_path = get_multiple_plots(multiple_plot_pattern,generate_report_path,all_file)
    multiple_plot_path['pathway_plots'] = multiple_plot_path['pathway_plots'][:sample_num] #cut much more pathway plots

    go_href = os.path.join(mRNA_result_dict['enrichment'],'go').replace(generate_report_path,'../..')
    kegg_href = os.path.join(mRNA_result_dict['enrichment'],'kegg').replace(generate_report_path,'../..')
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
		go_table_path = go_href,
		kegg_table_path = kegg_href,
		all_go_enrichment_plot_dir = kegg_href,
		all_dag_plot_dir = go_href,
		all_kegg_enrichment_plot_dir = kegg_href,
		all_kegg_pathway_plot_dir = kegg_href,
        fastqc = analysis_modules.get('fastqc'),
        mapping = analysis_modules.get('mapping'),
        rsqec = analysis_modules.get('rsqec'),
        quantification = analysis_modules.get('quantification'),
		))
    print 'enrichment analysis page done!'

def fastqc_analysis(generate_report_path,analysis_modules):
    '''
    generate_report_path:a path where to your analysis's report data
    analysis_modules:a dict for mRNA report exists analysis moudles
    function:create fastqc analysis moudle
    '''
    fastqc_path = os.path.join(generate_report_path,mRNA_data_dict['fastqc'])
    if not os.path.exists(fastqc_path):
        print "fastqc analysis part missing"
        return
    qc_list = table2list(os.path.join(fastqc_path,'fastqc_general_stats.txt'))

    all_file = []
    for root,dirs,files in os.walk(fastqc_path):
            all_file.extend([os.path.join(root,file) for file in files])

    multiple_plot_pattern = dict(gc_plots='.gc_distribution.line.png$',
                                 reads_quality_plots='.reads_quality.bar.png$')

    multiple_plot_path = get_multiple_plots(multiple_plot_pattern,generate_report_path,all_file)
    fastqc_stat_href = mRNA_result_dict['fastqc'].replace(generate_report_path,'../..')
    gc_plot_href = os.path.join(mRNA_result_dict['fastqc'],'gc_plot').replace(generate_report_path,'../..')
    reads_quality_href = os.path.join(mRNA_result_dict['fastqc'],'reads_quality_plot').replace(generate_report_path,'../..')

    html_template_path = os.path.join(generate_report_path,'analysis_report','templates')
    if not os.path.exists(html_template_path):
        os.makedirs(html_template_path)
    #render fastqc templates:
    template = html_jinja_env.get_template('data_stat.html')
    with open(os.path.join(html_template_path,'rendered_data_stat.html'),'w+') as f:
        f.write(template.render(title = '数据统计',
        header=qc_list[0],qc_table=qc_list[1],
        all_quality_data_barplot_path=multiple_plot_path['reads_quality_plots'],
        all_gc_plot_path=multiple_plot_path['gc_plots'],
        qc_table_path=fastqc_stat_href,
        quality_barplot_dir=reads_quality_href,
        gc_plot_dir=gc_plot_href,
        mapping=analysis_modules.get('mapping'),
        rseqc=analysis_modules.get('rseqc'),
        quantification=analysis_modules.get('quantification'),
        enrichment=analysis_modules.get('enrichment')
        ))
    print 'fastqc analysis page done!'

def mapping_analysis(generate_report_path,analysis_modules):
    '''
    generate_report_path:a path where to your analysis's report data
    analysis_modules:a dict for mRNA report exists analysis moudles
    function:create mapping analysis moudle
    '''
    mapping_path = os.path.join(generate_report_path,mRNA_data_dict['mapping'])
    if not os.path.exists(mapping_path):
        print "mapping analysis part missing"
        return
    mapping_list = table2list(os.path.join(mapping_path,'mapping_stats.txt'))
    mapping_stats_plot = os.path.join(mapping_path,'mapping_stats_plot.png').replace(os.path.join(generate_report_path,'analysis_report'),'..')
    mapping_href = mRNA_result_dict['mapping'].replace(generate_report_path,'../..')
    html_template_path = os.path.join(generate_report_path,'analysis_report','templates')
    if not os.path.exists(html_template_path):
        os.makedirs(html_template_path)
    #render mapping templates:
    template = html_jinja_env.get_template('mapping.html')
    with open(os.path.join(html_template_path,'rendered_mapping.html'),'w+') as f:
    		f.write(template.render(title = '序列对比',
    		header=mapping_list[0],mapping_table=mapping_list[1],
    		mapping_stat_plot_path = mapping_stats_plot,
    		mapping_table_path=mapping_href,
    		mapping_stat_plot_dir=mapping_href,
            fastqc=analysis_modules.get('fastqc'),
            rsqec=analysis_modules.get('rsqec'),
            quantification=analysis_modules.get('quantification'),
            enrichment=analysis_modules.get('enrichment')
    		))
    print 'mapping analysis page done!'

def quantification_analysis(generate_report_path,analysis_modules):
    '''
    generate_report_path:a path where to your analysis's report data
    analysis_modules:a dict for mRNA report exists analysis moudles
    function:create quantification&diff analysis moudle
    '''
    quantification_path = os.path.join(generate_report_path,mRNA_data_dict['quantification'])
    if not os.path.exists(quantification_path):
        print "quantification analysis part missing"
        return
    expression_summary_dir = os.path.join(quantification_path,'expression_summary')
    diff_analysis_dir = os.path.join(quantification_path,'differential_analysis')

    gene_count_list = table2list(os.path.join(expression_summary_dir,'Gene.tpm.txt'))
    diff_list = table2list(os.path.join(expression_summary_dir,'html.example.diff.table.txt'))

    expression_summary_plots = {'pca_plot':'PCA_plot.png','diff_heatmap_plot':'Diff.genes.heatmap.png',
                                'correlation_heatmap_plot':'Sample.correlation.heatmap.png','gene_expression_plot':'Gene_expression.png'}
    for key,value in expression_summary_plots.items():
        expression_summary_plots[key] = os.path.join(expression_summary_dir,value).replace(os.path.join(generate_report_path,'analysis_report'),'..')

    all_file = []
    for root,dirs,files in os.walk(diff_analysis_dir):
            all_file.extend([os.path.join(root,file) for file in files])

    multiple_plot_pattern = dict(volcano_plots='.Volcano_plot.png$')
    multiple_plot_path = get_multiple_plots(multiple_plot_pattern,generate_report_path,all_file)
    expression_summary_href = os.path.join(mRNA_result_dict['quantification'],'expression_summary').replace(generate_report_path,'../..')
    diff_analysis_href = os.path.join(mRNA_result_dict['quantification'],'differential_analysis').replace(generate_report_path,'../..')
    #render quant&diff templates
    html_template_path = os.path.join(generate_report_path,'analysis_report','templates')
    if not os.path.exists(html_template_path):
        os.makedirs(html_template_path)
    quant_template = html_jinja_env.get_template('quantitative_analysis.html')
    with open(os.path.join(html_template_path,'rendered_quantitative_analysis.html'),'w+') as f:
        f.write(quant_template.render(title = '定量分析',
        header=gene_count_list[0],gene_count_table = gene_count_list[1],
        Gene_merge_plot_path = expression_summary_plots['gene_expression_plot'],
        sample_correlation_plot_path = expression_summary_plots['correlation_heatmap_plot'],
        PCA_plot_path = expression_summary_plots['pca_plot'],
        gene_count_table_path=expression_summary_href,
        gene_merge_plot_dir=expression_summary_href,
        sample_correlation_plot_dir=expression_summary_href,
        PCA_plot_dir=expression_summary_href,
        fastqc=analysis_modules.get('fastqc'),
        mapping=analysis_modules.get('mapping'),
        rseqc=analysis_modules.get('rseqc'),
        enrichment=analysis_modules.get('enrichment')
        ))
    print 'quantification analysis page done!'
    diff_template = html_jinja_env.get_template('diff_analysis.html')
    with open(os.path.join(html_template_path,'rendered_diff_analysis.html'),'w+') as f:
		f.write(diff_template.render(title = '差异分析',
		header=diff_list[0],diff_table=diff_list[1],
		all_volcano_plot_path = multiple_plot_path['volcano_plots'],
		diff_heatmap_plot_path = expression_summary_plots['diff_heatmap_plot'],
		diff_table_path = expression_summary_href,
		all_volcano_plot_dir = diff_analysis_href,
		diff_heatmap_plot_dir = expression_summary_href,
        fastqc=analysis_modules.get('fastqc'),
        mapping=analysis_modules.get('mapping'),
        rsqec=analysis_modules.get('rsqec'),
        enrichment=analysis_modules.get('enrichment')
		))
    print 'diff analysis page done!'

def rseqc_analysis(generate_report_path,analysis_modules):
    '''
    generate_report_path:a path where to your analysis's report data
    analysis_modules:a dict for mRNA report exists analysis moudles
    function:create rseqc analysis moudle
    '''
    rseqc_path = os.path.join(generate_report_path,mRNA_data_dict['rseqc'])
    if not os.path.exists(rseqc_path):
        print "rseqc analysis part missing"
        return

    all_file = []
    for root,dirs,files in os.walk(rseqc_path):
        all_file.extend([os.path.join(root,file) for file in files])

    multiple_plot_pattern = dict(read_duplication='.reads_duplication.point.png$',
                                  read_distribution='.read_distribution.pie.png$',
                                  inner_distance='.inner_distance.bar.png$',
                                  genebody_coverage='.genebody_coverage.point.png$')

    multiple_plot_path = get_multiple_plots(multiple_plot_pattern,generate_report_path,all_file)

    read_duplication_href = os.path.join(mRNA_result_dict['rseqc'],'read_duplication').replace(generate_report_path,'../..')
    read_distribution_href = os.path.join(mRNA_result_dict['rseqc'],'read_distribution').replace(generate_report_path,'../..')
    inner_distance_href = os.path.join(mRNA_result_dict['rseqc'],'inner_distance').replace(generate_report_path,'../..')
    genebody_coverage_href = os.path.join(mRNA_result_dict['rseqc'],'genebody_coverage').replace(generate_report_path,'../..')

    html_template_path = os.path.join(generate_report_path,'analysis_report','templates')
    if not os.path.exists(html_template_path):
        os.makedirs(html_template_path)
    #render rseqc templates
    template = html_jinja_env.get_template('rseqc.html')
    with open(os.path.join(html_template_path,'rendered_rseqc.html'),'w+') as f:
    		f.write(template.render(title = '数据质控',
    		inner_distance_plot_path = multiple_plot_path['inner_distance'],
    		read_duplication_plot_path = multiple_plot_path['read_duplication'],
    		genebody_coverage_plot_path = multiple_plot_path['genebody_coverage'],
    		read_distrbution_plot_path = multiple_plot_path['read_distribution'],
    		inner_distance_plot_dir=inner_distance_href,
    		read_duplication_plot_dir=read_duplication_href,
    		genebody_coverage_plot_dir=genebody_coverage_href,
    		read_distrbution_plot_dir=read_distribution_href,
            fastqc=analysis_modules.get('fastqc'),
            mapping=analysis_modules.get('mapping'),
            quantification=analysis_modules.get('quantification'),
            enrichment=analysis_modules.get('enrichment')
    		))
    print 'rseqc analysis page done!'


def create_main_page_nav(generate_report_path,analysis_modules):
    '''
    generate_report_path:a path where to your analysis's report data
    analysis_modules:a dict for mRNA report exists analysis moudles
    '''
    html_template_path = os.path.join(generate_report_path,'analysis_report')
    if not os.path.exists(html_template_path):
        os.makedirs(html_template_path)
    template = html_jinja_env.get_template('mRNA_report.html')
    with open(os.path.join(html_template_path,'mRNA_report.html'),'w+') as f:
    		f.write(template.render(
            fastqc=analysis_modules.get('fastqc'),
            mapping=analysis_modules.get('mapping'),
            quantification=analysis_modules.get('quantification'),
            rsqec=analysis_modules.get('rsqec'),
            enrichment=analysis_modules.get('enrichment')
            ))
    print 'mRNA report main page done!'
