#coding:UTF-8
import os
import argparse
import configparser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '---create mRNA analysis report---')
    parser.add_argument('mRNA_report_path',help='a dir where include your analysis results')
    parser.add_argument('--pdf',action='store_true',help='print out pdf report')
    parser.add_argument('--html',action='store_true',help='print out html report')
    args = parser.parse_args()

    command = configparser.ConfigParser()
    command.read('report_conf.conf')
    report_data_path = command.get('mRNA','report_data')
    mRNA_report_dir = os.path.abspath(args.mRNA_report_path)
    generate_report_path = os.path.join(mRNA_report_dir,report_data_path)
    
