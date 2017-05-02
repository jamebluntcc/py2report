# encoding:utf-8
import os
import re
import sys
import glob
import jinja2
import argparse
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

html_jinja_env = jinja2.Environment(
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.join(os.path.abspath('.'),'html_templates'))
)

def table2list(table_path,header=True,split='\t',max_row_num = 50,max_col_num = 8,max_cell_num = 50):
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

def mRNA_dir_map(mRNA_report_dir):
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
    go_dagplot_dir = target_dir['GO_dag_plot$']
    go_enrichtable_dir = target_dir['GO_enrich_table$']
    kegg_barplot_dir = target_dir['KEGG_bar_plot$']
    kegg_enrichtable_dir = target_dir['KEGG_enrich_table$']
    kegg_pathway_dir = target_dir['KEGG_pathway$']

    mRNA_report_dir_info = {'difftable_dir': difftable_dir, 'volcano_plot_dir': volcano_plot_dir,
                            'heatmap_dir': heatmap_dir, 'go_barplot_dir': go_barplot_dir,
                            'kegg_barplot_dir': kegg_barplot_dir, 'go_dagplot_dir': go_dagplot_dir,
                            'go_enrichtable_dir': go_enrichtable_dir,
                            'kegg_enrichtable_dir': kegg_enrichtable_dir, 'kegg_pathway_dir': kegg_pathway_dir}

    return mRNA_report_dir_info

def find_sample_file(target_dir,pattern):
	sample_dir = os.listdir(target_dir)[0]
	target_file = glob.glob(os.path.join(target_dir,sample_dir,pattern))
	if len(target_file) == 1:
		return target_file[0]
	print 'try another pattern in {dir}'.format(dir=os.path.join(target_dir,sample_dir))
	sys.exit(1)

