# __Author__ = "Pranav Chandran"
# __Date__ = 24-02-2023
# __Time__ = 13:33
# __FileName__ = git_helpers.py
import os
import shutil
import stat
from git import Repo, GitCommandError


class GitHelper:
    """
    Fetch the git repo
    """
    def __init__(self, repo_url, ssh_key_filename):
        self.repo_url = repo_url
        self.ssh_key_filename = ssh_key_filename

    def remove_readonly(self, func, path, excinfo):
        """
        Remove the read only attribute
        """
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def fetch_git_repo(self):
        """
        Fetch the git repo
        """
        try:
            # Construct path to SSH key file
            ssh_key_path = os.path.join(os.path.expanduser('~'), '.ssh', self.ssh_key_filename)

            # Clone the repo
            cwd = os.getcwd()
            clone_dir = os.path.join(cwd, os.path.basename(self.repo_url).replace(".git", ""))
            if os.path.exists(clone_dir):
                shutil.rmtree(clone_dir, onerror=self.remove_readonly)

            Repo.clone_from(self.repo_url, clone_dir, env={'GIT_SSH_COMMAND': 'ssh -i %s' % ssh_key_path})

            print("Git repo cloned successfully")
        except GitCommandError as e:
            print(f"Error cloning git repo: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Enter the GitHub repo URL and SSH key filename
    repo_url = "git@github.com:pranavchandran/xxxxxx.git" # Security issue not showing the repo url
    ssh_key_filename = "id_ed25519" # You need to create a ssh key and add it to your github account
    obj = GitHelper(repo_url, ssh_key_filename)
    # Fetch the git repo
    obj.fetch_git_repo()
