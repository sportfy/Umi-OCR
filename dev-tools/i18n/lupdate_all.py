# 刷新所有翻译文本文件 .ts

import os

LangList = [
    "en_US",
    "zh_TW",
    "ja_JP",
    # "es_ES",
    # "fr_FR",
    # "de_DE",
    # "ko_KR",
    # "ru_RU",
    # "pt_BR",
    # "it_IT",
]

working = os.path.dirname(os.path.abspath(__file__))  # 工作目录
os.chdir(working)

for l in LangList:
    cmd = f'''lupdate.exe \
"../../UmiOCR-data/qt_res/qml" \
-recursive \
-no-obsolete \
-source-language "zh_CN" \
-target-language "{l}" \
-ts "release/{l}.ts"'''
    os.system(cmd)
