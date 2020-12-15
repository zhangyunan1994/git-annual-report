# git-annual-report

git 项目代码分析

分析结果如下:

```bash
你一共参与了 31 个项目
其中在 4 个项目中默默无闻, 你是在偷偷学习吗
在 455 个分支上
进行了 3519 次提交
修改了文件 12534 次, 新增了 513535 行代码, 删除了 435021 行
你对 xxx 项目情有独钟, 贡献了 801 提交
你在周三的码率最高
```

## 如何使用

1. clone 项目到本地
1. 根据 requirements.txt 安装必要依赖
1. 修改 word_tags.py 中字体文件路径
1. 在目录下新增 abc.csv 文件，文件内容为 项目名,项目git地址
1. 打开 `git_annual_report.py` 文件运行即可

**abc.csv示例**

```csv
git-annual-report,https://github.com/zhangyunan1994/git-annual-report.git
kola,https://github.com/zhangyunan1994/kola.git
```

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

# 计划要做

1. 根据提示信息生成图片
1. 将生成的 wordTags 图片生成到图片中
1. 全年提交时段统计【全年你在 10～11点 提交次数最多，是不是再攒着提交】
1. 全年最晚提交时间统计【你最晚的一次提交是在 凌晨3点，凌晨3点的你一定很兴奋吧！】
1. 全年晚上提交次数【】
1. 全年加班次数【工作日 9 点后提交天数】
1. 代码结构分析【语言，框架，常用三方库等】



git log --date=format:'%Y-%m-%d %H:%M:%S' --pretty=format:"%an|%ad|%S|%s" --all --shortstat