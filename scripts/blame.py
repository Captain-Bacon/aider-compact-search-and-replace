#!/usr/bin/env python3

import tempfile
import sys
import subprocess
from pathlib import Path
from aider.dump import dump

def get_lines_with_commit_hash(filename, aider_commits, git_dname, verbose=False):
    result = subprocess.run(
        ["git", "-C", git_dname, "blame", "-l", filename],
        capture_output=True,
        text=True,
        check=True
    )

    hashes = [
        line.split()[0]
        for line in result.stdout.splitlines()
    ]
    lines = Path(filename).read_text().splitlines()

    num_aider_lines = 0
    for hsh,line in zip(hashes, lines):
        if hsh in aider_commits:
            num_aider_lines += 1
            prefix = '+'
        else:
            prefix = " "

        if verbose:
            print(f"{prefix}{line}")

    num_lines = len(lines)

    return num_lines, num_aider_lines


def get_aider_commits(git_dname):
    """Get commit hashes for commits with messages starting with 'aider:'"""

    result = subprocess.run(
        ["git", "-C", git_dname, "log", "--pretty=format:%H %s"],
        capture_output=True,
        text=True,
        check=True
    )

    results = result.stdout.splitlines()
    dump(len(results))

    commits = set()
    for line in results:
        commit_hash, commit_message = line.split(" ", 1)
        if commit_message.startswith("aider:"):
            commits.add(commit_hash)

    dump(len(commits))
    return commits



def process_fnames(fnames, git_dname):
    if not git_dname:
        git_dname = "."

    aider_commits = get_aider_commits(git_dname)
    total_lines = 0
    total_aider_lines = 0

    for fname in fnames:
        num_lines, num_aider_lines = get_lines_with_commit_hash(fname, aider_commits, git_dname)
        total_lines += num_lines
        total_aider_lines += num_aider_lines
        percent_modified = (num_aider_lines / num_lines) * 100 if num_lines > 0 else 0
        if not num_aider_lines:
            continue
        print(f"{fname}: {num_aider_lines}/{num_lines} ({percent_modified:.2f}%)")

    total_percent_modified = (total_aider_lines / total_lines) * 100 if total_lines > 0 else 0
    print(f"Total: {total_aider_lines}/{total_lines} lines by aider ({total_percent_modified:.2f}%)")
    return total_aider_lines, total_lines, total_percent_modified

def process_repo(git_dname=None):
    if not git_dname:
        git_dname = "."

    result = subprocess.run(
        ["git", "-C", git_dname, "ls-files"],
        capture_output=True,
        text=True,
        check=True
    )
    git_dname = Path(git_dname)
    fnames = [git_dname/fname for fname in result.stdout.splitlines() if fname.endswith('.py')]

    return process_fnames(fnames, git_dname)


def history():
    git_dname = "."
    result = subprocess.run(
        ["git", "-C", git_dname, "log", "--pretty=format:%H %s"],
        capture_output=True,
        text=True,
        check=True
    )

    commits = []
    for line in result.stdout.splitlines():
        commit_hash, commit_message = line.split(" ", 1)
        commits.append(commit_hash)

    commits.reverse()
    dump(len(commits))

    num_commits = len(commits)
    N=3
    step = num_commits//N
    results = []
    for i in range(0, num_commits+1, step):
        dump(i, num_commits)
        commit = commits[i]

        repo_dname = tempfile.TemporaryDirectory().name
        cmd = f"git clone . {repo_dname}"
        subprocess.run(cmd.split(), check=True)
        dump(commit)
        cmd = f"git -c advice.detachedHead=false -C {repo_dname} checkout {commit}"
        subprocess.run(cmd.split(), check=True)

        aider_lines, total_lines, pct = process_repo(repo_dname)
        results.append((i, aider_lines, total_lines, pct))

    dump(results)




def main():
    history()
    return

    if len(sys.argv) < 2:
        return process_repo()

    fnames = sys.argv[1:]
    process_fnames(fnames)


if __name__ == "__main__":
    main()
