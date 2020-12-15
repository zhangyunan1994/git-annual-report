from git_commit_analyze import analyze
from csv_r import read_csv


if '__main__' == __name__:
    param = {
        'temp_file_path': 'c:/Users/zhangyunan/temp/',  # 临时文件夹，为了clone项目和生成文件使用
        'author': ['zyndev', 'zhangyunan', 'yunan.zhang', '张瑀楠', 'Zhang', 'zhangyunan1994'],  # 你的git名称，用来分析自己的提交记录
        'group': 'self',  # 本次执行组
        'git': read_csv()
    }
    analyze(param)
