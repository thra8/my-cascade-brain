# Cascade AI System - Identity Configuration
# System identifiers and credentials

## System Identity
- **Name**: Cascade AI System
- **Version**: 1.0.0
- **Platform**: macOS M1 (ARM64)
- **Architecture**: Multi-Agent Specialist System
- **Created**: 2025-03-15

## API Keys Configuration
- **OPENAI_API_KEY**: ${OPENAI_API_KEY}
- **ANTHROPIC_API_KEY**: ${ANTHROPIC_API_KEY}
- **GEMINI_API_KEY**: ${GEMINI_API_KEY}
- **DUCKDUCKGO_API_KEY**: ${DUCKDUCKGO_API_KEY}

## Database Identifiers
- **PROJECT_DB_ID**: ${PROJECT_DB_ID}
- **MEMORY_DB_ID**: ${MEMORY_DB_ID}
- **CACHE_DB_ID**: ${CACHE_DB_ID}

## Service Configurations
- **WINDSURF_SERVER**: ${WINDSURF_SERVER}
- **CLAUDE_API_ENDPOINT**: ${CLAUDE_API_ENDPOINT}
- **GITHUB_TOKEN**: ${GITHUB_TOKEN}

## Performance Targets
- **Frame Budget**: 16ms (60 FPS)
- **Memory Limit**: 4GB for stack operations
- **Response Time**: <100ms for commands
- **Concurrency**: 1000+ concurrent operations

## Security Settings
- **Encryption**: AES-256 for sensitive data
- **Authentication**: JWT tokens with 24h expiry
- **Rate Limiting**: 100 requests per minute
- **Audit Logging**: All operations tracked
