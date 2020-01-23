import jieba
from wordcloud import WordCloud
import shutil

import os
import subprocess

debug = True


class CommitInfo:
    name = None
    author = None
    date = None
    branch = None
    message = None
    file_changed = 0
    insertion = 0
    deletion = 0

    def __init__(self, name=None, author=None, date=None, branch=None, message=None, file_changed=0, insertion=0, deletion=0):
        self.name = name
        self.author = author
        self.date = date
        self.branch = branch
        self.message = message
        self.file_changed = file_changed
        self.insertion = insertion
        self.deletion = deletion


class ExtractGitProject:
    git_path = None
    commit_path = None
    word_cloud_path = None
    name = None

    def __init__(self, name, git_path=None, commit_path=None, word_cloud_path=None):
        self.name = name
        self.git_path = git_path
        self.commit_path = commit_path
        self.word_cloud_path = word_cloud_path

    def __str__(self):
        print(f'{self.name} {self.git_path} {self.commit_path} {self.word_cloud_path}')
        return f'{self.name} {self.git_path} {self.commit_path} {self.word_cloud_path}'


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
        subprocess.call(f"git clone {git_project.get('url')} {extract_git_project.git_path}", shell=True)
        extract_git_project.commit_path = git_log_path + '/' + git_project.get('name')
        subprocess.call(f"""cd {extract_git_project.git_path} && git log --date=format:'%Y-%m-%d %H:%M:%S' --pretty=format:"%an|%ad|%S|%s" --all --shortstat > {extract_git_project.commit_path}""", shell=True)
        result.append(extract_git_project)
    return result


def extract_commits(project_name, file_path):
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
            commit_info.date = commit_user_info[1]
            commit_info.branch = commit_user_info[2].replace('refs/remotes/origin/', '').replace('refs/heads/', '').replace('refs/tags/', '')
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
    # if debug:
    #     for info in commit_info_list:
    #         print(f'{info.author} 在 {info.date} 向 {info.branch} 分支修改了 {info.file_changed} 文件，添加了 {info.insertion} 行代码, 删除了 {info.deletion} 行代码')
    # print(commit_info_list)
    return commit_info_list


def statistics_log(temp_path, git_projects):
    """
    在 2021 中，

    你一共参加了 10 个项目，
    在  102 个分支上
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
    all_project_commits = []
    for project in git_projects:
        commits = extract_commits(project.name, project.commit_path)
        project.word_cloud_path = generate_word_cloud(project.name, commits, temp_path)
        all_project_commits.extend(commits)
        # 统计每个用户的提交
        commitor = {}
        for commit in commits:
            comit = commitor.get(commit.author)
            if not comit:
                comit = []
            comit.append(commit)
            commitor[commit.author] = comit
        print(f'你在 {project.name} 项目中和 {len(commitor)} 个人合作过')

    # print(git_projects)


def generate_word_cloud(project_name, commits, temp_path):
    word_cloud_root_path = f"{temp_path}/wordcloud/"
    if not os.path.exists(word_cloud_root_path):
        os.mkdir(word_cloud_root_path)
    str_list = []
    for commit in commits:
        if 'Merge branch' in commit.message:
            continue
        for msg in list(jieba.cut(commit.message)):
            str_list.append(msg)

    wc = WordCloud(font_path='Hiragino Sans GB.ttc', background_color="white", width=1000, height=860, margin=2)\
        .generate(' '.join(str_list))
    word_cloud_path = f'{temp_path}/wordcloud/{project_name}.png'
    wc.to_file(word_cloud_path)
    return word_cloud_path


if '__main__' == __name__:
    param = {
        'temp_file_path': '/Users/zhangyunan/temp/',
        'group': 'self',
        'git': [
            {
                'name': 'pearProject',
                'url': 'git@gitee.com:zyndev/vue-projectManage.git'
            },
            {
                'name': 'devops',
                'url': 'git@gitee.com:scoding/devops.git'
            },
            {
                'name': 'checkstyle',
                'url': 'git@gitee.com:zyndev/checkstyle.git'
            },
            {
                'name': 'universe_publish',
                'url': 'git@gitee.com:zyndev/universe_publish.git'
            }
        ]
    }
    git_projects = clone_git_project_then_obtain_info(param)
    statistics_log(param.get('temp_file_path') + param.get('group'), git_projects)
