from git_commit_analyze import analyze

if '__main__' == __name__:
    param = {
        'temp_file_path': '/Users/zhangyunan/temp/',  # 临时文件夹，为了clone项目和生成文件使用
        'author': ['zyndev', 'zhangyunan', 'yunan.zhang', '张瑀楠', 'Zhang'],  # 你的git名称，用来分析自己的提交记录
        'group': 'self',  # 本次执行组
        'git': [
            {
                'name': 'git-annual-report',  # 项目名称
                'url': 'git@github.com:zyndev/git-annual-report.git'  # git 地址
            },
        ]
    }
    analyze(param)
