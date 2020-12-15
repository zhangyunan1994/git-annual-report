import shutil
from functools import reduce
import datetime

from models import CommitInfo, ExtractGitProject
import random

import os
import subprocess

from word_tags import generate_word_cloud

self_author = '_self'
leisure_contributor = ['打酱油', '默默无闻', '摸鱼']


def clone_git_project_then_obtain_info(param):
    root_path = f"{param.get('temp_file_path')}/{param.get('group')}/"
    if os.path.exists(root_path):
         shutil.rmtree(root_path)
    if not param.get('git'):
        raise RuntimeError("no git project")
    git_log_path = f"{root_path}/log/"
    git_project_path = f"{root_path}/git/"
    if not os.path.exists(git_log_path):  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(git_log_path)
    result = []
    for git_project in param.get('git'):
        print(f"start clone {git_project.get('name')}")
        extract_git_project = ExtractGitProject(git_project.get('name'))
        extract_git_project.git_path = git_project_path + '/' + git_project.get('name')
        if not os.path.exists(extract_git_project.git_path):
            subprocess.call(f"git clone {git_project.get('url')} {extract_git_project.git_path}", shell=True)
        extract_git_project.commit_path = git_log_path + '/' + git_project.get('name')
        if not os.path.exists(extract_git_project.commit_path):
            print(f"""cd {extract_git_project.git_path} && git log --date=format:'%Y-%m-%d %H:%M:%S' --pretty=format:"%an|%ad|%S|%s" --all --shortstat > {extract_git_project.commit_path}""")
            subprocess.call(
                f"""cd {extract_git_project.git_path} && git log --date=format:"%Y-%m-%d %H:%M:%S" --pretty=format:"%an|%ad|%S|%s" --all --shortstat > {extract_git_project.commit_path}""",
                shell=True)
        result.append(extract_git_project)
    return result


def extract_commits(project_name, file_path, author):
    lines = list(open(file_path, encoding='utf-8').readlines())
    commit_info_list = []
    commit_info = None
    for line in lines:
        if '|' in line:
            if commit_info:
                commit_info_list.append(commit_info)
            commit_user_info = line.split("|", 4)
            commit_info = CommitInfo()
            commit_info.name = project_name
            commit_info.author = commit_user_info[0]
            if commit_info.author in author:
                commit_info.author = self_author
            commit_info.date = datetime.datetime.strptime(commit_user_info[1], "%Y-%m-%d %H:%M:%S")
            commit_info.branch = commit_user_info[2].replace('refs/remotes/origin/', '').replace('refs/heads/',
                                                                                                 '').replace(
                'refs/tags/', '')
            commit_info.message = commit_user_info[3]
        elif 'file changed' in line or 'files changed' in line:
            sp_msg = line.split(',')
            for sp in sp_msg:
                count = int(sp.strip().split(' ')[0])
                if 'file' in sp:
                    commit_info.file_changed = count
                elif 'insertion' in sp:
                    commit_info.insertion = count
                elif 'deletion' in sp:
                    commit_info.deletion = count
    commit_info_list.append(commit_info)
    return commit_info_list


