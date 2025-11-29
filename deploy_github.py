#!/usr/bin/env python3
"""
GitHub Deployment Script for Student Performance Predictor
This script helps set up and deploy the project to GitHub
"""

import subprocess
import os
import sys

def run_command(command, description):
    """Run a shell command and return success status"""
    print(f"\n📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Student Performance Predictor - GitHub Deployment")
    print("=" * 60)

    # Change to project directory
    project_dir = r"c:\Users\vvign\.gemini\antigravity\scratch\student-performance-predictor"
    os.chdir(project_dir)
    print(f"📁 Working directory: {project_dir}")

    # Step 1: Initialize Git repository
    if not os.path.exists('.git'):
        if not run_command("git init", "Initializing Git repository"):
            return False
    else:
        print("📋 Git repository already initialized")

    # Step 2: Add .gitignore and README.md first
    if not run_command("git add .gitignore README.md", "Adding gitignore and README files"):
        return False

    # Step 3: Initial commit
    if not run_command('git commit -m "Initial commit: Student Performance Predictor v1.1"', "Creating initial commit"):
        return False

    # Step 4: Add all other files
    if not run_command("git add .", "Adding all project files"):
        return False

    # Step 5: Final commit
    if not run_command('git commit -m "Complete Student Performance Predictor application

- ML-powered student performance prediction using XGBoost
- Multi-role dashboards (Student, Teacher, Parent)
- Real-time predictions and risk assessment
- Multi-language support (6 languages)
- CSV import/export functionality
- SQLite database integration
- Responsive web interface with Streamlit"', "Committing complete application"):
        return False

    # Step 6: Show status
    print("\n📊 Repository Status:")
    run_command("git status", "Checking repository status")

    print("\n📝 Next Steps for GitHub Deployment:")
    print("=" * 60)
    print("1. Create a new repository on GitHub:")
    print("   - Go to https://github.com/new")
    print("   - Repository name: student-performance-predictor")
    print("   - Make it public or private")
    print("   - DON'T initialize with README (we already have one)")

    print("\n2. Copy the repository URL from GitHub")

    print("\n3. Add GitHub remote and push:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/student-performance-predictor.git")
    print("   git branch -M main")
    print("   git push -u origin main")

    print("\n4. Optional: Deploy to Streamlit Cloud")
    print("   - Go to https://share.streamlit.io")
    print("   - Connect your GitHub repository")
    print("   - Deploy the app")

    print("\n✨ Your project is ready for GitHub deployment!")
    print("🎯 Repository contains: ML models, web app, documentation, and all features")

if __name__ == "__main__":
    main()
