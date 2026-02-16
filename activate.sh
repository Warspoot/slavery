#!/bin/bash
# Quick activation script for the virtual environment

if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Run ./setup.sh first to create it."
    exit 1
fi

source venv/bin/activate

echo "Virtual environment activated!"
echo ""
echo "Quick commands:"
echo "  python extract_templates.py          - Extract button templates"
echo "  python test_automation.py            - Test the setup"
echo "  python umamusume_autoplay.py --help  - Show automation options"
echo ""
echo "To deactivate: deactivate"
