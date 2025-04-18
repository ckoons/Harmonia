# Harmonia

## Overview

Harmonia is the workflow orchestration engine for the Tekton ecosystem. It coordinates complex workflows across components, manages state persistence, and handles task sequencing.

## Key Features

- Workflow definition and execution
- State management and persistence
- Error handling and recovery
- Event-driven execution
- Dynamic task routing
- Complex workflow patterns (branching, merging, parallelization)

## Quick Start

```bash
# Register with Hermes
python -m Harmonia/examples/register_with_hermes.py

# Start with Tekton
./scripts/tekton_launch --components harmonia

# Use client
python -m Harmonia/examples/client_usage.py
```

## Documentation

For detailed documentation, see the following resources in the MetaData directory:

- [Component Summaries](../MetaData/ComponentSummaries.md) - Overview of all Tekton components
- [Tekton Architecture](../MetaData/TektonArchitecture.md) - Overall system architecture
- [Component Integration](../MetaData/ComponentIntegration.md) - How components interact
- [CLI Operations](../MetaData/CLI_Operations.md) - Command-line operations