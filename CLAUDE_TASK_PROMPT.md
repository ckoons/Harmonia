# Claude Code Task for Harmonia Implementation

I need you to implement Harmonia, Tekton's workflow orchestration component. Harmonia is responsible for defining, executing, and monitoring complex workflows that coordinate tasks across the Tekton ecosystem.

Start by reviewing the following resources to understand Harmonia's purpose, requirements, and implementation plan:

1. Review the IMPLEMENTATION_GUIDE.md file in the Harmonia directory to understand the component's requirements and implementation plan.
2. Examine existing code in the Harmonia directory, particularly:
   - harmonia/client.py
   - harmonia/core/engine.py
   - harmonia/core/workflow.py
   - harmonia/core/state.py
3. Check the Tekton roadmap for Harmonia requirements (Phase 19).
4. Understand the Single Port Architecture pattern from docs/SINGLE_PORT_ARCHITECTURE.md
5. Examine the shared utilities in tekton-core/tekton/utils/ to leverage them in the implementation.

Your task is to implement Harmonia following the Tekton engineering guidelines, with specific focus on:

1. **API Implementation**:
   - Implement FastAPI endpoints following Single Port Architecture
   - Add WebSocket support for real-time updates
   - Fully document the API with OpenAPI

2. **Core Engine**:
   - Complete the workflow execution engine
   - Implement complex workflow patterns (branching, parallel, conditionals)
   - Create component integration mechanism
   - Implement execution context management

3. **State Management**:
   - Finish state persistence implementation
   - Add checkpoint and resume capabilities
   - Implement state history tracking

4. **Template System**:
   - Create workflow template models
   - Implement template repository
   - Add parameterization support

5. **Error Handling**:
   - Implement retry policies
   - Add recovery mechanisms
   - Create error notification system

6. **External Integration**:
   - Implement webhook support
   - Create event system for triggering workflows
   - Add data transformation utilities

7. **LLM Integration**:
   - Integrate with tekton-llm-client
   - Implement workflow optimization
   - Create debugging assistance

8. **UI Component**:
   - Create Hephaestus UI component for workflow management
   - Implement workflow designer
   - Add execution monitoring dashboard
   - Create workflow template management interface

**Required Deliverables**:

1. Complete API implementation with all endpoints as specified in the IMPLEMENTATION_GUIDE.md.
2. Fully functional workflow engine with support for all workflow patterns.
3. Complete state management system with checkpoint and resume capabilities.
4. Workflow template system with parameterization.
5. Error handling and recovery mechanisms.
6. External system integration capabilities.
7. LLM integration for workflow optimization and debugging.
8. Hephaestus UI component for workflow management.
9. Comprehensive test suite for all components.
10. Complete documentation including:
    - API documentation
    - User guide
    - Development guide
    - Architecture overview

**Technical Requirements**:

1. Use the shared utilities from tekton-core to ensure consistency with other components.
2. Follow the Single Port Architecture pattern.
3. Implement proper error handling using standardized error types.
4. Use async/await for all I/O operations.
5. Implement comprehensive logging.
6. Add type hints to all functions.
7. Include docstrings for all classes and functions.
8. Follow the Tekton engineering guidelines for code style and conventions.
9. Register with Hermes for component discovery.
10. Integrate with the Hephaestus UI framework for the UI component.

**Implementation Notes**:

1. Prioritize the implementation of the core workflow engine and API first.
2. The UI component should be implemented after the backend is functional.
3. Use test-driven development where appropriate.
4. Consider future extensibility in your design.
5. Identify patterns that could become shared utilities for other components.
6. Ensure graceful degradation when dependent components are unavailable.
7. Focus on creating a modular, maintainable implementation.
8. Use the newly implemented shared utilities from tekton-core.

After completing the implementation, please:

1. Update the Tekton roadmap to reflect the completion of Harmonia (Phase 19).
2. Document any patterns you identified that could become shared utilities.
3. Create a brief summary of the implementation and any challenges faced.

Your implementation should be production-ready, well-tested, and fully documented.