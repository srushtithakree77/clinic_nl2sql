import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from vanna_setup import create_agent
from vanna.core.user import RequestContext, User

load_dotenv()

# Create FastAPI app
app = FastAPI(title="Clinic NL2SQL API")

# Create Vanna agent once when server starts
agent = create_agent()

# This defines what the request should look like
class QuestionRequest(BaseModel):
    question: str

# This defines what the response will look like
class QuestionResponse(BaseModel):
    message: str
    sql_query: str
    rows: list
    row_count: int
    error: str = None

# SQL Validation - only allow SELECT queries
def validate_sql(sql: str) -> bool:
    if not sql:
        return False
    sql_upper = sql.upper().strip()
    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return False
    # Block dangerous keywords
    dangerous = ["INSERT", "UPDATE", "DELETE", "DROP", 
                 "ALTER", "EXEC", "GRANT", "REVOKE", 
                 "SHUTDOWN", "XP_", "SP_"]
    for keyword in dangerous:
        if keyword in sql_upper:
            return False
    # Block system tables
    if "SQLITE_MASTER" in sql_upper:
        return False
    return True

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "database": "connected",
        "agent": "ready"
    }

# Main chat endpoint
@app.post("/chat")
async def chat(request: QuestionRequest):
    # Check question is not empty
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if len(request.question) > 500:
        raise HTTPException(status_code=400, detail="Question too long")

    try:
        # Create request context
        context = RequestContext(
            user=User(id="default_user", name="Default User"),
            metadata={}
        )

        # Collect all responses from agent
        sql_query = ""
        message = ""
        rows = []

        async for component in agent.send_message(
            request_context=context,
            message=request.question
        ):
            # Extract simple text response
            if hasattr(component, 'simple_component') and component.simple_component:
                if hasattr(component.simple_component, 'text'):
                    message = component.simple_component.text

            # Extract SQL query if present
            if hasattr(component, 'rich_component') and component.rich_component:
                rc = component.rich_component
                if hasattr(rc, 'data') and isinstance(rc.data, dict):
                    if 'sql' in rc.data:
                        sql_query = rc.data['sql']
                    if 'rows' in rc.data:
                        rows = rc.data['rows']

        # Validate SQL if we got one
        if sql_query and not validate_sql(sql_query):
            return QuestionResponse(
                message="Sorry, that query is not allowed for security reasons.",
                sql_query=sql_query,
                rows=[],
                row_count=0,
                error="SQL validation failed"
            )

        # Return response
        if not message:
            message = "Query processed successfully"

        return QuestionResponse(
            message=message,
            sql_query=sql_query,
            rows=rows,
            row_count=len(rows)
        )

    except Exception as e:
        return QuestionResponse(
            message="Sorry, an error occurred while processing your question.",
            sql_query="",
            rows=[],
            row_count=0,
            error=str(e)
        )