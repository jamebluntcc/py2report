# py2report
py2report 是一个以 Python 模板语言 [**jinja2**](http://jinja.pocoo.org/docs/2.9/) 作为模板引擎,根据 [**lxgui**](https://github.com/bioShaun) 写的 [**RNAseq**](https://github.com/bioShaun/RNAseq) 流程结果文件自动生成 html 报告和 pdf 报告的 python 包。

## 参数
- option: -html(--html) 生成html版本报告；
- option: -pdf(--pdf) 生成pdf版本报告；
- option: -part(--part) 当报告缺少一部分分析结果的时候保证能够顺利生成报告；(需要注意的是参数 part 只能用于 pdf 报告的生成)

```
python main.py your_report_result_path -pdf -part 
```

## 运行
确定运行前执行 `pip install -r requirment.txt` 安装程序所需要的依赖保证能够正常的运行，程序可以部署在34(onmath 的服务器)和167(另一个onmath的服务器)上，需要进入 `main/__init__.py` 文件更改配置:
```python
#34上的配置
logo_path =  command.get('mRNA-pdf-static-34','logo_path')
pipeline_path =  command.get('mRNA-pdf-static-34','pipeline_path')
mRNAworkflow_path =  command.get('mRNA-pdf-static-34','mRNAworkflow_path')
#167上的配置
logo_path =  command.get('mRNA-pdf-static-167','logo_path')
pipeline_path =  command.get('mRNA-pdf-static-167','pipeline_path')
mRNAworkflow_path =  command.get('mRNA-pdf-static-167','mRNAworkflow_path')
```
如果以后需要运行在更多的服务器上请进入 `report_conf.conf` 中进行设置。

一切准备就绪后，在主程序`manager.py`下运行:(注意到report_result_path必须为绝对路径)
```sh
python main.py your_report_result_path --html #生成 html 报告

python main.py your_report_result_path --pdf #生成 pdf 报告
```
