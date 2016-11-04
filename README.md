#latex2pdf
- latex2pdf自述：主要用于产生onmath的mRNA report和sequencing report,由python的
django作为模板引擎，产生latex文档。
- latex2pdf构成：
 - templates储存mRNA和sequencing report模板
 - test用于测试文件
 - report_conf.conf写入report的基本信息
- Run：(保证提前进入python env 正常使用django模块)
 - mRNA report: python latex2pdf_linux1.2.py mRNA_report_dir(不包括最后的斜杠)
 - sequencing report:python sequencing_report1.1.py sequencing_report_dir
- test report dir：
 - onmath 34 address:/home/lxgui/chencheng/report/test_report_dir
 