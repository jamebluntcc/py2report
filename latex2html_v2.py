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

def table2list(table_path,header=True,split='\t',max_row_num = 30,max_col_num = 5,max_cell_num = 15):
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

def find_sample_file(target_dir,pattern,action = None):
	sample_dir = os.listdir(target_dir)[0] #return first sample
	if action:
		new_pattern = '.'.join([sample_dir,pattern])
		target_file = glob.glob(os.path.join(target_dir,sample_dir,new_pattern))
	else:
		target_file = glob.glob(os.path.join(target_dir,sample_dir,pattern))
	if len(target_file) == 1:
		return target_file[0]
	print target_file
	print 'try another pattern:{pattern} in {dir} by {function}'.format(pattern = pattern,dir=os.path.join(target_dir,sample_dir),function='find_sample_file')
	sys.exit(1)

def find_plot_path_list(plot_dir,pattern,plot_type=''):
	sample_list = os.listdir(plot_dir)
	#print sample_list
	plot_path_list = []
	if plot_type == 'DAG':
		if len(sample_list) == 1:
			target_path = glob.glob(os.path.join(plot_dir,sample_list[0],'DAG',pattern))[:5]
			plot_path_list.extend(target_path)
		else:
			for each_sample in sample_list:
				target_path = glob.glob(os.path.join(plot_dir,each_sample,'DAG',pattern))[0]
				plot_path_list.append(target_path)
		if len(plot_path_list) == 0:
			print 'try another pattern:{pattern} for DAG:{dir} by {function}'.format(pattern=pattern,dir=plot_dir,function='find_plot_path_list')
			sys.exit(1)
	elif plot_type == 'pathway':
		if len(sample_list) == 1:
			target_path = glob.glob(os.path.join(plot_dir,sample_list[0],'*.ALL.pathway',pattern))[:5]
			plot_path_list.extend(target_path)
		else:
			for each_sample in sample_list:
				target_path = glob.glob(os.path.join(plot_dir,each_sample,'*.ALL.pathway',pattern))[0]
				plot_path_list.append(target_path)
		if len(plot_path_list) == 0:
			print 'try another pattern:{pattern} for pathway:{dir} by {function}'.format(pattern=pattern,dir=plot_dir,function='find_plot_path_list')
			sys.exit(1)
	else:
		for each_sample in sample_list:
			target_path = glob.glob(os.path.join(plot_dir,each_sample,pattern))
			#print target_path
			if len(target_path) == 1:
				plot_path_list.append(target_path[0])
			else:
				print target_path
				print 'try another pattern:{pattern} in {dir} by {function}'.format(pattern=pattern,dir=os.path.join(plot_dir,each_sample),function='find_plot_path_list')
				sys.exit(1)

	return plot_path_list

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'a script to create html mRNA analysis report')
	parser.add_argument('mRNA_report_path',help='a dir where include your mRNA analysis results')
	args = parser.parse_args()

	mRNA_report_dir = os.path.abspath(args.mRNA_report_path)
	replace_dir = mRNA_report_dir.rstrip('/').rsplit('/',1)[0]
	###for table
	#fastqc
	qc_dir = os.path.join(mRNA_report_dir,'fastqc')
	qc_file = os.path.join(qc_dir,'fastqc_general_stats.txt')
	qc_list = table2list(qc_file)
	#quantification
	quantification_dir = os.path.join(mRNA_report_dir, 'quantification')
	differential_analysis_dir = os.path.join(quantification_dir,'differential_analysis')
	expression_summary_dir = os.path.join(quantification_dir,'expression_summary')

	gene_count_table = os.path.join(expression_summary_dir, 'Gene.tpm.txt')
	gene_count_list = table2list(gene_count_table)
	diff_table = find_sample_file(differential_analysis_dir,pattern = 'edgeR.DE_results.txt',action = 'diff_table')
	#enrichment
	enrichment_dir = os.path.join(mRNA_report_dir,'enrichment')
	go_dir = os.path.join(enrichment_dir,'go')
	kegg_dir = os.path.join(enrichment_dir,'kegg')
	go_table = find_sample_file(go_dir,pattern = '*ALL.go.enrichment.txt')
	kegg_table = find_sample_file(kegg_dir,pattern = '*ALL.kegg.enrichment.txt')

	diff_list = table2list(diff_table)
	go_list = table2list(go_table)
	kegg_list = table2list(kegg_table)
	#write all table path into template
	all_table_path = {'qc_table':qc_file,'gene_count_table':gene_count_table,'diff_table':diff_table,
					  'go_table':go_table,'kegg_table':kegg_table}
	for key,value in all_table_path.items():
		all_table_path[key] = value.replace(replace_dir,'..')
	###for plot
	#for single_plot
	gene_merge_plot_path = os.path.join(expression_summary_dir,'Gene_expression.png')
	sample_correlation_plot_path = os.path.join(expression_summary_dir,'Sample.correlation.heatmap.png')
	PCA_plot_path = os.path.join(expression_summary_dir,'PCA_plot.png')
	diff_heatmap_plot_path = os.path.join(expression_summary_dir,'Diff.genes.heatmap.png')

	plot_dict = {'gene_merge_plot_path':gene_merge_plot_path,
				 'sample_correlation_plot_path':sample_correlation_plot_path,
				 'PCA_plot_path':PCA_plot_path,'diff_heatmap_plot_path':diff_heatmap_plot_path}

	for key,value in plot_dict.items():
		plot_dict[key] = value.replace(replace_dir,'..')
	#for multiple plot
	multiple_plot_dict = dict.fromkeys(['quality_barplot_dir','volcano_plot_dir','go_barplot_dir',
										'go_dagplot_dir','kegg_barplot_dir','kegg_pathway_dir'])

	quality_barplot_path_list = glob.glob(os.path.join(qc_dir,'reads_quality_plot','*.reads_quality.png'))
	#print quality_barplot_path_list
	multiple_plot_dict['quality_barplot_dir'] = quality_barplot_path_list

	volcano_plot_path_list = find_plot_path_list(differential_analysis_dir,pattern='*.Volcano_plot.png')
	go_barplot_path_list = find_plot_path_list(go_dir,pattern = '*.go.enrichment.barplot.png')
	go_dag_plot_path_list = find_plot_path_list(go_dir,pattern = '*.GO.DAG.png',plot_type = 'DAG')
	kegg_barplot_path_list = find_plot_path_list(kegg_dir,pattern = '*.kegg.enrichment.barplot.png')
	kegg_pathway_path_list = find_plot_path_list(kegg_dir,pattern = '*.pathview.png',plot_type = 'pathway')

	multiple_plot_dict['volcano_plot_dir'] = volcano_plot_path_list
	multiple_plot_dict['go_barplot_dir'] = go_barplot_path_list
	multiple_plot_dict['go_dagplot_dir'] = go_dag_plot_path_list
	multiple_plot_dict['kegg_barplot_dir'] = kegg_barplot_path_list
	multiple_plot_dict['kegg_pathway_dir'] = kegg_pathway_path_list

	for key,value in multiple_plot_dict.items():
		multiple_plot_dict[key] = [k.replace(replace_dir,'..') for k in value]

	plot_dict.update(multiple_plot_dict)
	#check plot empty
	for key,value in multiple_plot_dict.items():
		if len(value) == 0:
			print 'plot in {plot_path} is empty!'.format(plot_path=key)
			sys.exit(1)

	### render template
	#data_control page:
	prject_templates_dir = os.path.join(replace_dir,'templates')
	if not os.path.exists(prject_templates_dir):
		os.makedirs(prject_templates_dir)

	template = html_jinja_env.get_template('data_control.html')
	with open(os.path.join(prject_templates_dir,'rendered_data_control.html'),'w+') as f:
		f.write(template.render(title = '数据质控',
		header=qc_list[0],qc_table=qc_list[1],
		all_quality_data_barplot_path = plot_dict['quality_barplot_dir'],
		qc_table_path=all_table_path['qc_table'],
		quality_barplot_dir=plot_dict['quality_barplot_dir'][0].rsplit('/',1)[0]
		))
	#quantitative_analysis
	template = html_jinja_env.get_template('quantitative_analysis.html')
	with open(os.path.join(prject_templates_dir,'rendered_quantitative_analysis.html'),'w+') as f:
		f.write(template.render(title = '定量分析',
		header=gene_count_list[0],gene_count_table = gene_count_list[1],
		Gene_merge_plot_path = plot_dict['gene_merge_plot_path'],
		sample_correlation_plot_path = plot_dict['sample_correlation_plot_path'],
		PCA_plot_path = plot_dict['PCA_plot_path'],
		gene_count_table_path=all_table_path['gene_count_table'],
		gene_merge_plot_dir=expression_summary_dir.replace(replace_dir,'..'),
		sample_correlation_plot_dir=expression_summary_dir.replace(replace_dir,'..'),
		PCA_plot_dir=expression_summary_dir.replace(replace_dir,'..')
		))
	#diff_analysis:
	template = html_jinja_env.get_template('diff_analysis.html')
	with open(os.path.join(prject_templates_dir,'rendered_diff_analysis.html'),'w+') as f:
		f.write(template.render(title = '差异分析',
		header=diff_list[0],diff_table=diff_list[1],
		all_volcano_plot_path = plot_dict['volcano_plot_dir'],
		diff_heatmap_plot_path = plot_dict['diff_heatmap_plot_path'],
		diff_table_path = all_table_path['diff_table'],
		all_volcano_plot_dir = plot_dict['volcano_plot_dir'][0].rsplit('/',1)[0],
		diff_heatmap_plot_dir = expression_summary_dir.replace(replace_dir,'..')
		))
	#enrichment_analysis:
	template = html_jinja_env.get_template('enrichment_analysis.html')
	with open(os.path.join(prject_templates_dir,'rendered_enrichment_analysis.html'),'w+') as f:
		f.write(template.render(title = '富集分析',
		go_header=go_list[0],go_enrichment_table=go_list[1],
		all_go_enrichment_plot_path = plot_dict['go_barplot_dir'],
		all_dag_plot_path = plot_dict['go_dagplot_dir'],
		kegg_header = kegg_list[0],kegg_enrichment_table = kegg_list[1],
		all_kegg_enrichment_plot_path = plot_dict['kegg_barplot_dir'],
		all_kegg_pathway_plot_path = plot_dict['kegg_pathway_dir'],
		go_table_path = all_table_path['go_table'],
		kegg_table_path = all_table_path['kegg_table'],
		all_go_enrichment_plot_dir = plot_dict['go_barplot_dir'][0].rsplit('/',1)[0],
		all_dag_plot_dir = plot_dict['go_dagplot_dir'][0].rsplit('/',1)[0],
		all_kegg_enrichment_plot_dir = plot_dict['kegg_barplot_dir'][0].rsplit('/',1)[0],
		all_kegg_pathway_plot_dir = plot_dict['kegg_pathway_dir'][0].rsplit('/',1)[0]
		))

	pwd = os.getcwd()
	os.chdir(replace_dir)
	#print replace_dir
	#print os.path.join(pwd,'static')
	subprocess.call('cp -r {static_file} ./'.format(static_file = os.path.join(pwd,'static')),shell = True)
	subprocess.call('cp -r {main_file} ./'.format(main_file = os.path.join(pwd,'mRNA_report.html')),shell = True)

	subprocess.call('echo ------------------------',shell = True)
	subprocess.call('echo -mRNA html report done!-',shell = True)
	subprocess.call('echo ------------------------',shell = True)
