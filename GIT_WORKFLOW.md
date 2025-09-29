# Finsite Development Workflow

## Initial Setup (One-time)

1. **Initialize Git Repository**
   ```cmd
   init_git.bat
   ```

2. **Create GitHub Repository**
   - Go to https://github.com
   - Click "New repository"
   - Name it "Finsite"
   - Don't initialize with README (we already have one)
   - Create repository

3. **Push to GitHub**
   ```cmd
   push_to_github.bat
   ```
   Enter your repository URL when prompted.

## Daily Development Workflow

### Making Changes

1. **Make your code changes**

2. **Test locally**
   ```cmd
   start_server.bat
   ```

3. **Commit changes**
   ```cmd
   commit_changes.bat
   ```

### Pulling Latest Changes

If working with others:
```cmd
git pull origin main
```

### Creating Feature Branches

For new features:
```cmd
git checkout -b feature/your-feature-name
```

After completing feature:
```cmd
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Git Commands Reference

### Basic Commands
- `git status` - Check current status
- `git add .` - Stage all changes
- `git commit -m "message"` - Commit changes
- `git push` - Push to remote repository
- `git pull` - Pull latest changes

### Branch Commands
- `git branch` - List branches
- `git checkout -b branch-name` - Create and switch to new branch
- `git checkout branch-name` - Switch to existing branch
- `git merge branch-name` - Merge branch into current branch

### Useful Commands
- `git log --oneline` - View commit history
- `git diff` - See unstaged changes
- `git stash` - Temporarily store changes
- `git stash pop` - Restore stashed changes

## Best Practices

1. **Commit Messages**
   - Use present tense ("Add feature" not "Added feature")
   - Be descriptive but concise
   - Format: `Type: Description`
   - Types: `Add:`, `Fix:`, `Update:`, `Remove:`, `Refactor:`

2. **Commit Frequency**
   - Commit logical units of work
   - Don't commit broken code
   - Commit before switching tasks

3. **Branch Strategy**
   - `main` - stable, production-ready code
   - `develop` - integration branch for features
   - `feature/*` - new features
   - `bugfix/*` - bug fixes
   - `hotfix/*` - urgent production fixes

## Troubleshooting

### Authentication Issues
If you get authentication errors:
```cmd
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Large Files
If you have large files (>100MB), consider using Git LFS:
```cmd
git lfs track "*.db"
git add .gitattributes
```

### Merge Conflicts
1. Open conflicted files
2. Look for `<<<<<<<`, `=======`, `>>>>>>>` markers
3. Resolve conflicts manually
4. Stage resolved files: `git add .`
5. Complete merge: `git commit`

## GitHub Features to Explore

1. **Issues** - Track bugs and features
2. **Projects** - Kanban boards for project management
3. **Actions** - CI/CD automation
4. **Wiki** - Documentation
5. **Releases** - Version management

## Security Notes

- Never commit sensitive data (API keys, passwords)
- Use `.env` files for configuration (already in .gitignore)
- Review code before committing
- Keep dependencies updated
