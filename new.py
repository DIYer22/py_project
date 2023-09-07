#!/usr/bin/env python
import os
import sys
import shutil
from pathlib import Path
import subprocess
from glob import glob


def copy_directory(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as e:
        print(f"Error: {e}")


def remove(dirr, glob_match):
    files_list = glob(os.path.join(dirr, "**", glob_match), recursive=True)
    for file in files_list:
        if os.path.isfile(file):
            os.remove(file)
        elif os.path.isdir(file):
            shutil.rmtree(file)


def replace_text_in_files(directory, old, new):
    for path in Path(directory).rglob("*"):
        if path.suffix in (".py", ".md"):
            with open(path, "r+") as file:
                content = file.read()
                content = content.replace(old, new)
                file.seek(0)
                file.truncate()
                file.write(content)


def init_git_and_commit(dest_dir, project_name):
    os.chdir(dest_dir)
    subprocess.run(["git", "init"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "rm", "--cached", "requirements.txt"])
    subprocess.run(["git", "rm", "-r", "--cached", "doc"])

    commit_message = f"Init of {project_name}"
    subprocess.run(["git", "commit", "-m", commit_message])


def main():
    if len(sys.argv) != 2:
        sys.stderr.write(
            """Usage: python new.py project_name\n
这个文件会按照你的要求执行以下操作：

1. 复制源目录到新的目录下，并重命名为 `project_name/`
2. 将 `project_name/py_project` 重命名为 `project_name/project_name`
3. 替换所有 `.py` 和 `.md` 文件中的 `py_project` 为 `project_name`
4. 执行 `git init`，将所有文件添加到 git 中
5. 从 git 添加文件中移除 `requirements.txt` 和 `doc/`
6. 提交 commit 信息为 "Init of {project_name}"

使用方法：
```bash
python new.py project_name
```
"""
        )
        sys.exit(1)

    project_name = sys.argv[1]

    source_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(source_dir, "..", project_name)
    assert not os.path.exists(dest_dir), dest_dir
    copy_directory(source_dir, dest_dir)
    remove(dest_dir, "new.py")
    remove(dest_dir, "__pycache__")
    remove(dest_dir, "*.pyc")
    remove(dest_dir, ".git")

    renamed_path = os.path.join(dest_dir, project_name)
    os.rename(os.path.join(dest_dir, "py_project"), renamed_path)

    replace_text_in_files(dest_dir, "py_project", project_name)

    init_git_and_commit(dest_dir, project_name)


if __name__ == "__main__":
    main()
