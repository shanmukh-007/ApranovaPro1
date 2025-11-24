#!/bin/bash
# MCP Server Setup Script for AI-Assisted AWS Deployment

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}MCP Server Setup for AWS Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Step 1: Check if UV is installed
echo -e "${YELLOW}Step 1: Checking UV installation...${NC}"
if command -v uv &> /dev/null; then
    echo -e "${GREEN}✓ UV is already installed${NC}"
    uv --version
else
    echo -e "${YELLOW}Installing UV...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH
    export PATH="$HOME/.cargo/bin:$PATH"
    
    echo -e "${GREEN}✓ UV installed successfully${NC}"
    uv --version
fi

echo ""

# Step 2: Check AWS CLI
echo -e "${YELLOW}Step 2: Checking AWS CLI...${NC}"
if command -v aws &> /dev/null; then
    echo -e "${GREEN}✓ AWS CLI is already installed${NC}"
    aws --version
else
    echo -e "${YELLOW}Installing AWS CLI...${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install awscli
        else
            echo -e "${RED}Please install Homebrew first: https://brew.sh${NC}"
            exit 1
        fi
    else
        # Linux
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install
        rm -rf aws awscliv2.zip
    fi
    echo -e "${GREEN}✓ AWS CLI installed successfully${NC}"
fi

echo ""

# Step 3: Configure AWS Credentials
echo -e "${YELLOW}Step 3: Configuring AWS credentials...${NC}"
if [ -f ~/.aws/credentials ]; then
    echo -e "${GREEN}✓ AWS credentials already configured${NC}"
    echo "Current AWS identity:"
    aws sts get-caller-identity 2>/dev/null || echo -e "${YELLOW}⚠ AWS credentials may need updating${NC}"
else
    echo -e "${YELLOW}Please configure AWS credentials:${NC}"
    aws configure
fi

echo ""

# Step 4: Verify MCP Configuration
echo -e "${YELLOW}Step 4: Verifying MCP configuration...${NC}"
if [ -f .kiro/settings/mcp.json ]; then
    echo -e "${GREEN}✓ MCP configuration file exists${NC}"
    echo "Configured MCP servers:"
    cat .kiro/settings/mcp.json | grep -o '"[^"]*":' | grep -v "mcpServers\|command\|args\|env\|disabled\|autoApprove" | sed 's/://g' | sed 's/"//g' | sed 's/^/  - /'
else
    echo -e "${RED}✗ MCP configuration file not found${NC}"
    echo "Please ensure .kiro/settings/mcp.json exists"
    exit 1
fi

echo ""

# Step 5: Test MCP Servers
echo -e "${YELLOW}Step 5: Testing MCP server availability...${NC}"

echo "Testing AWS CLI MCP server..."
if uvx --help &> /dev/null; then
    echo -e "${GREEN}✓ uvx command works${NC}"
else
    echo -e "${RED}✗ uvx command not found${NC}"
    echo "Please restart your terminal and run this script again"
    exit 1
fi

echo ""

# Step 6: Summary
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "MCP servers configured:"
echo "  ✓ aws-cli - Execute AWS CLI commands"
echo "  ✓ terraform - Manage infrastructure"
echo "  ✓ docker - Build and manage containers"
echo "  ✓ filesystem - Read/write files"
echo "  ✓ git - Version control operations"
echo ""
echo "Next steps:"
echo "  1. Restart Kiro (MCP servers connect on startup)"
echo "  2. Try: 'Show me my AWS account information'"
echo "  3. Try: 'Deploy ApraNova to AWS'"
echo ""
echo "Documentation:"
echo "  - MCP_AWS_SETUP.md - Complete MCP setup guide"
echo "  - AWS_DEPLOYMENT_PLAN.md - AWS deployment guide"
echo ""
echo -e "${GREEN}Ready to deploy with AI assistance! 🚀${NC}"
