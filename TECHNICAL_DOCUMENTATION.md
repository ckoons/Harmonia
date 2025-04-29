# Harmonia Technical Documentation

## Overview

Harmonia is the workflow orchestration engine for the Tekton ecosystem, coordinating complex workflows across components, managing state persistence, and handling task sequencing. Named after the Greek goddess of harmony and concord, Harmonia brings together various Tekton components to work in unison.

## Architecture

Harmonia follows a modular architecture designed for flexibility, reliability, and scalability:

### Core Components

1. **Workflow Engine (`core/engine.py`)**
   - Central execution engine that coordinates task scheduling and execution
   - Manages dependency resolution between tasks
   - Handles error recovery and retry logic
   - Implements checkpoint and recovery mechanisms
   - Provides event-based notifications for workflow status changes

2. **State Manager (`core/state.py`)**
   - Manages persistence of workflow state
   - Provides storage for execution checkpoints and history
   - Implements save/load mechanisms for workflow continuation
   - Supports both in-memory and file-based storage with DB extensibility

3. **Workflow Models (`core/workflow.py`, `models/workflow.py`, `models/execution.py`)**
   - Define data structures for workflows, tasks, and executions
   - Implement serialization/deserialization for persistence
   - Support dependency graph generation and validation
   - Provide status tracking for tasks and workflows

4. **Component Registry (`core/component.py`)**
   - Manages connections to other Tekton components
   - Routes task execution requests to appropriate components
   - Provides adapter pattern for component integration

5. **Expression Evaluator (`core/expressions.py`)**
   - Evaluates dynamic expressions within workflow definitions
   - Handles parameter substitution from context values
   - Supports condition evaluation for conditional task execution

6. **Template System (`core/template.py`)**
   - Provides template-based workflow definition
   - Supports parameter injection for reusable workflows
   - Manages template versioning and instantiation

### API Layer

1. **HTTP REST API (`api/app.py`)**
   - Exposes workflow management endpoints
   - Implements Single Port Architecture following Tekton standards
   - Provides JSON API for workflow creation, execution, and monitoring

2. **WebSocket API (`api/app.py`)**
   - Enables real-time monitoring of workflow execution
   - Publishes event streams for task and workflow status changes
   - Supports client-side progress tracking and visualization

3. **Client Library (`client.py`)**
   - Provides a Python client for integrating with Harmonia
   - Implements Tekton's standardized component client interface
   - Supports both workflow and state management operations

### Integration Points

1. **Hermes Integration (`scripts/register_with_hermes.py`)**
   - Registers Harmonia capabilities with Hermes service registry
   - Enables component discovery and orchestration
   - Provides capability metadata for integration

2. **Component Adapters**
   - Interfaces with other Tekton components like:
     - Engram for long-term memory
     - Rhetor for LLM interactions
     - Prometheus for metrics
     - Ergon for command execution
     - Synthesis for task execution

## Data Model

### Workflow Definition

```
Workflow
├── id: UUID
├── name: string
├── description: string
├── version: string
├── metadata: object
├── input: object (schema)
├── output: object (schema)
└── tasks: Map<string, Task>
    └── Task
        ├── id: string
        ├── name: string
        ├── component: string
        ├── action: string
        ├── input: object
        ├── output: object
        ├── depends_on: string[]
        ├── timeout: number
        ├── retry: number
        └── metadata: object
```

### Workflow Execution

```
WorkflowExecution
├── id: UUID
├── workflow_id: UUID
├── status: enum (PENDING, RUNNING, COMPLETED, FAILED, PAUSED, CANCELED)
├── start_time: datetime
├── end_time: datetime
├── input: object
├── output: object
├── error: string
├── metadata: object
└── task_executions: Map<string, TaskExecution>
    └── TaskExecution
        ├── task_id: string
        ├── status: enum (PENDING, RUNNING, COMPLETED, FAILED, SKIPPED)
        ├── start_time: datetime
        ├── end_time: datetime
        ├── input: object
        ├── output: object
        ├── error: string
        └── retries: number
```

### State Management

```
Checkpoint
├── id: UUID
├── execution_id: UUID
├── created_at: datetime
├── workflow_status: enum
├── task_statuses: Map<string, enum>
├── completed_tasks: string[]
└── state_data: object

ExecutionHistory
├── execution_id: UUID
├── events: ExecutionEvent[]
├── checkpoints: Checkpoint[]
└── metrics: ExecutionMetrics
```

## API Reference

### HTTP REST API

