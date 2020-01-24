# git-annual-report

git 项目代码分析

分析结果如下:

```bash
你一共参与了 31 个项目
其中在 4 个项目中默默无闻，你是在偷偷学习吗
在 455 个分支上
进行了 3519 次提交
修改了文件 12534 次, 新增了 513535 行代码, 删除了 435021 行
你对 ecm-admin 项目情有独钟, 贡献了 801 提交
你在周三的码率最高
```

## 如何使用

1. clone 项目到本地
1. 根据 requirements.txt 安装必要依赖
1. 打开 `git_annual_report.py` 文件运行即可

参数介绍
```python
{
    'temp_file_path': '/Users/zhangyunan/temp/', # 临时文件夹，为了clone项目和生成文件使用
    'author': ['zyndev', 'zhangyunan', 'yunan.zhang', '张瑀楠', 'Zhang'], # 你的git名称，用来分析自己的提交记录
    'group': 'self', # 本次执行组
    'git': [
        {   
            'name': 'git-annual-report',  # 项目名称
            'url': 'git@github.com:zyndev/git-annual-report.git'  # git 地址
        },
    ]
}
```


git log --date=format:'%Y-%m-%d %H:%M:%S' --pretty=format:"%an|%ad|%S|%s" --all --shortstat