#coding=utf-8
'''
create on 2016-10-31
version = 1.0
template engine using django templates
function:create sequencing report
'''
import re
import sys
import os
import time
import glob
import django
import configparser
import subprocess
from django.conf import settings
settings.configure(TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.abspath('/home/lxgui/chencheng/report/latex2pdf'),'templates','sequencing_report'),
                 os.path.join(os.path.abspath('/home/lxgui/chencheng/report/latex2pdf'),'templates','mRNA_report'),
                 os.path.join(os.path.abspath('/home/lxgui/chencheng/report/latex2pdf'),'templates','data_table')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
])

django.setup()
from django.template import Context
from django.template.loader import get_template

def create_template(template_file,output_file,context):
    t = get_template(template_file)
    file = t.render(Context(context))
    try:
        f = open(output_file,'w',encoding='UTF-8')
        f.write(file)
        f.close()
    except IOError as e:
        print(e)
        sys.exit(1)

def create_filter_table(input_file,output_file,split):
    with open(input_file.replace('\\', '/'), 'rt', encoding='UTF-8') as input_f:
        data = input_f.readlines()
        data_head = data[0]
        data_body = data[1:]
        output_f = open(output_file, 'wt', encoding='UTF-8')
        output_f.write('%s\n' % (r'\toprule'))
        head_list = cut_overlong_table(data_head.strip().split(split))[:2]
        output_f.write('&'.join(head_list).replace('_', '\_').replace('%', '\%') + r'\\' + '\n')
        output_f.write('%s\n' % (r'\midrule'))
        for line in data_body:
            each_list = cut_overlong_table(line.strip('\n').split(split))[:2]
            output_f.write('&'.join(each_list).replace('_', '\_').replace('%', '\%') + r'\\' + '\n')
        output_f.write(r'\bottomrule')
        output_f.close()

def cut_overlong_table(row_list,max_len=20):
    for i in range(len(row_list)):
        if len(row_list[i]) > max_len:
           row_list[i] = row_list[i][:max_len] + '...'
    return row_list

def rep(str,n):
    i = 0
    tmp_str = ''
    while i < n:
        tmp_str = tmp_str + str
        i += 1
    return tmp_str

def three_line_table(input_file,output_file,split):
    with open(input_file,'rt',encoding='UTF-8') as f:
        data = f.readlines()
    thead = data[0]
    tboy = data[1:len(data)]
    if len(tboy) > table_len:
        tboy = tboy[:table_len]
    f = open(output_file,'wt',encoding='UTF-8')
    f.write('%s\n'%(r'\toprule'))
    head_list = cut_overlong_table(thead.strip('\n').split(split))
    f.write('&'.join(head_list).replace('_','\_').replace('%','\%') + r'\\' +'\n')
    f.write('%s\n'%(r'\midrule'))
    for line in tboy:
        each_list = cut_overlong_table(line.strip('\n').split(split))
        f.write('&'.join(each_list).replace('_','\_').replace('%','\%') + r'\\' +'\n')
    f.write(r'\bottomrule')
    f.close()
    return 0

