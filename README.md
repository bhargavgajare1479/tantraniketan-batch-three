# Git and GitHub

## Check your Git version
```bash
git --version
```

## Configuring your Git credentials 
```bash
git config --global user.name "your-user-name"
git config --global user.email "your-email-id"
```

## Initialize your local repository as a Git repository
```bash
git init
```

## Add your files to staging area
```bash
git add file-name
```
or
```bash
git add .
```

## Check the status of your files - if they are tracked or untracked
```bash
git status
```

## Commit your changes to local repository 
```bash
git commit -m "your-commit-message"
```

## Add remote origin (link your GitHub repository with your local working directory)
```bash
git remote add origin your-github-repository-link
```

## Create a branch
```bash
git branch -M "your-branch-name"
```

## Push your changes to GitHub repository
```bash
git push origin "branch-name"
```
