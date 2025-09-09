#!/bin/bash

# Cloud Architecture Exercise - GitHub Upload Script
# This script helps upload the project to GitHub

set -e

echo "🚀 Cloud Architecture Exercise - GitHub Upload Helper"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Please run 'git init' first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "app.py" ]; then
    echo "❌ Please run this script from the project root directory."
    exit 1
fi

echo "✅ Git repository found"
echo "✅ Project files found"

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

# Repository name
REPO_NAME="cloud-architecture-exercise"
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo "📋 Repository Details:"
echo "   Username: $GITHUB_USERNAME"
echo "   Repository: $REPO_NAME"
echo "   URL: $REPO_URL"
echo ""

# Confirm before proceeding
read -p "Do you want to proceed with the upload? (y/N): " CONFIRM

if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "❌ Upload cancelled"
    exit 0
fi

echo ""
echo "🔄 Setting up remote repository..."

# Add remote origin
git remote add origin $REPO_URL 2>/dev/null || {
    echo "⚠️  Remote origin already exists, updating URL..."
    git remote set-url origin $REPO_URL
}

echo "✅ Remote repository configured"

# Check if there are any uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  There are uncommitted changes. Committing them now..."
    git add .
    git commit -m "Update: prepare for GitHub upload"
fi

echo "🔄 Pushing to GitHub..."

# Push to GitHub
git push -u origin main

echo ""
echo "🎉 Success! Your repository has been uploaded to GitHub!"
echo "📍 Repository URL: $REPO_URL"
echo ""
echo "📋 Next Steps:"
echo "1. Visit your repository on GitHub"
echo "2. Update README.md to replace 'yourusername' with '$GITHUB_USERNAME'"
echo "3. Configure GitHub Actions secrets if you want to use CI/CD"
echo "4. Share your repository with others!"
echo ""
echo "🔧 To update the repository in the future:"
echo "   git add ."
echo "   git commit -m 'Your commit message'"
echo "   git push"
echo ""
echo "Happy coding! 🚀"
