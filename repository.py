# 커밋 저장소, HEAD, 현재 사용자 관리

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