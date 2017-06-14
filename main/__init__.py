#coding:UTF-8
import os
import jinja2
from copy import deepcopy
import configparser
'''
init html and pdf configure
'''
#template env config
html_jinja_env = jinja2.Environment(
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'html_templates'))
)
pdf_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'pdf_templates'))
)

##################
######html version
##################

#add each analysis part
configFilePath = os.path.join(os.path.dirname(__file__),'report_conf.conf')
command = configparser.ConfigParser()
command.read(configFilePath)
#all path
mRNA_data_path = command.get('mRNA-report-data','report_data_path')
mRNA_result_path = command.get('mRNA-report-result','report_result_path')
enrichment_path = command.get('mRNA-path','enrichment_path')
fastqc_path = command.get('mRNA-path','fastqc_path')
mapping_path = command.get('mRNA-path','mapping_path')
quantification_path = command.get('mRNA-path','quantification_path')
rseqc_path = command.get('mRNA-path','rseqc_path')
#pdf settings
address = command.get('mRNA-pdf-info','address')
phone = command.get('mRNA-pdf-info','phone')
table_rows = command.get('mRNA-pdf-info','table_rows')
max_cell_len = command.get('mRNA-pdf-info','max_cell_len')
project_name = command.get('mRNA-pdf-info','project_name')
logo_path =  command.get('mRNA-pdf-static-34','logo_path')
pipeline_path =  command.get('mRNA-pdf-static-34','pipeline_path')
mRNAworkflow_path =  command.get('mRNA-pdf-static-34','mRNAworkflow_path')

mRNA_data_dict = dict(enrichment=enrichment_path,fastqc=fastqc_path,
					  mapping=mapping_path,quantification=quantification_path,
					  rseqc=rseqc_path)
for key,value in mRNA_data_dict.items():
	mRNA_data_dict[key] = os.path.join(mRNA_data_path,value)

mRNA_result_dict = deepcopy(mRNA_data_dict)
for key,value in mRNA_result_dict.items():
	mRNA_result_dict[key] = os.path.join(mRNA_result_path,value)

#################
######pdf version
#################

##enrichment part
enrichment_analysis_path = dict(go_barplot_path='go.enrichment.barplot.png',
							    kegg_barplot_path='kegg.enrichment.barplot.png',
								pathview_path='kegg.pathview.png',dag_bp_path='BP.GO.DAG.png',
								dag_cc_path='CC.GO.DAG.png',dag_mf_path='MF.GO.DAG.png',
								go_table_path='report.go.table.txt',kegg_table_path='report.kegg.table.txt')

for key,value in enrichment_analysis_path.items():
	enrichment_analysis_path[key] = os.path.join(mRNA_data_path,enrichment_path,value)
##fastqc part
fastqc_analysis_path = dict(gc_barplot_path = 'gc_plot/gc_distribution.line.png',
							reads_quality_path = 'reads_quality_plot/reads_quality.bar.png',
							qc_table_path='fastqc_general_stats.txt')

for key,value in fastqc_analysis_path.items():
	fastqc_analysis_path[key] = os.path.join(mRNA_data_path,fastqc_path,value)
##mapping part
mapping_analysis_path = dict(mapping_table_path='mapping_stats.txt',mapping_plot_path='mapping_stats_plot.png')

for key,value in mapping_analysis_path.items():
	mapping_analysis_path[key] = os.path.join(mRNA_data_path,mapping_path,value)
##quantification part
expression_summary_dir = 'expression_summary'
quantification_analysis_path = dict(
									correlation_heatmap_path='Sample.correlation.heatmap.png',
									gene_expression_path='Gene_expression.png',
									pca_plot_path='PCA_plot.png',
									gene_table_path='pdf.example.Gene.tpm.txt',
									)

for key,value in quantification_analysis_path.items():
	quantification_analysis_path[key] = os.path.join(mRNA_data_path,quantification_path,expression_summary_dir,value)
##diff part
diff_analysis_path = dict(volcano_plot_path='ALL.Volcano_plot.png',
						  diff_heatmap_path='Diff.genes.heatmap.png',
						  diff_table_path='pdf.example.diff.table.txt')

for key,value in diff_analysis_path.items():
	diff_analysis_path[key] = os.path.join(mRNA_data_path,quantification_path,expression_summary_dir,value)
##rseqc part
rseqc_analysis_path = dict(genebody_coverage_plot_path='genebody_coverage/genebody_coverage.point.png',
						   inner_distance_plot_path='inner_distance/inner_distance.bar.png',
						   read_distribution_plot_path='read_distribution/read_distribution.bar.png')

for key,value in rseqc_analysis_path.items():
	rseqc_analysis_path[key] = os.path.join(mRNA_data_path,rseqc_path,value)

pdf_analysis_path = {'enrichment':enrichment_analysis_path,
					 'fastqc':fastqc_analysis_path,
					 'mapping':mapping_analysis_path,
					 'quantification':quantification_analysis_path,
					 'diff':diff_analysis_path,
					 'rseqc':rseqc_analysis_path}
##other info
pdf_settings = {'address':address,
				'phone':phone,
				'table_rows':table_rows,
				'max_cell_len':max_cell_len,
				'logo_path':logo_path,
				'project_name':project_nameself,
				'pipeline_path':pipeline_path,
				'mRNAworkflow_path':mRNAworkflow_path}