def statistics_log(temp_path, git_projects, author):
    print('********************')
    print('***    开始统计   ***')
    print('********************')
    """
    在 2021 中，

    你一共参加了 10 个项目，
    在 102 个分支上
    进行了 7000 次提交

    新增了 1040000 行代码，删除了 2000000 行

    你对 xxx 项目情有独钟，贡献了 xxxx 提交

    你在周三的码率最高
    全年你在 10～11点 提交次数最多，是不是再攒着提交，

    你最晚的一次提交是在 凌晨3点，凌晨3点的你一定很兴奋吧！


    全年你有 6个非工作日再提交代码，是不是在改bug呀！ 不要太拼哦，偶尔也要做个头发

    你和 xxx 个同时，共同开发过 4 个项目，其中 项目 xx 分支的协作用户最多，是不是有很大的分歧呀，
    你和 xxx 合作最多，一定是特殊的默契


    你最长上线的第一个项目时 xxx, 共用了 180 天，其中的挫折是不是很多
    :param temp_path:
    :param git_projects:
    :return:
    """
    project_contributor = {}
    no_commit_project = []
    all_project_commits = []
    for project in git_projects:
        print(f"开始成功图 {project.name}")
        commits = extract_commits(project.name, project.commit_path, author)
        project.word_cloud_path = generate_word_cloud(project.name, [x.message for x in commits], temp_path)
        # 统计每个用户的提交
        contributor = {}
        for commit in commits:
            contributor_commits = contributor.get(commit.author)
            if not contributor_commits:
                contributor_commits = []
            contributor_commits.append(commit)
            contributor[commit.author] = contributor_commits
        project_contributor[project.name] = contributor
        if self_author in contributor:
            all_project_commits.extend(commits)
        else:
            no_commit_project.append(project.name)

    print(f'你一共参与了 {len(git_projects)} 个项目')
    if len(no_commit_project) > 0:
        if len(no_commit_project) > 3:
            print(f'其中在 {no_commit_project[:2]} 等 {len(no_commit_project)} 个项目中{random.choice(leisure_contributor)}, 你是在偷偷学习吗, 还是害羞的不好意思提交? ')
        else:
            print(f'其中在 {no_commit_project} 等 {len(no_commit_project)} 个项目中{random.choice(leisure_contributor)}, 你是在偷偷学习吗, 还是害羞的不好意思提交? ')

    # 在所有分支中找到自己的提交记录
    all_project_self_commits = list(filter(lambda x: x.author == self_author, all_project_commits))
    all_project_self_branch = set([x.name + '@' + x.branch for x in all_project_self_commits])
    print(f'在 {len(all_project_self_branch)} 个分支上\n进行了 {len(all_project_self_commits)} 次提交')
    files_change_count = reduce(lambda x, y: x + y, map(lambda x: x.file_changed, all_project_self_commits))
    insertion_count = reduce(lambda x, y: x + y, map(lambda x: x.insertion, all_project_self_commits))
    deletion_count = reduce(lambda x, y: x + y, map(lambda x: x.deletion, all_project_self_commits))
    print(f'修改了文件 {files_change_count} 次, 新增了 {insertion_count} 行代码, 删除了 {deletion_count} 行')

    # 获取最喜欢的项目
    favourite_project = ['unknow', -1]
    for project_name, contributor in project_contributor.items():
        self_commits = contributor.get(self_author)
        if self_commits and favourite_project[1] < len(self_commits):
            favourite_project[1] = len(self_commits)
            favourite_project[0] = project_name

    print(f'你对 {favourite_project[0]} 项目情有独钟, 贡献了 {favourite_project[1]} 提交')

    # 获取码率最高的星期
    week_commit_count = [0, 0, 0, 0, 0, 0, 0]
    weekend = ('一', '二', '三', '四', '五', '六', '日')
    weekend_code = []
    for commit in all_project_self_commits:
        week_commit_count[commit.date.weekday()] = week_commit_count[commit.date.weekday()] + 1
        if commit.date.weekday() > 4:
            weekend_code.append(commit.date.strftime("%Y-%m-%d"))

    # 查询最大值的index
    index = -1
    count = 0
    for (i, c) in enumerate(week_commit_count):
        if c > count:
            count = c
            index = i
    print(f'你在周{weekend[index]}的码率最高')

    print(f'全年你有 {len(set(weekend_code))} 个非工作日再提交代码，是不是在改bug呀！ 不要太拼哦，偶尔也要做个头发')
    print('\n' * 4)

    for project_name, contributor in project_contributor.items():
        if self_author not in contributor:
            print(f'你在 {project_name} 项目中{random.choice(leisure_contributor)}, 其他 {len(contributor)} 个人在勤奋的敲键盘')
        elif len(contributor) - 1 == 0:
            print(f'你在 {project_name} 项目中孤军奋战，一定很孤单吧')
        else:
            print(f'你在 {project_name} 项目中和其他 {len(contributor) - 1} 个人合作过')


def analyze(param):
    git_projects = clone_git_project_then_obtain_info(param)
    statistics_log(param.get('temp_file_path') + param.get('group'), git_projects, param.get('author'))

