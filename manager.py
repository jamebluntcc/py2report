#coding:UTF-8
import os
import argparse
from main import html_report
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '---create mRNA analysis report---')
    parser.add_argument('mRNA_report_path',help='a dir where include your analysis results')
    parser.add_argument('--pdf',action='store_true',help='print out pdf report')
    parser.add_argument('--html',action='store_true',help='print out html report')
    args = parser.parse_args()
    print args.mRNA_report_path
    if args.html:
        html_report.enrichment_analysis(args.mRNA_report_path)
