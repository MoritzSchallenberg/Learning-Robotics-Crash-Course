# Git

{{ common }}

Every team at the institute keeps its robot software in Git. You will spend
more time reading history and merging branches than you expect, so it is worth
learning the workflow properly rather than memorising three commands.

## Learning objectives

After this page you can:

- configure Git with an identity that your team will accept;
- clone a repository over HTTPS or SSH and know when to use which;
- create a branch following the MASKOR naming conventions;
- write a commit message in the expected format;
- recover from the two situations that scare beginners most — a detached HEAD
  and a diverged branch.

## Prerequisites

[Linux and the terminal](linux-terminal.md), and a GitHub account.

## Set up your identity

Git stamps every commit with a name and an email. Set them once, globally:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.name@example.org"
```

Use the address that is registered with your GitHub account, otherwise your
commits will not be linked to you.

Set the editor Git opens for commit messages and interactive rebases:

```bash
git config --global core.editor "nano"    # or "vim", or "code --wait"
```

## SSH keys

Cloning over **HTTPS** is fine for repositories you only read. As soon as you
push, use **SSH** — then Git authenticates with your key instead of asking for
credentials.

Generate a key if you do not have one:

```bash
ssh-keygen -t ed25519 -C "your.name@example.org"
```

Print the public half and add it to GitHub under
*Settings → SSH and GPG keys*:

```bash
cat ~/.ssh/id_ed25519.pub
```

:::{danger}
Only ever copy the `.pub` file. The file without the extension is your
**private** key: it never leaves your machine, is never committed, and is never
pasted into a chat.
:::

Check which protocol a clone is using, and switch it if needed:

```bash
git remote -v
git remote set-url origin git@github.com:<org>/<repo>.git
```

## Branches

The MASKOR teams use a simple scheme:

```text
<scope>/<branch-name>
```

`<scope>` is normally your abbreviated name — first initial plus surname, so
`jdoe` for a Jane Doe — or `common` if several people will work on the branch
together.

```bash
git switch -c jdoe/fix-laser-frame
```

Development branches are kept up to date with `git rebase` rather than repeated
merges, which keeps the history readable.

## Commit messages

Two conventions the teams enforce:

- lines wrap at **80 characters**;
- the first line has the form `<prefix>: <description>`, where the prefix names
  the component you touched.

```text
laser_scan: fix frame_id of the merged scan

The integrator published in base_link while the driver publishes in
laser_frame, which made RViz place the scan half a metre off.
```

If you are unsure which prefix to use, look at what previous commits to the
same file used:

```bash
git log --oneline -- path/to/file
```

## pre-commit hooks

The teams run automated formatting and lint checks through
[pre-commit](https://pre-commit.com/). Install it in every repository that has
a `.pre-commit-config.yaml`:

```bash
pip install pre-commit
pre-commit install
```

From then on, checks run automatically when you commit. If a hook rewrites your
files, stage the changes and commit again.

:::{warning}
`git commit --no-verify` skips the hooks. It exists for genuine emergencies.
Using it routinely means the server-side checks will reject your work later,
which wastes more time than the hooks ever cost you.
:::

## Commands worth knowing

### Staging selectively

```bash
git add -p        # step through your changes hunk by hunk
git reset -p      # unstage selectively
git checkout -p   # discard selectively -- careful, this loses work
```

`git add -p` is the single habit that most improves the quality of commits: it
forces you to look at what you are about to commit.

### Fixing the previous commit

```bash
git add -p
git commit --amend
```

### Fixing an older commit

```bash
git log                                    # find the commit hash
git commit --fixup=<commit-hash>           # create a fixup commit
git rebase -i --autosquash origin/main     # squash it into place
```

### Undoing almost anything

```bash
git reflog                     # every position HEAD has had
git reset HEAD@{3}             # go back to one of them
```

`git reflog` is the safety net. Almost nothing in Git is truly lost for the
first 90 days, as long as it was committed at least once.

## Two situations that look worse than they are

### Detached HEAD

You checked out something that is not a branch — a tag, a commit hash, or a
remote branch (`origin/jdoe/fix` instead of `jdoe/fix`). Commits you make here
belong to no branch.

Fix it by deciding what you actually wanted:

```bash
git switch main                        # go back to a branch, discarding nothing
git switch -c jdoe/new-branch          # keep your work on a new branch
```

### A diverged branch

```text
Your branch and 'origin/jdoe/fix' have diverged,
and have 2 and 4 different commits each, respectively.
```

Usually this means someone force-pushed a rebase. Find out what actually
differs before doing anything:

```bash
git diff origin/jdoe/fix
```

Then pick the appropriate resolution:

- **Your local commits are the ones worth keeping** — rebase them onto the
  remote:

  ```bash
  git rebase -i origin/jdoe/fix
  ```

- **The remote is right and your local commits are stale** — reset to it:

  ```bash
  git reset --hard origin/jdoe/fix
  ```

  :::{danger}
  `git reset --hard` deletes every local commit on the branch **and** every
  uncommitted change to tracked files. Run `git status` and `git diff` first,
  every time.
  :::

- **The remote is wrong and you are certain** — force-push. This rewrites
  history that others may already have pulled, so confirm with your team first,
  and prefer `git push --force-with-lease` over `git push -f` because it
  refuses to clobber commits you have not seen.

## Working with Git on a robot

Robots normally have no push permission, deliberately: nobody can tell who made
a commit that came from a shared machine. So when you change code on a robot,
move the change to your own machine as a patch:

```bash
# on the robot
git diff > my-change.diff

# copy it to your machine
scp <robot>:my-change.diff .

# on your machine
git apply my-change.diff
```

## Task

:::{admonition} Task: a complete cycle
:class: task

Using any repository you own:

1. Configure your name and email, and verify with `git config --list`.
2. Create a branch following the `<scope>/<name>` convention.
3. Make two small changes to a file. Commit them as **two separate commits**
   using `git add -p`.
4. Notice a typo in the first commit. Fix it with `git commit --fixup` and
   squash it with an interactive autosquash rebase.
5. Inspect the resulting history with `git log --oneline`.
:::

:::{admonition} Expected result
:class: result

`git log --oneline` shows exactly two commits on your branch, each with a
`<prefix>: <description>` first line, and no leftover `fixup!` commit.
:::

## Common mistakes

**Committing with the wrong email.**
The commits will not be attributed to you on GitHub. Fix your config, and ask
your team lead before rewriting history that is already pushed.

**Committing build output.**
`build/`, `install/` and `log/` never belong in a repository. Check the
repository's `.gitignore` before your first commit.

**Committing credentials.**
Never commit a password, token, key or private configuration file — and this
repository is public, so treat everything as visible to the world. If it
happens, tell your team immediately: the secret must be rotated, because
deleting the commit does not remove it from clones.

## Further reading

- [Pro Git](https://git-scm.com/book/en/v2) — free, and genuinely the best
  reference
- [Git rebase documentation](https://git-scm.com/docs/git-rebase)
- [pre-commit](https://pre-commit.com/)
