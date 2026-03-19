from github import Github
from os import getenv
from logs.logger import logger

GITHUB_TOKEN = getenv("GITHUB_TOKEN")
REPO_NAME = "gemini-dot/html_upload"


def upload_html_to_github(file, filename, user_email):
    try:
        if not GITHUB_TOKEN:
            logger.error("Chưa cấu hình GITHUB_TOKEN trên Render!")
            return None

        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        if isinstance(file, str):
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = file.read().decode("utf-8")

        user_folder = user_email.replace("@", "_").replace(".", "_")
        path_in_repo = f"users/{user_folder}/{filename}"

        try:
            contents = repo.get_contents(path_in_repo, ref="main")
            repo.update_file(
                path_in_repo, f"Update {filename}", content, contents.sha, branch="main"
            )
        except:
            repo.create_file(path_in_repo, f"Upload {filename}", content, branch="main")

        return f"https://gemini-dot.github.io/html_upload/{path_in_repo}?username={user_email}"

    except Exception as e:
        logger.error(f"Lỗi xử lý GitHub: {e}")
        return None
