"""
Hermes Bridge for Harmonia MCP Tools

This module bridges Harmonia's FastMCP tools with Hermes MCP aggregator,
allowing Harmonia's tools to be discoverable and executable through Hermes.
"""

import logging
from typing import Dict, Any, List, Optional
from shared.mcp import MCPService, MCPConfig
from shared.mcp.client import HermesMCPClient
from shared.mcp.tools import HealthCheckTool, ComponentInfoTool

logger = logging.getLogger(__name__)

class HarmoniaMCPBridge(MCPService):
    """
    Bridge between Harmonia's FastMCP tools and Hermes MCP aggregator.
    
    This class allows Harmonia to register its tools with Hermes while
    maintaining the existing FastMCP implementation.
    """
    
    def __init__(self, workflow_engine, component_name: str = "harmonia"):
        """Initialize the Harmonia MCP Bridge."""
        super().__init__(component_name)
        self.workflow_engine = workflow_engine
        self.hermes_client = None
        self._fastmcp_tools = None
        
    async def initialize(self):
        """Initialize the MCP service and register with Hermes."""
        await super().initialize()
        
        # Create Hermes client
        config = MCPConfig.from_env(self.component_name)
        self.hermes_client = HermesMCPClient(
            hermes_url=config.hermes_url,
            component_name=self.component_name,
            auth_token=getattr(config, "auth_token", None)
        )
        
        # Load FastMCP tools
        try:
            from harmonia.core.mcp import get_all_tools
            self._fastmcp_tools = get_all_tools(self.workflow_engine)
            logger.info(f"Loaded {len(self._fastmcp_tools)} FastMCP tools")
        except Exception as e:
            logger.error(f"Failed to load FastMCP tools: {e}")
            self._fastmcp_tools = []
            
        # Register tools with both local registry and Hermes
        await self.register_default_tools()
        await self.register_fastmcp_tools()
        
    async def register_default_tools(self):
        """Register standard tools like health check and component info."""
        # Health check tool
        health_tool = HealthCheckTool(self.component_name)
        health_tool.get_health_func = self._get_health_status
        await self.register_tool_with_hermes(health_tool)
        
        # Component info tool  
        info_tool = ComponentInfoTool(
            component_name=self.component_name,
            component_version="0.1.0",
            component_description="Workflow orchestration engine for coordinating tasks across Tekton components"
        )
        await self.register_tool_with_hermes(info_tool)
        
    async def register_fastmcp_tools(self):
        """Register FastMCP tools with Hermes."""
        if not self._fastmcp_tools:
            logger.warning("No FastMCP tools to register")
            return
            
        for tool in self._fastmcp_tools:
            try:
                # Create a wrapper that converts FastMCP tool to shared MCP format
                await self.register_fastmcp_tool(tool)
            except Exception as e:
                logger.error(f"Failed to register tool {tool.get('name', 'unknown')}: {e}")
                
    async def register_fastmcp_tool(self, fastmcp_tool: Dict[str, Any]):
        """Register a single FastMCP tool with Hermes."""
        tool_name = f"{self.component_name}_{fastmcp_tool['name']}"
        
        # Create handler that delegates to FastMCP
        async def handler(parameters: Dict[str, Any]) -> Dict[str, Any]:
            # Import here to avoid circular imports
            from tekton.mcp.fastmcp.utils.requests import process_mcp_request
            from tekton.mcp.fastmcp.schema import MCPRequest
            
            # Create an MCP request for the FastMCP handler
            request = MCPRequest(
                client_id="hermes",
                tool=fastmcp_tool['name'],
                parameters=parameters
            )
            
            # Process through FastMCP
            response = await process_mcp_request(
                component_manager=self.workflow_engine,
                request=request,
                component_module_path="harmonia.core.mcp.tools"
            )
            
            # Extract result from response
            if response.status == "success":
                return response.result
            else:
                raise Exception(response.error or "Unknown error")
                
        # Register with Hermes
        if self.hermes_client:
            try:
                await self.hermes_client.register_tool(
                    name=tool_name,
                    description=fastmcp_tool.get('description', ''),
                    input_schema=fastmcp_tool.get('input_schema', {}),
                    output_schema=fastmcp_tool.get('output_schema', {}),
                    handler=handler,
                    metadata={
                        'category': fastmcp_tool.get('category', 'general'),
                        'tags': fastmcp_tool.get('tags', []),
                        'fastmcp': True
                    }
                )
                logger.info(f"Registered tool {tool_name} with Hermes")
            except Exception as e:
                logger.error(f"Failed to register {tool_name} with Hermes: {e}")
                
    async def register_tool_with_hermes(self, tool):
        """Register a standard MCP tool with Hermes."""
        if not self.hermes_client:
            logger.warning("Hermes client not initialized")
            return
            
        tool_name = f"{self.component_name}_{tool.name}"
        
        try:
            await self.hermes_client.register_tool(
                name=tool_name,
                description=tool.description,
                input_schema=tool.get_input_schema(),
                output_schema=getattr(tool, "output_schema", {}),
                handler=tool,  # The tool itself is callable
                metadata=tool.get_metadata()
            )
            logger.info(f"Registered tool {tool_name} with Hermes")
        except Exception as e:
            logger.error(f"Failed to register {tool_name} with Hermes: {e}")
            
    async def _get_health_status(self) -> Dict[str, Any]:
        """Get health status from workflow engine."""
        try:
            if self.workflow_engine:
                # Get engine status
                active_workflows = await self.workflow_engine.get_active_workflow_count()
                total_workflows = await self.workflow_engine.get_total_workflow_count()
                
                return {
                    "status": "healthy",
                    "details": {
                        "active_workflows": active_workflows,
                        "total_workflows": total_workflows,
                        "engine_initialized": True
                    }
                }
            else:
                return {
                    "status": "starting",
                    "details": {"message": "Workflow engine initializing"}
                }
        except Exception as e:
            return {
                "status": "unhealthy", 
                "details": {"error": str(e)}
            }
            
    async def shutdown(self):
        """Shutdown the MCP service and unregister from Hermes."""
        if self.hermes_client:
            # Get all registered tools
            tools_to_unregister = []
            
            # Add default tools
            tools_to_unregister.extend([
                f"{self.component_name}_health_check",
                f"{self.component_name}_component_info"
            ])
            
            # Add FastMCP tools
            if self._fastmcp_tools:
                for tool in self._fastmcp_tools:
                    tools_to_unregister.append(f"{self.component_name}_{tool['name']}")
                    
            # Unregister all tools
            for tool_id in tools_to_unregister:
                try:
                    await self.hermes_client.unregister_tool(tool_id)
                    logger.info(f"Unregistered tool {tool_id} from Hermes")
                except Exception as e:
                    logger.error(f"Failed to unregister {tool_id}: {e}")
                    
        await super().shutdown()