# latex2pdf
- latex2pdf:产生mRNA analysis results,sequencing report的报告。采用python django框架里的模板引擎输出latex文档。
## 运行
- 确定运行前导入python django模块保证正常的运行环境;
- report_conf中可以更改基本的配置信息;
- python latex2pdf_linux_2.1.py -h 查看参数说明其中可以选择有无assembly部分;
- 脚本位置:onmath 34 address:/home/lxgui/chencheng/report/latex2pdf;
```
- python latex2pdf_linux_2.1.py report_dir #运行脚本
```
## 新增html版本
latex2html 使用的模板渲染模板和latex2pdf不同,latex2html使用jinja2。除此之外和latex2pdf没有什么不同
latex2html脚本使用方法和latex2pdf基本一致:
```
python latex2html.py report_dir
```
