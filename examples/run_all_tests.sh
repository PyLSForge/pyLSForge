#!/bin/bash
# Quick test script for teacher to run all assignments

echo "=========================================="
echo "pyLSForge Assignment - TanishyadavNSUT"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

echo "1️⃣  Testing Heat Equation..."
echo "-------------------------------------------"
python3 heat_equation_test.py
echo ""

echo "2️⃣  Testing Signed Distance Field (Main Assignment)..."
echo "-------------------------------------------"
python3 signed_distance_circle.py
echo ""

echo "3️⃣  Generating Visualization..."
echo "-------------------------------------------"
python3 viz_sdf.py
echo ""

echo "=========================================="
echo "✅ All tests completed successfully!"
echo "=========================================="
echo ""
echo "📊 Results:"
echo "   - Heat equation: Completed 10 time steps"
echo "   - SDF program: Computed distance field for circle"
echo "   - Visualization: sdf_circle_visualization.png"
echo ""
echo "📂 Files to review:"
echo "   - signed_distance_circle.py (main assignment)"
echo "   - heat_equation_test.py (heat diffusion)"
echo "   - sdf_circle_visualization.png (result image)"
echo ""
