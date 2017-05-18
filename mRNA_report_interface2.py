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
