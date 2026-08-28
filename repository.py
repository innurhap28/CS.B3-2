# 커밋 저장소, HEAD, 현재 사용자 관리

import uuid
from datetime import datetime
from commit import Commit

class Repository:
    def __init__(self):
        self.commits = {}
        self.branches = {}
        self.head = None
        self.current_user = None

    def init_repository(self, user_name):
        self.current_user = user_name

        self.branches["main"] = None
        self.head = "main"

    def create_branch(self, branch_name):
        if branch_name in self.branches:
            print("Error: Branch already exists")
            return

        commit_hash = self.branches[self.head]
        self.branches[branch_name] = commit_hash

    def switch_branch(self, branch_name):
        if branch_name not in self.branches:
            print("Error: Branch not exists")
            return
        self.head = branch_name

    def get_current_branch(self):
        return self.head

    def get_current_commit(self):
        commit_hash = self.branches[self.head]
        if commit_hash is None:
            return None
        return self.commits[commit_hash]

    def get_commit(self, commit_hash):
        if commit_hash not in self.commits:
            print("Error: Commit not found")
            return None
        return self.commits[commit_hash]

    def create_commit(self, message):
        if self.current_user is None:
            print("Error: Repository not initialized with a user")
            return None
        current_hash = self.branches[self.head]
        if current_hash is None:
            parents = []
        else:
            parents = [current_hash]

        while True:
            commit_hash = str(uuid.uuid4())[:6]
            if commit_hash not in self.commits:
                break

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_commit = Commit(commit_hash, message, self.current_user, timestamp, parents)
        self.commits[commit_hash] = new_commit
        self.branches[self.head] = commit_hash

        return new_commit