def create_multiple_plot_list(plot_dir,pattern='*.png',max_plot_num = 8,dir_type = None):
	plot_path_list = []
	if dir_type == 'kegg_pathway':
		for each_dir in os.listdir(plot_dir):
			target_file = glob.glob(os.path.join(plot_dir,each_dir,'ALL_pathway',pattern))
			plot_path_list.extend(target_file)
	else:
		for each_dir in os.listdir(plot_dir):
			target_file = glob.glob(os.path.join(plot_dir,each_dir,pattern))
			plot_path_list.extend(target_file)

	if len(plot_path_list) == 0:
		print plot_path_list
		print 'plot path is None in {dir}'.format(dir=plot_dir)
		sys.exit(1)
	elif len(plot_path_list) < max_plot_num:
		return plot_path_list
	else:
		return plot_path_list[:max_plot_num]

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'a script to create html mRNA analysis report')
	parser.add_argument('mRNA_report_path',help='a dir where include your mRNA analysis results')
	args = parser.parse_args()

	mRNA_report_dir = os.path.abspath(args.mRNA_report_path)
	mRNA_report_dir_str = 'mRNA_analysis_results'
	replace_dir = mRNA_report_dir.split(mRNA_report_dir_str)[0]
	###for table
	#qc
	qc_dir = os.path.join(mRNA_report_dir,'qc')
	qc_file = os.path.join(qc_dir,'qc.summary.txt')
	qc_list = table2list(qc_file)
	#quantification
	quantification_dir = os.path.join(mRNA_report_dir, 'quantification')
	gene_count_table = os.path.join(quantification_dir, 'Gene.tpm.xls')
	gene_count_list = table2list(gene_count_table)

	mRNA_report_dir_info = mRNA_dir_map(mRNA_report_dir)
	diff_table = find_sample_file(mRNA_report_dir_info['difftable_dir'],pattern = '*DE_results.txt')
	go_table = find_sample_file(mRNA_report_dir_info['go_enrichtable_dir'],pattern = '*ALL.GO.enrich.xls')
	kegg_table = find_sample_file(mRNA_report_dir_info['kegg_enrichtable_dir'],pattern = '*ALL.KEGG.enrich.xls')

	diff_list = table2list(diff_table)
	go_list = table2list(go_table)
	kegg_list = table2list(kegg_table)

	###for plot
	#for single_plot
	gene_merge_plot_path = '/'.join(['..',mRNA_report_dir_str,'quantification','gene_merge_plot.png'])
	sample_correlation_plot_path = '/'.join(['..',mRNA_report_dir_str,'quantification','sample_correlation.plot.png'])
	PCA_plot_path = '/'.join(['..',mRNA_report_dir_str,'quantification','PCA_plot.png'])
	diff_heatmap_plot_path = '/'.join(['..',mRNA_report_dir_str,'differential_analysis','heatmap','Heatmap.png'])

	plot_dict = {'gene_merge_plot_path':gene_merge_plot_path,
				 'sample_correlation_plot_path':sample_correlation_plot_path,
				 'PCA_plot_path':PCA_plot_path,'diff_heatmap_plot_path':diff_heatmap_plot_path}

	#for multiple plot
	multiple_plot_dict = dict.fromkeys(['quality_barplot_dir','volcano_plot_dir','go_barplot_dir',
										'go_dagplot_dir','kegg_barplot_dir','kegg_pathway_dir'])

	quality_barplot_path_list = glob.glob(os.path.join(qc_dir,'reads_quality','*_reads_quality_barplot.png'))
	multiple_plot_dict['quality_barplot_dir'] = quality_barplot_path_list

	for plot_dir in ['volcano_plot_dir','go_barplot_dir','go_dagplot_dir','kegg_barplot_dir','kegg_pathway_dir']:
		if plot_dir == 'kegg_pathway_dir':
			multiple_plot_dict[plot_dir] = create_multiple_plot_list(mRNA_report_dir_info[plot_dir],dir_type = 'kegg_pathway')
		else:
			multiple_plot_dict[plot_dir] = create_multiple_plot_list(mRNA_report_dir_info[plot_dir])

	for key,value in multiple_plot_dict.items():
		multiple_plot_dict[key] = [k.replace(replace_dir,'../') for k in value]

	plot_dict.update(multiple_plot_dict)
	### render template
	#data_control page:
	prject_templates_dir = os.path.join(replace_dir,'templates')
	if not os.path.exists(prject_templates_dir):
		os.makedirs(prject_templates_dir)

	template = html_jinja_env.get_template('data_control.html')
	with open(os.path.join(prject_templates_dir,'rendered_data_control.html'),'w+') as f:
		f.write(template.render(title = '数据质控',
		header=qc_list[0],qc_table=qc_list[1],
		all_quality_data_barplot_path = plot_dict['quality_barplot_dir']))
	#quantitative_analysis
	template = html_jinja_env.get_template('quantitative_analysis.html')
	with open(os.path.join(prject_templates_dir,'rendered_quantitative_analysis.html'),'w+') as f:
		f.write(template.render(title = '定量分析',
		header=gene_count_list[0],gene_count_table = gene_count_list[1],
		Gene_merge_plot_path = plot_dict['gene_merge_plot_path'],
		sample_correlation_plot_path = plot_dict['sample_correlation_plot_path'],
		PCA_plot_path = plot_dict['PCA_plot_path']))
	#diff_analysis:
	template = html_jinja_env.get_template('diff_analysis.html')
	with open(os.path.join(prject_templates_dir,'rendered_diff_analysis.html'),'w+') as f:
		f.write(template.render(title = '差异分析',
		header=diff_list[0],diff_table=diff_list[1],
		all_volcano_plot_path = plot_dict['volcano_plot_dir'],
		diff_heatmap_plot_path = plot_dict['diff_heatmap_plot_path']))
	#enrichment_analysis:
	template = html_jinja_env.get_template('enrichment_analysis.html')
	with open(os.path.join(prject_templates_dir,'rendered_enrichment_analysis.html'),'w+') as f:
		f.write(template.render(title = '富集分析',
		go_header=go_list[0],go_enrichment_table=go_list[1],
		all_go_enrichment_plot_path = plot_dict['go_barplot_dir'],
		all_dag_plot_path = plot_dict['go_dagplot_dir'],
		kegg_header = kegg_list[0],kegg_enrichment_table = kegg_list[1],
		all_kegg_enrichment_plot_path = plot_dict['kegg_barplot_dir'],
		all_kegg_pathway_plot_path = plot_dict['kegg_pathway_dir']))

	pwd = os.getcwd()
	os.chdir(replace_dir)
	#print replace_dir
	#print os.path.join(pwd,'static')
	subprocess.call('cp -r {static_file} ./'.format(static_file = os.path.join(pwd,'static')),shell = True)
	subprocess.call('cp -r {main_file} ./'.format(main_file = os.path.join(pwd,'mRNA_report.html')),shell = True)

	subprocess.call('echo ------------------------',shell = True)
	subprocess.call('echo -mRNA html report done!-',shell = True)
	subprocess.call('echo ------------------------',shell = True)
