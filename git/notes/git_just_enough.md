# Git: Just Enough

Git records the history of files in a project. You can use Git commands in VS
Code's terminal (`Terminal > New Terminal`) or use the Source Control view
(`Ctrl+Shift+G` on Windows). Both use the same repository. Git works locally;
you do not need a GitHub account or an internet connection.

The examples use a `servers.txt` file listing server names such as `web-01` and
`db-01`. Replace example file names, messages, and tag names with your own.

## Key Ideas

| Term          | Meaning                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------- |
| Repository    | A project folder and its Git history. The history is stored in the `.git` folder.               |
| Working files | The files you edit and save in your project folder.                                             |
| Staging area  | The changes you have selected for the next commit.                                              |
| Commit        | A saved snapshot in Git history, with a message describing the changes.                         |
| Tag           | A name that marks a particular commit. An annotated tag also has a message, tagger, and date.   |
| `.gitignore`  | A file listing patterns for files Git should not start tracking, such as a virtual environment. |

Saving a file in VS Code is not the same as committing it. Save the file, stage
the changes you want, and then commit them.

## Create or Open a Repository

Open the project folder in VS Code using `File > Open Folder...`. Run Git
commands from that folder in the terminal.

| Task                                      | Git command                     | VS Code                                                |
| ----------------------------------------- | ------------------------------- | ------------------------------------------------------ |
| Create a repository in the current folder | `git init`                      | In Source Control, select `Initialize Repository`.     |
| Check the repository and its changes      | `git status`                    | View `Changes` and `Staged Changes` in Source Control. |
| Show the repository root folder           | `git rev-parse --show-toplevel` | Run the Git command in the terminal.                   |

Before creating a repository, use `git status` to check whether the folder is
already in one. If it is, use `git rev-parse --show-toplevel` to identify its
root. Avoid creating a repository inside another repository. Project setup tools
may already have created a repository.

## Commit Identity

Git records a name and email with commits and annotated tags. If they are not
already configured, set them in the repository:

```powershell
git config --local user.name "Your Name"
git config --local user.email "you@example.com"
```

Replace the example values with the name and email you want recorded in your
history. These are not login credentials. The `--local` option applies only to
this repository; repeat this setup in another repository if needed.

## Review, Stage, and Commit Changes

| Task                                     | Git command                                                 | VS Code Source Control                             |
| ---------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------- |
| See changed, untracked, and staged files | `git status`                                                | Check `Changes` and `Staged Changes`.              |
| Review unstaged edits to tracked files   | `git diff`                                                  | Select a file under `Changes`.                     |
| Stage a file                             | `git add servers.txt`                                       | Select `+` beside the file under `Changes`.        |
| Stage all changes                        | `git add .`                                                 | Select `+` beside `Changes`.                       |
| Review staged changes                    | `git diff --staged`                                         | Select a file under `Staged Changes`.              |
| Unstage a file without deleting edits    | `git restore --staged servers.txt` (after the first commit) | Select `-` beside the file under `Staged Changes`. |
| Commit staged changes                    | `git commit -m "Update server inventory"`                   | Enter a message and select `Commit`.               |

A new file is untracked until it is staged. Staging records the file's contents
at that moment. If you edit and save it again before committing, stage it again
to include the new changes. Unstaging keeps your edits; discarding changes can
delete them.

From the repository root, `git add .` stages new, modified, and deleted files,
except untracked files matching `.gitignore`. When a file is moved, Git may show
a deletion at the old location and a new file at the new location. Stage both.
Check the staged changes before committing so you do not include unwanted files.

## Ignore Files

The `.gitignore` file lists files and folders Git should not start tracking. For
example, a Python repository might contain:

```gitignore
.venv/
__pycache__/
.pytest_cache/
```

These patterns keep untracked virtual environment and cache files out of
commits. A file already tracked by Git stays tracked even if you later add it to
`.gitignore`. Do not commit passwords, tokens, or other secrets.

Commit `.gitignore` and the files needed for the project, such as
`pyproject.toml`, `uv.lock`, and any required VS Code configuration.

## History and Annotated Tags

| Task                      | Git command                                      | VS Code                                          |
| ------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| View commit history       | `git log --oneline`                              | Expand `Source Control Graph` in Source Control. |
| Create an annotated tag   | `git tag -a inventory-v1 -m "Initial inventory"` | Run the Git command in the terminal.             |
| List tags and messages    | `git tag -n`                                     | Run the Git command in the terminal.             |
| View a tag and its commit | `git show --no-patch inventory-v1`               | Run the Git command in the terminal.             |

In the tag example, `-a` creates an annotated tag and `-m` supplies its message.
Without a commit specified, the tag marks the latest commit, not uncommitted
changes. Commit the changes you want to include before tagging. Later commits do
not move the tag. `git show` displays the tagger, message, and tagged commit.

If Git displays a long result one screen at a time, press `q` to return to the
terminal.

## Archive a Repository

The `.git` folder contains the repository history and tags. If a ZIP must
include Git history, include `.git` and check that it is in the ZIP. On Windows,
enable `View > Show > Hidden items` in File Explorer if `.git` is hidden.
`.gitignore` controls Git tracking, not which files are included in a ZIP.

## References

- [Git](https://git-scm.com/book/en/v2)
- [Source control in VS Code](https://code.visualstudio.com/docs/sourcecontrol/overview)
