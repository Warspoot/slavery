#!/bin/bash
# Setup script for Umamusume Autoplay

echo "Setting up Umamusume Autoplay virtual environment..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "Next steps:"
echo "1. Extract templates: python extract_templates.py"
echo "2. Test template extraction: ls -la templates/"
echo "3. Run in test mode (see test_automation.py)"
