#!/usr/bin/env pwsh
# Setup curriculum for both tracks on deployment

Write-Host "🚀 Setting up ApraNova Curriculum..." -ForegroundColor Cyan

# Run DP curriculum setup
Write-Host "📊 Setting up Data Professional track..." -ForegroundColor Yellow
python setup_dp_curriculum.py

# Run FSD curriculum setup
Write-Host "💻 Setting up Full Stack Development track..." -ForegroundColor Yellow
python setup_fsd_curriculum.py

Write-Host "✅ Curriculum setup complete!" -ForegroundColor Green
