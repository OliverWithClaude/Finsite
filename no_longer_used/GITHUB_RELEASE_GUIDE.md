# GitHub Release Guide - Finsite v1.0

## Pre-Release Checklist

Before creating the release, ensure:

- [ ] All code is committed and pushed to main branch
- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] Release notes are finalized
- [ ] Version number is updated in `app/version.py`
- [ ] CHANGELOG is updated (if you have one)

## Step-by-Step Release Process

### Step 1: Final Commit

Commit all your changes with the release:

```bash
cd C:\Claude\Finsite
git add .
git commit -m "Release v1.0.0 - Foundation

- Complete position tracking system
- Open/closed position management
- Live market data integration
- Delete functionality for closed positions
- Simplified close workflow
- Full documentation and release notes"
```

### Step 2: Create Git Tag

Create an annotated tag for the release:

```bash
git tag -a v1.0.0 -m "Finsite v1.0.0 - Foundation Release

First official release of Finsite investment workbench.

Major Features:
- Watchlist management with live market data
- Open position tracking with real-time valuations
- Closed position history with P&L analysis
- SQLite database for local storage
- Clean, responsive UI with Optimistic Grit design"
```

### Step 3: Push to GitHub

Push both your commits and the tag:

```bash
# Push commits
git push origin main

# Push tags
git push origin --tags
```

Or push everything at once:

```bash
git push --follow-tags origin main
```

### Step 4: Create GitHub Release

#### Option A: Via GitHub Web Interface (Recommended)

1. **Navigate to your repository** on GitHub
   - Go to https://github.com/yourusername/finsite

2. **Go to Releases**
   - Click "Releases" in the right sidebar
   - OR go to https://github.com/yourusername/finsite/releases

3. **Draft a new release**
   - Click "Draft a new release" button

4. **Choose tag**
   - Select `v1.0.0` from the dropdown
   - Or type `v1.0.0` to create a new tag

5. **Release title**
   - Enter: `Finsite v1.0.0 - Foundation`

6. **Release description**
   - Copy content from `RELEASE_NOTES_v1.0.md`
   - Or write a summary with key highlights

7. **Attach files (optional)**
   - You can attach a ZIP of the source code
   - Or any additional documentation

8. **Set as latest release**
   - Check "Set as the latest release"

9. **Publish**
   - Click "Publish release" button

#### Option B: Via GitHub CLI

If you have GitHub CLI installed:

```bash
# Install GitHub CLI first if needed
# See: https://cli.github.com/

# Create release
gh release create v1.0.0 \
  --title "Finsite v1.0.0 - Foundation" \
  --notes-file RELEASE_NOTES_v1.0.md \
  --latest
```

### Step 5: Verify Release

1. Check the release appears on GitHub: 
   - https://github.com/yourusername/finsite/releases/tag/v1.0.0

2. Verify the tag exists:
   ```bash
   git tag -l
   ```

3. Test downloading the release:
   - Download ZIP from GitHub
   - Extract and verify files

## What Your Release Should Include

### Mandatory Files (should be in repo)
- ✅ `README.md` - Updated project documentation
- ✅ `RELEASE_NOTES_v1.0.md` - Detailed release notes
- ✅ `requirements.txt` - Python dependencies
- ✅ `LICENSE` - License file
- ✅ `setup.bat` - Setup script
- ✅ `start_server.bat` - Start script
- ✅ All source code in `app/`, `static/`, `templates/`

### Optional Files (good to have)
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines
- `.gitignore` - Git ignore rules
- `screenshots/` - Application screenshots

## Post-Release Tasks

### 1. Update Development Branch

If you work on a develop branch:

```bash
git checkout develop
git merge main
git push origin develop
```

### 2. Announce the Release

Share your release:
- LinkedIn
- Twitter
- Reddit (r/Python, r/algotrading)
- Dev.to
- Your blog

### 3. Create Milestones

Plan next version:
- Create GitHub milestone for v1.1
- Add feature ideas as issues
- Tag them with milestone

### 4. Monitor Issues

Watch for bug reports:
- Check GitHub issues
- Be ready to create hotfix if needed

## Quick Reference Commands

### Common Git Commands for Releases

```bash
# View all tags
git tag -l

# View tag details
git show v1.0.0

# Delete local tag (if mistake)
git tag -d v1.0.0

# Delete remote tag (if mistake)
git push origin --delete v1.0.0

# List all releases
gh release list

# View release details
gh release view v1.0.0

# Edit release
gh release edit v1.0.0
```

## Troubleshooting

### Tag Already Exists

If tag exists locally:
```bash
git tag -d v1.0.0
git tag -a v1.0.0 -m "Your message"
git push origin v1.0.0 --force
```

### Push Fails

If push is rejected:
```bash
# Pull latest changes
git pull origin main --rebase

# Then push
git push origin main --follow-tags
```

### Wrong Version Number

If you tagged wrong version:
```bash
# Delete tag locally and remotely
git tag -d v1.0.0
git push origin --delete v1.0.0

# Create new tag
git tag -a v1.0.1 -m "Corrected version"
git push origin v1.0.1
```

## Semantic Versioning

Finsite follows semantic versioning (semver):

- **MAJOR** version (1.x.x): Incompatible API changes
- **MINOR** version (x.1.x): New functionality, backward compatible
- **PATCH** version (x.x.1): Bug fixes, backward compatible

Examples:
- `v1.0.0` - Initial release
- `v1.1.0` - Add new features (e.g., charts)
- `v1.0.1` - Bug fixes for v1.0.0
- `v2.0.0` - Major rewrite or breaking changes

## Release Checklist Template

Copy this for each release:

```markdown
## Release Checklist - v1.0.0

### Pre-Release
- [ ] All features complete
- [ ] All bugs fixed
- [ ] Code reviewed
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Version bumped in code
- [ ] Release notes written
- [ ] CHANGELOG updated

### Release
- [ ] Final commit pushed
- [ ] Tag created and pushed
- [ ] GitHub release created
- [ ] Release verified

### Post-Release
- [ ] Development branch updated
- [ ] Announcement posted
- [ ] Next milestone created
- [ ] Monitoring for issues
```

## Example Release Notes Format

```markdown
# Finsite v1.0.0 - Foundation

## 🎉 Highlights
- Major new feature
- Important improvement
- Breaking change

## ✨ New Features
- Feature 1 (#123)
- Feature 2 (#124)

## 🐛 Bug Fixes
- Fix 1 (#125)
- Fix 2 (#126)

## 📝 Documentation
- Updated README
- Added new guides

## 🙏 Credits
Thanks to all contributors!

**Full Changelog**: https://github.com/user/finsite/compare/v0.9.0...v1.0.0
```

---

## Next Steps

After completing these steps, you'll have:
- ✅ Code committed and tagged
- ✅ Release published on GitHub
- ✅ Version available for download
- ✅ Clear documentation for users

**Your release is complete!** 🎉

Users can now:
1. Visit your releases page
2. Download the source code
3. Follow the README to get started
