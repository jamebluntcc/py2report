#coding:UTF-8
import os
import jinja2
import configparser

#template env config
html_jinja_env = jinja2.Environment(
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.join(os.path.abspath('.'),'html_templates'))
)
pdf_jinja_env = jinja2.Environment(
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.join(os.path.abspath('.'),'pdf_templates'))
)
#add each analysis part
command = configparser.ConfigParser()
command.read('report_conf.conf')
#all path
mRNA_data_path = command.get('mRNA-data','report_data')
enrichment_path = command.get('mRNA-path','enrichment_path')
fastqc_path = command.get('mRNA-path','fastqc_path')
mapping_path = command.get('mRNA-path','mapping_path')
quantification_path = command.get('mRNA-path','quantification_path')
rseqc_path = command.get('mRNA-path','rseqc_path')
#enrichment
go_table = command.get('mRNA-enrichment','go_table')
go_bar_pattern = command.get('mRNA-enrichment','go_bar_pattern')
go_dag_pattern = command.get('mRNA-enrichment','go_dag_pattern')
kegg_table = command.get('mRNA-enrichment','kegg_table')
kegg_bar_pattern = command.get('mRNA-enrichment','kegg_bar_pattern')
kegg_pathway_pattern = command.get('mRNA-enrichment','kegg_pathway_pattern')
#fastqc
gc_distribution_pattern = command.get('mRNA-fastqc','gc_distribution_pattern')
reads_quality_pattern = command.get('mRNA-fastqc','gc_distribution_pattern')
fastqc_table = command.get('mRNA-fastqc','fastqc_table')
#mapping
mapping_plot = command.get('mRNA-mapping','mapping_plot')
mapping_table = command.get('mRNA-mapping','mapping_table')
#quantification
volcano_plot_pattern = command.get('mRNA-quantification','volcano_plot_pattern')
all_volcano_plot = command.get('mRNA-quantification','all_volcano_plot')
diff_gene_heatmap_plot = command.get('mRNA-quantification','diff_gene_heatmap_plot')
gene_expression_plot = command.get('mRNA-quantification','gene_expression_plot')
pca_plot = command.get('mRNA-quantification','pca_plot')
sample_correlation_plot = command.get('mRNA-quantification','sample_correlation_plot')
pdf_diff_table = command.get('mRNA-quantification','pdf_diff_table')
pdf_gene_table = command.get('mRNA-quantification','pdf_gene_table')
html_diff_table = command.get('mRNA-quantification','html_diff_table')
html_gene_table = command.get('mRNA-quantification','html_gene_table')
#rseqc
reads_duplication_pattern = command.get('mRNA-rseqc','reads_duplication_pattern')
genebody_coverage_pattern = command.get('mRNA-rseqc','genebody_coverage_pattern')
inner_distance_pattern = command.get('mRNA-rseqc','inner_distance_pattern')
reads_distribution_pattern = command.get('mRNA-rseqc','reads_distribution_pattern')
pdf_reads_duplication = command.get('mRNA-rseqc','pdf_reads_duplication')
pdf_inner_distance = command.get('mRNA-rseqc','pdf_inner_distance')
pdf_read_distribution = command.get('mRNA-rseqc','pdf_read_distribution')
pdf_genebody_coverage = command.get('mRNA-rseqc','pdf_genebody_coverage')

all_path = dict(enrichment_path=enrichment_path,fastqc_path=fastqc_path,mapping_path=mapping_path,
                quantification_path=quantification_path,rseqc_path=rseqc_path)

for key,value in all_path.items():
    all_path[key] = os.path.join(mRNA_data_path,value)

enrichment_part = dict(go_table=go_table,go_bar_pattern=go_bar_pattern,go_dag_pattern=go_dag_pattern,
                       kegg_table=kegg_table,kegg_bar_pattern=kegg_bar_pattern,kegg_pathway_pattern=kegg_pathway_pattern)
for key,value in enrichment_part.items():
    enrichment_part[key] = os.path.join(mRNA_data_path,value)

fastqc_part = dict(gc_distribution_pattern=gc_distribution_pattern,
                   reads_quality_pattern=reads_quality_pattern,
                   fastqc_table=fastqc_table)
for key,value in fastqc_part.items():
    fastqc_part[key] = os.path.join(mRNA_data_path,value)

mapping_part = dict(mapping_plot=mapping_plot,mapping_table=mapping_table)
for key,value in mapping_part.items():
    mapping_part[key] = os.path.join(mRNA_data_path,value)

quantification_part = dict(volcano_plot_pattern=volcano_plot_pattern,all_volcano_plot=all_volcano_plot,
                           diff_gene_heatmap_plot=diff_gene_heatmap_plot,gene_expression_plot=gene_expression_plot,
                           sample_correlation_plot=sample_correlation_plot,pca_plot=pca_plot,
                           pdf_diff_table=pdf_diff_table,pdf_gene_table=pdf_gene_table,
                           html_diff_table=html_diff_table,html_gene_table=html_gene_table)
for key,value in quantification_part.items():
    quantification_part[key] = os.path.join(mRNA_data_path,value)

rseqc_part = dict(reads_duplication_pattern=reads_duplication_pattern,genebody_coverage_pattern=genebody_coverage_pattern,
                  inner_distance_pattern=inner_distance_pattern,reads_distribution_pattern=reads_distribution_pattern,
                  pdf_reads_duplication=pdf_reads_duplication,pdf_inner_distance=pdf_inner_distance,
                  pdf_read_distribution=pdf_read_distribution,pdf_genebody_coverage=pdf_genebody_coverage)
for key,value in rseqc_part.items():
    rseqc_part[key] = os.path.join(mRNA_data_path,value)
