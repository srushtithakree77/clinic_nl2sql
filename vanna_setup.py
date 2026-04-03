
import os
from dotenv import load_dotenv
from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.google import GeminiLlmService

load_dotenv()

def create_agent():
    llm_service = GeminiLlmService(
        api_key=os.getenv('GOOGLE_API_KEY'),
        model='gemini-2.0-flash'
    )
    print('LLM Service created!')
    db_runner = SqliteRunner(database_path='clinic.db')
    print('Database connected!')
    registry = ToolRegistry()
    registry.register_local_tool(RunSqlTool(sql_runner=db_runner), access_groups=[])
    registry.register_local_tool(VisualizeDataTool(), access_groups=[])
    registry.register_local_tool(SaveQuestionToolArgsTool(), access_groups=[])
    registry.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=[])
    print('Tools registered!')
    memory = DemoAgentMemory()
    print('Memory created!')
    class SimpleUserResolver(UserResolver):
        async def resolve_user(self, request_context: RequestContext) -> User:
            return User(id='default_user', name='Default User')
    user_resolver = SimpleUserResolver()
    print('User resolver created!')
    agent = Agent(
        llm_service=llm_service,
        tool_registry=registry,
        user_resolver=user_resolver,
        agent_memory=memory
    )
    print('Agent created successfully!')
    return agent

if __name__ == '__main__':
    agent = create_agent()
    print('Vanna Agent is ready!')