def find_plot_path(plot_dir):
    plot_path = glob.glob(os.path.join(plot_dir,'*.png'))
    if len(plot_path) == 0:
        print('ERROR in %s'%plot_dir)
        exit(1)
    return plot_path[0].replace('\\','/')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python + %s + sequencing report dir'%sys.argv[0])
    table_len = 30
    REPORT_DIR = sys.argv[1]
    REPORT_DIR_LIST = REPORT_DIR.split('/')
    REPORT_DIR_SHORT = '/'.join(REPORT_DIR_LIST[:len(REPORT_DIR_LIST) - 1]) + '/'
    command = configparser.ConfigParser()
    command.read('report_conf.conf')
    project_num = command.get('sequencing','project_num')
    report_name = command.get('sequencing','report_name')
    project_name = command.get('sequencing','project_name')
    library_name = command.get('sequencing','library_name')
    reads_length  = command.get('sequencing','reads_length')
    data_count = command.get('sequencing','data_count')
    q30_avg = command.get('sequencing','q30_avg')
    data_filter_dir = filter_distrbution_dir = None
    clean_data_barplot_dir = raw_data_barplot_dir = None
    base_quality_dir = base_content_dir = None
    data_count_table_dir = NT_table_dir = None

    for roots, dirs, files in os.walk(REPORT_DIR):
        if re.search('fiter.stat$', roots):
            data_filter_dir = roots
            create_filter_table(os.path.join(data_filter_dir,'filter.stat.xls'),'/home/lxgui/chencheng/report/latex2pdf/templates/data_table/data_filter_table.txt',split='\t')
        elif re.search('fiter.rate$',roots):
            filter_distrbution_dir = roots
        elif re.search('CleanBase$',roots):
            clean_data_barplot_dir = roots
        elif re.search('RawBase$',roots):
            raw_data_barplot_dir = roots
        elif re.search('base_quality$',roots):
            base_quality_dir = roots
        elif re.search('base_content$',roots):
            base_content_dir = roots
        elif re.search('output_stat$',roots):
            data_count_table_dir = roots
            three_line_table(os.path.join(data_count_table_dir,'output_stat.xls'),'/home/lxgui/chencheng/report/latex2pdf/templates/data_table/data_count_table.txt',split='\t')
        elif re.search('NT$',roots):
            NT_table_dir = roots
            three_line_table(os.path.join(NT_table_dir,'nt.stat.xls'),'/home/lxgui/chencheng/report/latex2pdf/templates/data_table/nt_table.txt',split='\t')

    all_dir = {'data_filter_dir': data_filter_dir, 'filter_distrbution_dir': filter_distrbution_dir,
                            'clean_data_barplot_dir': clean_data_barplot_dir, 'raw_data_barplot_dir': raw_data_barplot_dir,
                            'base_quality_dir': base_quality_dir, 'base_content_dir': base_content_dir,
                            'data_count_table_dir': data_count_table_dir,'NT_table_dir': NT_table_dir}

    for k, v in all_dir.items():
        if v == None:
            print('%s is empty' % k)
            sys.exit(1)

    context = {'project_num': project_num,
                'report_name': report_name,
                'project_name': project_name,
                'library_name': library_name,
                'reads_length': reads_length,
                'data_count': data_count,
                'q30_avg': q30_avg,
                'filter_distrbution_plot': '{./' + find_plot_path(filter_distrbution_dir).replace(REPORT_DIR_SHORT,'') + '}',
                'clean_data_barplot': '{./' + find_plot_path(clean_data_barplot_dir).replace(REPORT_DIR_SHORT,'')  + '}',
                'raw_data_barplot': '{./' + find_plot_path(raw_data_barplot_dir).replace(REPORT_DIR_SHORT,'')  + '}',
                'mean_quality_distrbution_plot': '{./' + find_plot_path(base_quality_dir).replace(REPORT_DIR_SHORT,'')  + '}',
                'base_distrbution_plot': '{./' + find_plot_path(base_content_dir).replace(REPORT_DIR_SHORT,'')  + '}',
                'mean_quality_distrbution_plot_href': '{run:./' + base_quality_dir.replace(REPORT_DIR_SHORT,'') + '}',
                'base_distrbution_plot_href': '{run:./' + base_content_dir.replace(REPORT_DIR_SHORT,'') + '}'
               }
    output_tex_file = project_num + '_DNAsequencing_report.tex'
    create_template('sequencing_main.txt',os.path.join(REPORT_DIR_SHORT,output_tex_file),context=context)
    #run xelatex:
    os.chdir(REPORT_DIR_SHORT)
    tex_list = glob.glob(os.path.join(REPORT_DIR_SHORT, output_tex_file))
    rm_set = ('.aux', '.log', '.out', '.tex','.toc', '.tmp', '.bib')
    if len(tex_list) == 1:
        subprocess.call('xelatex %s' % output_tex_file, shell=True)
        subprocess.call('xelatex %s' % output_tex_file, shell=True)
        for each_file in os.listdir(REPORT_DIR_SHORT):
            if os.path.splitext(each_file)[1] in rm_set:
                subprocess.call('rm %s' % each_file, shell=True)
        subprocess.call('echo sequencing report all done!', shell=True)
    else:
        print('Not one tex file in %s'%REPORT_DIR_SHORT)
        sys.exit(1)



