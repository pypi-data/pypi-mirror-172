#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage


def json2docx(template_docx, output_docx, context):
    ''' 
    根据模板及字典创建docx
    :param template_docx 模板文件路径
    :param output_docx 输出文件路径
    :param context 字典
    '''
    docx = DocxTemplate(template_docx)
    for _ in context:
        if isinstance(context[_], str):
            if os.path.isfile(context[_]):
                if context[_].split('.')[-1].lower() in ['bmp', 'jpg', 'png', 'jpeg', 'gif']:
                    context[_] = InlineImage(docx, context[_], width=Mm(160))
    docx.render(context)
    docx.save(output_docx)
