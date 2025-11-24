#!/bin/bash
# Setup curriculum for both tracks on deployment

echo "🚀 Setting up ApraNova Curriculum..."

# Run DP curriculum setup
echo "📊 Setting up Data Professional track..."
python setup_dp_curriculum.py

# Run FSD curriculum setup
echo "💻 Setting up Full Stack Development track..."
python setup_fsd_curriculum.py

echo "✅ Curriculum setup complete!"
