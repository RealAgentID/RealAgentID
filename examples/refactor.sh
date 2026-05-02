#!/bin/bash
# RealAgentID - Architecture Refactor
# Run from ~/RealAgentID

set -e  # stop on any error

echo "Creating new directory structure..."
mkdir -p core api cli adapters/fintech tests examples

echo "Moving core modules..."
mv agents/audit.py core/
mv agents/connection.py core/
mv agents/db.py core/
mv agents/keygen.py core/
mv agents/registry.py core/
mv agents/schema.py core/
mv agents/signing.py core/
mv agents/tamper_test.py core/

echo "Moving test files..."
mv agents/test_attack_simulation.py tests/
mv test_attack_simulation.py tests/ 2>/dev/null || true
mv test_replay_attack.py tests/
mv test_registry_verify.py tests/

echo "Moving api..."
mv api.py api/

echo "Moving examples..."
mv demo.py examples/

echo "Moving utilities..."
mv add_ttl.py core/
mv register_agents.py core/

echo "Creating __init__.py files..."
touch core/__init__.py
touch api/__init__.py
touch cli/__init__.py
touch adapters/__init__.py
touch adapters/fintech/__init__.py
touch tests/__init__.py

echo "Cleaning up old agents dir..."
rm -rf agents/

echo "Done! New structure:"
find . -type f | grep -v '\.git' | grep -v '__pycache__' | sort
