#!/bin/bash
# setup.sh - Quick setup script for new project
# Author: Homero Thompson del Lago del Terror

set -e

echo "🚀 FastAPI Project Setup"
echo "========================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}✗ uv not found${NC}"
    echo ""
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo ""
    echo -e "${GREEN}✓ uv installed${NC}"
    echo "Please restart your shell and run this script again"
    exit 0
fi

echo -e "${BLUE}1. Installing dependencies...${NC}"
uv sync --all-extras
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

echo -e "${BLUE}2. Setting up environment file...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}→ Please edit .env with your configuration${NC}"
else
    echo -e "${YELLOW}→ .env already exists, skipping${NC}"
fi
echo ""

echo -e "${BLUE}3. Installing pre-commit hooks...${NC}"
uv run pre-commit install
echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"
echo ""

echo -e "${BLUE}4. Initializing git repository...${NC}"
if [ ! -d .git ]; then
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
else
    echo -e "${YELLOW}→ Git repository already exists${NC}"
fi
echo ""

echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "  1. Edit .env file:"
echo -e "     ${YELLOW}nano .env${NC}"
echo ""
echo "  2. Start services:"
echo -e "     ${YELLOW}make docker-up${NC}"
echo "     or"
echo -e "     ${YELLOW}docker-compose up -d${NC}"
echo ""
echo "  3. Run the application:"
echo -e "     ${YELLOW}make run${NC}"
echo "     or"
echo -e "     ${YELLOW}uv run uvicorn fastapi_project.main:app --reload${NC}"
echo ""
echo "  4. Run tests:"
echo -e "     ${YELLOW}make test${NC}"
echo ""
echo "  5. View available commands:"
echo -e "     ${YELLOW}make help${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "📚 API Docs will be at: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
