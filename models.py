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
