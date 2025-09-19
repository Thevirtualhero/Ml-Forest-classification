# PowerShell helper to install Git LFS and track file types for this repo
# Run this from the repository root.

# 1) Ensure Git LFS is installed. On Windows, use Winget if available, otherwise use the installer from https://git-lfs.github.com/
# winget install --id Git.GitLFS -e --source winget

# 2) Initialize Git LFS for the repository and track the configured patterns
git lfs install --local

# Track file patterns that are common for datasets and models
git lfs track "*.csv"
git lfs track "*.pkl"
git lfs track "*.joblib"
git lfs track "*.h5"
git lfs track "*.pt"

# Show .gitattributes
Get-Content .gitattributes -ErrorAction SilentlyContinue

Write-Host "Git LFS setup complete. Commit .gitattributes and push. Example:" -ForegroundColor Green
Write-Host "git add .gitattributes" -ForegroundColor Yellow
Write-Host "git commit -m 'Add .gitattributes for Git LFS'" -ForegroundColor Yellow
Write-Host "git push origin clean-main" -ForegroundColor Yellow