#### Workflow Management

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/workflows` | POST | Create workflow | `name`, `description`, `tasks`, `input`, `output` |
| `/api/workflows/{id}` | GET | Get workflow | - |
| `/api/workflows/{id}` | PUT | Update workflow | `name`, `description`, `tasks`, `input`, `output` |
| `/api/workflows/{id}` | DELETE | Delete workflow | - |
| `/api/workflows` | GET | List workflows | `limit`, `offset`, `filter` |

#### Execution Management

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/executions` | POST | Execute workflow | `workflow_id`, `input` |
| `/api/executions/{id}` | GET | Get execution status | - |
| `/api/executions/{id}/cancel` | POST | Cancel execution | - |
| `/api/executions/{id}/pause` | POST | Pause execution | - |
| `/api/executions/{id}/resume` | POST | Resume execution | - |
| `/api/executions` | GET | List executions | `limit`, `offset`, `filter` |

#### Template Management

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/templates` | POST | Create template | `name`, `workflow_definition_id`, `parameters` |
| `/api/templates/{id}` | GET | Get template | - |
| `/api/templates/{id}/instantiate` | POST | Instantiate template | `parameter_values` |
| `/api/templates` | GET | List templates | `limit`, `offset`, `filter` |

#### State Management

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/state/{execution_id}` | GET | Get state | - |
| `/api/state/{execution_id}` | PUT | Save state | `state` |
| `/api/checkpoints` | POST | Create checkpoint | `execution_id` |
| `/api/checkpoints/{id}/restore` | POST | Restore from checkpoint | - |

### WebSocket API

| Endpoint | Description | Events |
|----------|-------------|--------|
| `/ws/executions/{id}` | Execution events | `workflow_started`, `task_started`, `task_completed`, `task_failed`, `workflow_completed`, `workflow_failed`, `workflow_canceled` |

### Server-Sent Events (SSE)

| Endpoint | Description | Events |
|----------|-------------|--------|
| `/events/executions/{id}` | Execution events | `workflow_started`, `task_started`, `task_completed`, `task_failed`, `workflow_completed`, `workflow_failed`, `workflow_canceled` |

## Client Usage

### Basic Workflow Creation and Execution

```python
import asyncio
from harmonia.client import get_harmonia_client

async def main():
    # Get Harmonia client
    client = await get_harmonia_client()
    
    # Create a workflow
    workflow = await client.create_workflow(
        name="example_workflow",
        description="Example workflow",
        tasks=[
            {
                "id": "task1",
                "component": "ergon",
                "action": "execute_command",
                "input": {"command": "echo Hello World"}
            },
            {
                "id": "task2",
                "component": "prometheus",
                "action": "analyze_results",
                "input": {"data": "${tasks.task1.output.result}"},
                "depends_on": ["task1"]
            }
        ]
    )
    
    # Execute the workflow
    execution = await client.execute_workflow(
        workflow_id=workflow["workflow_id"]
    )
    
    # Get workflow status
    status = await client.get_workflow_status(
        execution_id=execution["execution_id"]
    )
    
    print(f"Workflow status: {status['status']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Template-Based Workflows

```python
import asyncio
from harmonia.client import get_harmonia_client

async def main():
    client = await get_harmonia_client()
    
    # Create a template from an existing workflow
    template = await client.create_template(
        name="process_data_template",
        workflow_definition_id="workflow-uuid-here",
        parameters={
            "input_file": {
                "type": "string",
                "required": True,
                "description": "Input file path"
            },
            "output_format": {
                "type": "string",
                "required": False,
                "default": "json",
                "description": "Output format"
            }
        }
    )
    
    # Instantiate the template
    workflow = await client.instantiate_template(
        template_id=template["template_id"],
        parameter_values={
            "input_file": "/path/to/data.csv",
            "output_format": "xml"
        }
    )
    
    # Execute the instantiated workflow
    await client.execute_workflow(workflow_id=workflow["workflow_id"])

if __name__ == "__main__":
    asyncio.run(main())
```

### State Management and Checkpoints

```python
import asyncio
from harmonia.client import get_harmonia_client, get_harmonia_state_client

