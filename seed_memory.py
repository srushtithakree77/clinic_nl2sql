import os
import asyncio
from dotenv import load_dotenv
from vanna_setup import create_agent
from vanna.core.user import RequestContext, User

load_dotenv()

print("Creating agent...")
agent = create_agent()

examples = [
    "How many patients do we have?",
    "List all doctors and their specializations",
    "Which city has the most patients?",
    "What is the total revenue?",
    "Show all unpaid invoices",
    "Which doctor has the most appointments?",
    "How many cancelled appointments are there?",
    "Top 5 patients by spending",
    "Show monthly appointment count",
    "List patients who visited more than 3 times",
    "Average treatment cost by specialization",
    "Show all no-show appointments",
    "How many male and female patients do we have?",
    "Show overdue invoices with patient names",
    "Show revenue by doctor"
]

async def test_question(question):
    context = RequestContext(
        user=User(id="default_user", name="Default User"),
        metadata={}
    )
    responses = []
    async for component in agent.send_message(
        request_context=context,
        message=question
    ):
        responses.append(str(component))
    return responses

async def main():
    print(f"Testing agent with {len(examples)} questions...\n")
    passed = 0
    failed = 0

    for i, question in enumerate(examples, 1):
        try:
            print(f"Q{i}: {question}")
            responses = await test_question(question)
            for r in responses:
                print(f"  → {r}")
            print("-" * 50)
            passed += 1
        except Exception as e:
            print(f"  Error: {e}")
            print("-" * 50)
            failed += 1

    print(f"\nDone! Passed: {passed}/15 | Failed: {failed}/15")

asyncio.run(main())