import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from .models import AgentMessage, MessageResponse
from autopilot_flywheel.observability.tracer import tracer

class AgentMailClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8765/mcp/"):
        self.base_url = base_url

    async def _send_async(self, message: AgentMessage) -> MessageResponse:
        async with streamablehttp_client(self.base_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool("send_message", arguments={
                    "project_key": message.project,
                    "sender_name": message.sender,
                    "to": [message.recipient],
                    "subject": message.subject,
                    "body_md": message.body
                })
                if result.isError:
                    raise RuntimeError(f"MCP Tool Error: {result.content}")
                return MessageResponse(status="success")

    def send_message(self, message: AgentMessage) -> MessageResponse:
        with tracer.start_as_current_span("agent_mail.send_message") as span:
            span.set_attribute("project", message.project)
            span.set_attribute("recipient", message.recipient)
            try:
                return asyncio.run(self._send_async(message))
            except Exception as e:
                span.record_exception(e)
                raise

    async def _fetch_async(self, project: str, agent: str) -> str:
        async with streamablehttp_client(self.base_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool("fetch_inbox", arguments={
                    "project_key": project,
                    "agent_name": agent
                })
                if result.isError:
                    raise RuntimeError(f"MCP Tool Error: {result.content}")
                return result.content[0].text if result.content else "[]"

    def fetch_inbox(self, project: str, agent: str) -> str:
        with tracer.start_as_current_span("agent_mail.fetch_inbox") as span:
            span.set_attribute("project", project)
            span.set_attribute("agent", agent)
            return asyncio.run(self._fetch_async(project, agent))
