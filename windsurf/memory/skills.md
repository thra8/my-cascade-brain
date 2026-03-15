# Expert Skills Vault - Cascade AI System

## 3D Graphics & Rendering
### M1 Native Optimization
- **Pattern**: NumPy vectorization instead of pixel loops
- **Performance**: 68.8 FPS achieved with 16ms frame budget
- **Braille Unicode**: U+2800 mapping for 2x8 resolution
- **Double Buffering**: Prevents flicker in animations
- **Accelerate Framework**: Apple's vector libraries integration

### Rendering Pipeline
- **No Pixel Loops**: Strict NumPy broadcasting
- **Frame Budget**: 16ms for 60 FPS target
- **Memory Pooling**: Reuse buffers to avoid allocations
- **Thermal Management**: Monitor M1 temperature and adjust load

## Color Systems & Terminal Graphics
### TrueColor Implementation
- **Priority**: 24-bit RGB with ANSI 256 fallback
- **HEX Formats**: Support for #RGB, #RRGGBB, #RRGGBBAA
- **WCAG Compliance**: Contrast ratio calculations for accessibility
- **Unicode Dithering**: Smooth gradients in terminal

### Color Harmonies
- **HSL Space**: Generate complementary, triadic, analogous
- **Accessibility**: Ensure WCAG AA/AAA compliance
- **Terminal Limits**: Work within 256 color fallback
- **Performance**: Vectorized calculations for gradients

## DevOps & System Architecture
### Stack Health Monitoring
- **Port Management**: Check availability before service launch
- **Process Detection**: Identify and kill conflicting processes
- **Resource Monitoring**: CPU, memory, disk, network tracking
- **Auto-Recovery**: Restart failed services automatically

### M1 Optimization Patterns
- **Worker Calculation**: (2 * cpu_count) + 1 for FastAPI
- **CPU Affinity**: P-cores for performance, E-cores for background
- **Memory Limits**: 512MB per worker, <4GB total stack
- **Native Dependencies**: ARM64-specific installations

## AI Agent Architecture
### Devin-like Planning System
- **Think Before Act**: Plan before execution
- **Self-Evolution**: Learn from corrections and feedback
- **Lessons Learned**: Store reusable patterns
- **Scratchpad System**: Organize thoughts and progress

### Multi-Agent Coordination
- **Planner Agent**: o1-like strategic planning
- **Executor Agent**: Claude/GPT-like implementation
- **Cross-Checking**: Validate results between agents
- **Iterative Improvement**: Refine based on feedback

## Memory & Knowledge Management
### Dual Memory System
- **System 1**: Programming concepts, business logic, past interactions
- **System 2**: Reasoning steps, decision processes, tool usage
- **Vector Storage**: Semantic search with embeddings
- **Knowledge Graph**: Relationship mapping between concepts

### MCP Integration
- **Universal Compatibility**: Cursor, Windsurf, Claude Code, VS Code
- **Real-time Communication**: WebSocket synchronization
- **Session Management**: Persistent sessions across IDEs
- **Tool Integration**: Native IDE tool support

## Spec-Driven Development
### Workflow Integration
- **6 Steps**: spec → plan → tasks → implement → review → merge
- **Repository Artifacts**: spec.md, plan.md, tasks.md
- **Work Packages**: Lane-based execution (planned → doing → for_review → done)
- **Git Worktrees**: Isolated parallel development

### Multi-Agent Support
- **12 Agents**: Claude Code, Cursor, Codex, Gemini, Copilot, etc.
- **Agent Management**: Centralized configuration
- **Template Generation**: Agent-specific templates
- **Coordination**: Parallel execution with conflict resolution

## Performance Optimization
### M1 Specific Patterns
- **Accelerate Framework**: Use Apple's vector libraries
- **Memory Alignment**: Optimize for cache efficiency
- **Thermal Throttling**: Monitor and adjust for temperature
- **GPU Utilization**: Balance CPU/GPU workloads

### Terminal Graphics Performance
- **Unicode Rendering**: Use Braille for 2x8 resolution
- **Color Management**: TrueColor with fallbacks
- **Frame Timing**: Consistent 16ms budget
- **Memory Efficiency**: Pool and reuse buffers

## Error Handling & Validation
### Graceful Degradation
- **Fallback Systems**: Multiple levels of functionality
- **Error Recovery**: Automatic retry with backoff
- **User Feedback**: Clear error messages and suggestions
- **Logging**: Comprehensive error tracking

### Validation Patterns
- **Input Validation**: Type checking and sanitization
- **Output Verification**: Result validation before return
- **State Consistency**: Maintain valid system state
- **Resource Cleanup**: Proper resource management

## Integration Patterns
### System Coordination
- **Event-Driven**: React to system changes
- **State Management**: Centralized state tracking
- **Message Passing**: Clear communication between components
- **Modularity**: Independent, reusable components

### Memory Integration
- **Context Loading**: Load relevant memories before tasks
- **Pattern Recognition**: Identify and apply learned patterns
- **Continuous Learning**: Update knowledge base from interactions
- **Compression**: Optimize memory usage