async def main():
    client = await get_harmonia_client()
    state_client = await get_harmonia_state_client()
    
    # Create checkpoint for a running workflow
    checkpoint = await state_client.create_checkpoint(
        execution_id="execution-uuid-here"
    )
    
    # Restore from checkpoint
    new_execution = await client.restore_from_checkpoint(
        checkpoint_id=checkpoint["checkpoint_id"]
    )
    
    print(f"Restored workflow: {new_execution['execution_id']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Component Integration

### Integrating with Harmonia

Other Tekton components can integrate with Harmonia using the following approaches:

1. **Client Integration**
   - Use the Harmonia client library (`harmonia.client`) to create and execute workflows
   - Handle workflow events through the WebSocket API
   - Ensure proper error handling and retry logic

2. **Task Execution**
   - Implement task execution handlers for component-specific actions
   - Register capabilities with Hermes to be discoverable by Harmonia
   - Return standardized result objects with success/failure status

3. **State Persistence**
   - Use the state management APIs to store component-specific state
   - Leverage checkpointing for long-running operations
   - Integrate with Engram for shared memory across components

### Integration with Hermes

Harmonia registers the following capabilities with Hermes:

- `create_workflow`: Create workflow definitions
- `execute_workflow`: Execute workflows
- `get_workflow_status`: Get execution status
- `cancel_workflow`: Cancel workflow execution
- `save_state`: Save workflow state
- `load_state`: Load workflow state
- `create_checkpoint`: Create execution checkpoint

## Implementation Details

### Workflow Execution Process

1. **Workflow Creation**
   - Client calls `create_workflow` API
   - System validates workflow definition
   - Workflow is stored in state manager

2. **Workflow Execution**
   - Client calls `execute_workflow` API
   - Engine creates execution context
   - Engine builds dependency graph
   - Root tasks (with no dependencies) are identified

3. **Task Scheduling**
   - Tasks are scheduled based on dependencies
   - Semaphore controls concurrent task execution
   - Engine continuously monitors for ready tasks

4. **Task Execution**
   - Engine resolves task input parameters
   - Component registry routes task to appropriate component
   - Retry policy handles transient failures
   - Results are stored and dependencies updated

5. **Workflow Completion**
   - All tasks are marked as completed, failed, or skipped
   - Final status is determined
   - Results are saved to state manager
   - Events are fired for completion or failure

### Error Handling and Recovery

- **Retry Policy**: Each task can specify retry parameters
- **Exponential Backoff**: Retries use exponential backoff with jitter
- **Partial Completion**: Workflows track partially completed states
- **Checkpointing**: Periodic state snapshots for long-running workflows
- **Recovery**: Failed workflows can be resumed from checkpoints

### Event System

- **Event Types**: Comprehensive events for workflow and task lifecycle
- **Multiple Interfaces**: Events available via WebSocket, SSE, and callback
- **Subscription Model**: Components can subscribe to specific event types
- **Event History**: Complete event history for auditing and debugging

## Security Considerations

- **Input Validation**: All workflow inputs are validated against schemas
- **Component Authentication**: Component registry validates component identity
- **Expression Sandboxing**: Expressions evaluated in controlled environment
- **Resource Limits**: Concurrency and timeout limits prevent resource exhaustion
- **Workflow Isolation**: Executions are isolated from each other

## Performance Optimization

- **Concurrent Execution**: Parallel execution of independent tasks
- **Resource Management**: Controlled task concurrency via semaphores
- **Efficient State Storage**: Selective state persistence for large workflows
- **Event Buffering**: Event delivery optimized for high-throughput cases
- **Memory Management**: Cleanup of completed workflow resources

## Integration with Tekton Ecosystem

Harmonia integrates with other Tekton components:

- **Hermes**: Service discovery and registration
- **Engram**: Memory persistence for workflow state
- **Rhetor**: LLM decision making for workflow branching
- **Prometheus**: Analytics and metrics for workflow performance
- **Ergon**: Command execution and automation
- **Sophia**: ML operations within workflows
- **Synthesis**: Integration with external systems

## Future Enhancements

1. **Advanced Workflow Features**
   - Dynamic workflow generation
   - Conditional branching and looping
   - Sub-workflows and composition
   - Time-based triggers and scheduling

2. **Performance Improvements**
   - Distributed execution across nodes
   - Streaming task results for large data
   - Optimized checkpoint mechanisms
   - Selective task re-execution

3. **Enhanced Integration**
   - Standard connectors for common systems
   - Workflow marketplace for sharing templates
   - Visual workflow designer in UI
   - Enhanced monitoring and observability

## Conclusion

Harmonia provides a robust workflow orchestration system for the Tekton ecosystem, enabling complex multi-component processes with reliability, flexibility, and observability. Its modular design and comprehensive feature set make it suitable for a wide range of orchestration needs, from simple sequential tasks to complex distributed workflows with state persistence and real-time monitoring.