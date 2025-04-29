# Harmonia API Reference

This document provides a comprehensive reference for the Harmonia workflow orchestration engine API.

## Table of Contents

1. [API Endpoints](#api-endpoints)
   - [Workflow Management](#workflow-management)
   - [Execution Management](#execution-management)
   - [Template Management](#template-management)
   - [State Management](#state-management)
   - [WebSocket API](#websocket-api)
   - [Server-Sent Events](#server-sent-events)
2. [Data Models](#data-models)
   - [Workflow Definition](#workflow-definition)
   - [Workflow Execution](#workflow-execution)
   - [Tasks](#tasks)
   - [Events](#events)
   - [Templates](#templates)
   - [Checkpoints](#checkpoints)
3. [Client Library](#client-library)
   - [Python Client](#python-client)
   - [JavaScript Client](#javascript-client)
4. [Error Handling](#error-handling)
5. [Authentication](#authentication)

## API Endpoints

All API endpoints are accessible through the base URL: `http://localhost:8002/`

### Workflow Management

#### Create Workflow

```
POST /api/workflows
```

Create a new workflow definition.

**Request Body:**

```json
{
  "name": "My Workflow",
  "description": "Example workflow",
  "tasks": {
    "task1": {
      "component": "ergon",
      "action": "execute_command",
      "input": {
        "command": "echo Hello World"
      }
    },
    "task2": {
      "component": "prometheus",
      "action": "analyze_results",
      "input": {
        "data": "${tasks.task1.output.result}"
      },
      "depends_on": ["task1"]
    }
  },
  "input": {
    "type": "object",
    "properties": {
      "param1": {"type": "string"}
    }
  },
  "output": {
    "type": "object",
    "properties": {
      "result": {"type": "string"}
    }
  }
}
```

**Response:**

```json
{
  "workflow_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "My Workflow",
  "created_at": "2025-01-01T12:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Workflow successfully created
- `400 Bad Request`: Invalid workflow definition
- `409 Conflict`: Workflow with the same name already exists

#### Get Workflow

```
GET /api/workflows/{workflow_id}
```

Retrieve a workflow definition by ID.

**Path Parameters:**
- `workflow_id`: UUID of the workflow

**Response:**

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "My Workflow",
  "description": "Example workflow",
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z",
  "tasks": {
    "task1": {
      "component": "ergon",
      "action": "execute_command",
      "input": {
        "command": "echo Hello World"
      }
    },
    "task2": {
      "component": "prometheus",
      "action": "analyze_results",
      "input": {
        "data": "${tasks.task1.output.result}"
      },
      "depends_on": ["task1"]
    }
  },
  "input": {
    "type": "object",
    "properties": {
      "param1": {"type": "string"}
    }
  },
  "output": {
    "type": "object",
    "properties": {
      "result": {"type": "string"}
    }
  }
}
```

**Status Codes:**
- `200 OK`: Workflow found
- `404 Not Found`: Workflow not found

#### Update Workflow

```
PUT /api/workflows/{workflow_id}
```

Update an existing workflow definition.

**Path Parameters:**
- `workflow_id`: UUID of the workflow

**Request Body:**
Same as the Create Workflow request body.

**Response:**

```json
{
  "workflow_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "My Workflow (Updated)",
  "updated_at": "2025-01-02T12:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Workflow successfully updated
- `400 Bad Request`: Invalid workflow definition
- `404 Not Found`: Workflow not found

#### Delete Workflow

```
DELETE /api/workflows/{workflow_id}
```

Delete a workflow definition.

**Path Parameters:**
- `workflow_id`: UUID of the workflow

**Response:**

```json
{
  "success": true,
  "message": "Workflow deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Workflow successfully deleted
- `404 Not Found`: Workflow not found
- `409 Conflict`: Cannot delete workflow with active executions

#### List Workflows

```
GET /api/workflows
```

List all workflows.

**Query Parameters:**
- `limit` (optional): Maximum number of workflows to return (default: 100)
- `offset` (optional): Number of workflows to skip (default: 0)
- `filter` (optional): Filter expression (e.g., `name:contains:test`)

**Response:**

```json
{
  "workflows": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "name": "My Workflow",
      "description": "Example workflow",
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z"
    },
    {
      "id": "4fa85f64-5717-4562-b3fc-2c963f66afa7",
      "name": "Another Workflow",
      "description": "Another example workflow",
      "created_at": "2025-01-02T12:00:00Z",
      "updated_at": "2025-01-02T12:00:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

**Status Codes:**
- `200 OK`: Workflows retrieved successfully

### Execution Management

#### Execute Workflow

```
POST /api/executions
```

Execute a workflow.

**Request Body:**

```json
{
  "workflow_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "input": {
    "param1": "value1"
  },
  "metadata": {
    "source": "api",
    "priority": "high"
  }
}
```

**Response:**

```json
{
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "workflow_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "status": "pending",
  "created_at": "2025-01-03T12:00:00Z"
}
```

**Status Codes:**
- `202 Accepted`: Execution started
- `400 Bad Request`: Invalid input
- `404 Not Found`: Workflow not found

#### Get Execution Status

```
GET /api/executions/{execution_id}
```

Get the status of a workflow execution.

**Path Parameters:**
- `execution_id`: UUID of the workflow execution

**Response:**

```json
{
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "workflow_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "workflow_name": "My Workflow",
  "status": "running",
  "start_time": "2025-01-03T12:00:05Z",
  "end_time": null,
  "task_statuses": {
    "task1": {
      "status": "completed",
      "start_time": "2025-01-03T12:00:06Z",
      "end_time": "2025-01-03T12:00:07Z",
      "output": {
        "result": "Hello World"
      }
    },
    "task2": {
      "status": "running",
      "start_time": "2025-01-03T12:00:08Z",
      "end_time": null
    }
  },
  "input": {
    "param1": "value1"
  },
  "output": null,
  "error": null
}
```

**Status Codes:**
- `200 OK`: Execution found
- `404 Not Found`: Execution not found

#### Cancel Execution

```
POST /api/executions/{execution_id}/cancel
```

Cancel a running workflow execution.

**Path Parameters:**
- `execution_id`: UUID of the workflow execution

**Response:**

```json
{
  "success": true,
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "status": "canceled"
}
```

**Status Codes:**
- `200 OK`: Execution canceled successfully
- `404 Not Found`: Execution not found
- `409 Conflict`: Cannot cancel execution (already completed/failed)

#### Pause Execution

```
POST /api/executions/{execution_id}/pause
```

Pause a running workflow execution.

**Path Parameters:**
- `execution_id`: UUID of the workflow execution

**Response:**

```json
{
  "success": true,
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "status": "paused"
}
```

**Status Codes:**
- `200 OK`: Execution paused successfully
- `404 Not Found`: Execution not found
- `409 Conflict`: Cannot pause execution (not running)

#### Resume Execution

```
POST /api/executions/{execution_id}/resume
```

Resume a paused workflow execution.

**Path Parameters:**
- `execution_id`: UUID of the workflow execution

**Response:**

```json
{
  "success": true,
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "status": "running"
}
```

**Status Codes:**
- `200 OK`: Execution resumed successfully
- `404 Not Found`: Execution not found
- `409 Conflict`: Cannot resume execution (not paused)

#### List Executions

```
GET /api/executions
```

List workflow executions.

**Query Parameters:**
- `workflow_id` (optional): Filter by workflow ID
- `status` (optional): Filter by status
- `limit` (optional): Maximum number of executions to return (default: 100)
- `offset` (optional): Number of executions to skip (default: 0)

**Response:**

```json
{
  "executions": [
    {
      "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
      "workflow_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "workflow_name": "My Workflow",
      "status": "running",
      "start_time": "2025-01-03T12:00:05Z",
      "end_time": null
    },
    {
      "execution_id": "6fa85f64-5717-4562-b3fc-2c963f66afa9",
      "workflow_id": "4fa85f64-5717-4562-b3fc-2c963f66afa7",
      "workflow_name": "Another Workflow",
      "status": "completed",
      "start_time": "2025-01-02T12:00:05Z",
      "end_time": "2025-01-02T12:00:10Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

**Status Codes:**
- `200 OK`: Executions retrieved successfully

### Template Management

#### Create Template

```
POST /api/templates
```

Create a workflow template.

**Request Body:**

```json
{
  "name": "Data Processing Template",
  "description": "Template for data processing workflows",
  "workflow_definition_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "parameters": {
    "data_source": {
      "type": "string",
      "required": true,
      "description": "Source of the data to process"
    },
    "format": {
      "type": "string",
      "required": false,
      "default": "json",
      "description": "Format of the data"
    },
    "processing_options": {
      "type": "object",
      "required": false,
      "default": {"normalize": true},
      "description": "Processing options"
    }
  }
}
```

**Response:**

```json
{
  "template_id": "7fa85f64-5717-4562-b3fc-2c963f66afaa",
  "name": "Data Processing Template",
  "created_at": "2025-01-04T12:00:00Z"
}
```

**Status Codes:**
- `201 Created`: Template created successfully
- `400 Bad Request`: Invalid template definition
- `404 Not Found`: Workflow definition not found
- `409 Conflict`: Template with the same name already exists

#### Get Template

```
GET /api/templates/{template_id}
```

Get a workflow template.

**Path Parameters:**
- `template_id`: UUID of the template

**Response:**

```json
{
  "id": "7fa85f64-5717-4562-b3fc-2c963f66afaa",
  "name": "Data Processing Template",
  "description": "Template for data processing workflows",
  "workflow_definition_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2025-01-04T12:00:00Z",
  "updated_at": "2025-01-04T12:00:00Z",
  "parameters": {
    "data_source": {
      "type": "string",
      "required": true,
      "description": "Source of the data to process"
    },
    "format": {
      "type": "string",
      "required": false,
      "default": "json",
      "description": "Format of the data"
    },
    "processing_options": {
      "type": "object",
      "required": false,
      "default": {"normalize": true},
      "description": "Processing options"
    }
  }
}
```

**Status Codes:**
- `200 OK`: Template found
- `404 Not Found`: Template not found

#### Instantiate Template

```
POST /api/templates/{template_id}/instantiate
```

Create a workflow from a template.

**Path Parameters:**
- `template_id`: UUID of the template

**Request Body:**

```json
{
  "parameter_values": {
    "data_source": "s3://mybucket/data.csv",
    "format": "csv",
    "processing_options": {
      "normalize": true,
      "deduplicate": true
    }
  },
  "name": "My Data Processing Workflow"
}
```

**Response:**

```json
{
  "workflow_id": "8fa85f64-5717-4562-b3fc-2c963f66afab",
  "template_id": "7fa85f64-5717-4562-b3fc-2c963f66afaa",
  "name": "My Data Processing Workflow",
  "created_at": "2025-01-04T12:30:00Z"
}
```

**Status Codes:**
- `201 Created`: Workflow created successfully from template
- `400 Bad Request`: Invalid parameter values
- `404 Not Found`: Template not found

#### List Templates

```
GET /api/templates
```

List workflow templates.

**Query Parameters:**
- `limit` (optional): Maximum number of templates to return (default: 100)
- `offset` (optional): Number of templates to skip (default: 0)

**Response:**

```json
{
  "templates": [
    {
      "id": "7fa85f64-5717-4562-b3fc-2c963f66afaa",
      "name": "Data Processing Template",
      "description": "Template for data processing workflows",
      "created_at": "2025-01-04T12:00:00Z",
      "updated_at": "2025-01-04T12:00:00Z"
    },
    {
      "id": "8fa85f64-5717-4562-b3fc-2c963f66afac",
      "name": "Notification Template",
      "description": "Template for notification workflows",
      "created_at": "2025-01-04T13:00:00Z",
      "updated_at": "2025-01-04T13:00:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

**Status Codes:**
- `200 OK`: Templates retrieved successfully

### State Management

#### Create Checkpoint

```
POST /api/checkpoints
```

Create a checkpoint of a workflow execution.

**Request Body:**

```json
{
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8"
}
```

**Response:**

```json
{
  "checkpoint_id": "9fa85f64-5717-4562-b3fc-2c963f66afad",
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "created_at": "2025-01-03T12:15:00Z",
  "workflow_status": "running",
  "completed_tasks": ["task1"]
}
```

**Status Codes:**
- `201 Created`: Checkpoint created successfully
- `404 Not Found`: Execution not found
- `400 Bad Request`: Cannot create checkpoint (execution not running)

#### Get Checkpoint

```
GET /api/checkpoints/{checkpoint_id}
```

Get a checkpoint.

**Path Parameters:**
- `checkpoint_id`: UUID of the checkpoint

**Response:**

```json
{
  "id": "9fa85f64-5717-4562-b3fc-2c963f66afad",
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "created_at": "2025-01-03T12:15:00Z",
  "workflow_status": "running",
  "task_statuses": {
    "task1": "completed",
    "task2": "running"
  },
  "completed_tasks": ["task1"],
  "state_data": {
    "task_results": {
      "task1": {
        "result": "Hello World"
      }
    }
  }
}
```

**Status Codes:**
- `200 OK`: Checkpoint found
- `404 Not Found`: Checkpoint not found

#### Restore From Checkpoint

```
POST /api/checkpoints/{checkpoint_id}/restore
```

Restore a workflow execution from a checkpoint.

**Path Parameters:**
- `checkpoint_id`: UUID of the checkpoint

**Response:**

```json
{
  "execution_id": "afa85f64-5717-4562-b3fc-2c963f66afae",
  "original_execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "checkpoint_id": "9fa85f64-5717-4562-b3fc-2c963f66afad",
  "status": "running"
}
```

**Status Codes:**
- `201 Created`: New execution created from checkpoint
- `404 Not Found`: Checkpoint not found
- `400 Bad Request`: Cannot restore from checkpoint

#### List Checkpoints

```
GET /api/checkpoints
```

List checkpoints.

**Query Parameters:**
- `execution_id` (optional): Filter by execution ID
- `limit` (optional): Maximum number of checkpoints to return (default: 100)
- `offset` (optional): Number of checkpoints to skip (default: 0)

**Response:**

```json
{
  "checkpoints": [
    {
      "id": "9fa85f64-5717-4562-b3fc-2c963f66afad",
      "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
      "created_at": "2025-01-03T12:15:00Z",
      "workflow_status": "running"
    },
    {
      "id": "bfa85f64-5717-4562-b3fc-2c963f66afaf",
      "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
      "created_at": "2025-01-03T12:30:00Z",
      "workflow_status": "running"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

**Status Codes:**
- `200 OK`: Checkpoints retrieved successfully

#### Save State

```
PUT /api/state/{execution_id}
```

Save custom state data for a workflow execution.

**Path Parameters:**
- `execution_id`: UUID of the workflow execution

**Request Body:**

```json
{
  "state": {
    "custom_data": {
      "key1": "value1",
      "key2": 42
    },
    "progress": 0.75,
    "processed_items": 150
  }
}
```

**Response:**

```json
{
  "success": true,
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "timestamp": "2025-01-03T12:45:00Z"
}
```

**Status Codes:**
- `200 OK`: State saved successfully
- `404 Not Found`: Execution not found

#### Load State

```
GET /api/state/{execution_id}
```

Load custom state data for a workflow execution.

**Path Parameters:**
- `execution_id`: UUID of the workflow execution

**Response:**

```json
{
  "state": {
    "custom_data": {
      "key1": "value1",
      "key2": 42
    },
    "progress": 0.75,
    "processed_items": 150
  },
  "last_updated": "2025-01-03T12:45:00Z"
}
```

**Status Codes:**
- `200 OK`: State retrieved successfully
- `404 Not Found`: Execution or state not found

### WebSocket API

#### Execution Events

```
ws://localhost:8002/ws/executions/{execution_id}
```

Subscribe to real-time events for a workflow execution.

**Path Parameters:**
- `execution_id`: UUID of the workflow execution

**Events Received:**

```json
{
  "event_type": "task_started",
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "task_id": "task2",
  "timestamp": "2025-01-03T12:00:08Z",
  "details": {
    "task_name": "Analyze Results"
  }
}
```

**Messages to Send:**

```json
{
  "type": "ping"
}
```

**Responses:**

```json
{
  "type": "pong",
  "timestamp": "2025-01-03T12:10:00Z"
}
```

### Server-Sent Events

#### Execution Events

```
GET /events/executions/{execution_id}
```

Stream real-time events for a workflow execution.

**Path Parameters:**
- `execution_id`: UUID of the workflow execution

**Events:**

```
event: task_started
data: {"execution_id":"5fa85f64-5717-4562-b3fc-2c963f66afa8","task_id":"task2","timestamp":"2025-01-03T12:00:08Z"}

event: task_completed
data: {"execution_id":"5fa85f64-5717-4562-b3fc-2c963f66afa8","task_id":"task2","timestamp":"2025-01-03T12:00:10Z"}

event: workflow_completed
data: {"execution_id":"5fa85f64-5717-4562-b3fc-2c963f66afa8","timestamp":"2025-01-03T12:00:10Z"}
```

## Data Models

### Workflow Definition

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "My Workflow",
  "description": "Example workflow",
  "version": "1.0",
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z",
  "tasks": {
    "task1": {
      "id": "task1",
      "name": "Execute Command",
      "component": "ergon",
      "action": "execute_command",
      "input": {
        "command": "echo Hello World"
      },
      "output": {
        "result": "string"
      },
      "depends_on": [],
      "timeout": 300,
      "retry": 3,
      "metadata": {
        "description": "Execute a shell command",
        "category": "system"
      }
    },
    "task2": {
      "id": "task2",
      "name": "Analyze Results",
      "component": "prometheus",
      "action": "analyze_results",
      "input": {
        "data": "${tasks.task1.output.result}"
      },
      "output": {
        "analysis": "object"
      },
      "depends_on": ["task1"],
      "timeout": 600,
      "retry": 2,
      "metadata": {
        "description": "Analyze command results",
        "category": "analysis",
        "condition": "${tasks.task1.output.result != ''}"
      }
    }
  },
  "input": {
    "type": "object",
    "properties": {
      "param1": {"type": "string"}
    }
  },
  "output": {
    "type": "object",
    "properties": {
      "result": {"type": "string"}
    }
  },
  "metadata": {
    "author": "user",
    "category": "example",
    "tags": ["demo", "example"]
  }
}
```

### Workflow Execution

```json
{
  "id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "workflow_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "workflow_name": "My Workflow",
  "status": "running",
  "start_time": "2025-01-03T12:00:05Z",
  "end_time": null,
  "input": {
    "param1": "value1"
  },
  "output": null,
  "error": null,
  "task_executions": {
    "task1": {
      "task_id": "task1",
      "status": "completed",
      "start_time": "2025-01-03T12:00:06Z",
      "end_time": "2025-01-03T12:00:07Z",
      "input": {
        "command": "echo Hello World"
      },
      "output": {
        "result": "Hello World"
      },
      "error": null,
      "retries": 0
    },
    "task2": {
      "task_id": "task2",
      "status": "running",
      "start_time": "2025-01-03T12:00:08Z",
      "end_time": null,
      "input": {
        "data": "Hello World"
      },
      "output": null,
      "error": null,
      "retries": 0
    }
  },
  "metadata": {
    "source": "api",
    "priority": "high"
  }
}
```

### Tasks

```json
{
  "id": "task1",
  "name": "Execute Command",
  "component": "ergon",
  "action": "execute_command",
  "input": {
    "command": "echo Hello World"
  },
  "output": {
    "result": "string"
  },
  "depends_on": [],
  "timeout": 300,
  "retry": 3,
  "metadata": {
    "description": "Execute a shell command",
    "category": "system",
    "condition": null
  }
}
```

### Events

```json
{
  "event_type": "task_completed",
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "task_id": "task1",
  "timestamp": "2025-01-03T12:00:07Z",
  "details": {
    "duration": 1.0,
    "output_size": 11
  },
  "message": "Task 'Execute Command' completed successfully"
}
```

### Templates

```json
{
  "id": "7fa85f64-5717-4562-b3fc-2c963f66afaa",
  "name": "Data Processing Template",
  "description": "Template for data processing workflows",
  "workflow_definition_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "created_at": "2025-01-04T12:00:00Z",
  "updated_at": "2025-01-04T12:00:00Z",
  "parameters": {
    "data_source": {
      "type": "string",
      "required": true,
      "description": "Source of the data to process"
    },
    "format": {
      "type": "string",
      "required": false,
      "default": "json",
      "description": "Format of the data"
    },
    "processing_options": {
      "type": "object",
      "required": false,
      "default": {"normalize": true},
      "description": "Processing options"
    }
  },
  "metadata": {
    "author": "user",
    "category": "data_processing",
    "version": "1.0"
  }
}
```

### Checkpoints

```json
{
  "id": "9fa85f64-5717-4562-b3fc-2c963f66afad",
  "execution_id": "5fa85f64-5717-4562-b3fc-2c963f66afa8",
  "created_at": "2025-01-03T12:15:00Z",
  "workflow_status": "running",
  "task_statuses": {
    "task1": "completed",
    "task2": "running"
  },
  "completed_tasks": ["task1"],
  "state_data": {
    "input": {
      "param1": "value1"
    },
    "output": null,
    "task_results": {
      "task1": {
        "result": "Hello World"
      }
    }
  }
}
```

## Client Library

### Python Client

#### Installation

```bash
pip install harmonia-client
```

#### Basic Usage

```python
import asyncio
from harmonia.client import get_harmonia_client

async def main():
    # Get Harmonia client
    client = await get_harmonia_client()
    
    try:
        # Create a workflow
        workflow = await client.create_workflow(
            name="Example Workflow",
            description="An example workflow",
            tasks=[
                {
                    "id": "task1",
                    "component": "ergon",
                    "action": "execute_command",
                    "input": {"command": "echo Hello World"}
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
    
    finally:
        # Close the client
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

#### API Reference

```python
class HarmoniaClient:
    async def create_workflow(name, tasks, description=None, input_schema=None, output_schema=None):
        """Create a new workflow definition."""
        
    async def execute_workflow(workflow_id, input_data=None):
        """Execute a workflow."""
        
    async def get_workflow_status(execution_id):
        """Get the status of a workflow execution."""
        
    async def cancel_workflow(execution_id):
        """Cancel a workflow execution."""
        
    async def create_template(name, workflow_definition_id, parameters):
        """Create a workflow template."""
        
    async def instantiate_template(template_id, parameter_values):
        """Instantiate a workflow from a template."""
        
    async def restore_from_checkpoint(checkpoint_id):
        """Restore a workflow from a checkpoint."""
```

### JavaScript Client

```javascript
// Initialize client
const harmoniaClient = new HarmoniaClient({
  baseUrl: 'http://localhost:8002',
  headers: {
    'Authorization': 'Bearer your-token'
  }
});

// Create workflow
harmoniaClient.createWorkflow({
  name: 'JavaScript Example',
  description: 'Example workflow from JavaScript',
  tasks: [
    {
      id: 'task1',
      component: 'ergon',
      action: 'execute_command',
      input: { command: 'echo Hello World' }
    }
  ]
})
.then(workflow => {
  console.log(`Created workflow: ${workflow.workflow_id}`);
  
  // Execute workflow
  return harmoniaClient.executeWorkflow({
    workflow_id: workflow.workflow_id
  });
})
.then(execution => {
  console.log(`Started execution: ${execution.execution_id}`);
  
  // Connect to WebSocket for real-time updates
  const ws = harmoniaClient.connectToExecution(execution.execution_id);
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(`Event: ${data.event_type}`, data);
    
    if (data.event_type === 'workflow_completed') {
      ws.close();
      
      // Get final status
      harmoniaClient.getWorkflowStatus(execution.execution_id)
        .then(status => {
          console.log('Final status:', status);
        });
    }
  };
})
.catch(error => {
  console.error('Error:', error);
});
```

## Error Handling

### Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | `ValidationError` | Invalid input data |
| 401 | `AuthenticationError` | Authentication required |
| 403 | `AuthorizationError` | Permission denied |
| 404 | `NotFoundError` | Resource not found |
| 409 | `ConflictError` | Resource conflict |
| 422 | `ProcessingError` | Processing error |
| 429 | `RateLimitError` | Rate limit exceeded |
| 500 | `InternalError` | Internal server error |
| 503 | `UnavailableError` | Service unavailable |

### Error Response Format

```json
{
  "error": {
    "type": "ValidationError",
    "message": "Invalid input data",
    "details": {
      "field": "tasks",
      "reason": "Missing required field: component"
    },
    "code": "INVALID_INPUT",
    "request_id": "req-12345-abcde"
  }
}
```

## Authentication

Harmonia supports token-based authentication through Hermes.

### Authentication Header

```
Authorization: Bearer <token>
```

### Example Request with Authentication

```bash
curl -X POST http://localhost:8002/api/workflows \
  -H "Authorization: Bearer your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Workflow",
    "description": "Example workflow",
    "tasks": [...]
  }'
```