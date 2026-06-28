# Git & GitHub Cheatsheet (Jigar's reference)

> Written by Hedwig as a teaching aid. Re-read this whenever the muscle
> memory fades. Understanding > automation.

## Mental model
- **Git** = the version-control tool (runs on your laptop, works offline).
- **GitHub** = a website that *hosts* a copy of your Git repo (backup + sharing).
- Two repos exist: your **local** repo (`.git/` folder) and the **remote** on GitHub.

### The four zones a change passes through
```
Working Dir  --git add-->  Staging  --git commit-->  Local History  --git push-->  GitHub
                                                                     <--git pull--
```
- Staging = the box you're packing.
- Commit = sealing + labeling the box.
- Push = shipping the box to GitHub's warehouse.

## Why SSH key auth?
GitHub killed plain passwords for git (Aug 2021). Two ways to authenticate:
- **HTTPS + Personal Access Token** — type/cache a token each push.
- **SSH key** — a cryptographic keypair; passwordless after setup. (We use this.)

### How the keypair works
- **Private key** `~/.ssh/id_ed25519` — SECRET. Never leaves your laptop. Never share.
- **Public key** `~/.ssh/id_ed25519.pub` — safe to share; pasted into GitHub settings.
- On push: GitHub challenges you; your client signs it with the PRIVATE key;
  GitHub verifies with the PUBLIC key on your account. Match -> access. The
  private key never travels the network.
- `Permission denied (publickey)` = GitHub has no matching public key on file.

### Port-443 workaround (corporate firewall blocks SSH port 22)
`~/.ssh/config` block routes github.com over port 443:
```
Host github.com
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile ~/.ssh/id_ed25519
  AddKeysToAgent yes
```
Test it: `ssh -T git@github.com`  -> should greet you by username.

## One-time setup for a NEW project
```bash
git init                                  # create local repo
git config user.name  "Your Name"         # identity on commits (this repo)
git config user.email "you@example.com"   # GitHub matches commits via email
git add -A                                # stage everything
git commit -m "Initial commit"            # first snapshot
git remote add origin git@github.com:USER/REPO.git   # link to GitHub (SSH)
git push -u origin main                    # push + set upstream tracking
```

## Connecting to an EXISTING GitHub repo that already has content
```bash
git remote add origin git@github.com:USER/REPO.git
git fetch origin                                   # see what's there (no file changes)
git merge origin/main --allow-unrelated-histories  # combine separate histories
#   ^ resolve any conflicts, then: git add <file> && git commit
git push -u origin main
```

## Everyday loop (95% of git usage)
```bash
git status                 # what changed? run this CONSTANTLY
git add <file>             # stage a file (git add -A = everything)
git commit -m "message"    # snapshot
git push                   # send to GitHub
git pull                   # pull others'/other-machine's changes first
```

## Inspecting
```bash
git log --oneline          # compact history
git diff                   # unstaged changes
git diff --staged          # staged changes
git branch -vv             # branches + upstream tracking + latest commit
git remote -v              # show remote URLs
```

## Glossary
- **origin** = conventional nickname for your main remote (just a bookmark to a URL).
- **upstream / tracking** = the link between local `main` and `origin/main`;
  set by `git push -u`. Once set, `git push`/`git pull` need no arguments.
- **commit hash** = unique id of a snapshot (e.g. `3eca186`).
- **HEAD** = pointer to your current commit/branch.
- **--allow-unrelated-histories** = permit merging two repos that began separately.
