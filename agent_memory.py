import asyncio
import os
from azure.ai.projects.aio import AIProjectClient
from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import (
    MessageRole,
    FileSearchTool,
)
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()


async def chat(
    agents_client: AgentsClient,
    thread_id: str,
    agent_id: str,
    user_message: str,
) -> str:
    """Send a message and return the assistant's reply."""
    await agents_client.messages.create(
        thread_id=thread_id,
        role=MessageRole.USER,
        content=user_message,
    )

    run = await agents_client.runs.create_and_process(
        thread_id=thread_id,
        agent_id=agent_id,
    )

    if run.status == "failed":
        raise RuntimeError(f"Run failed: {run.last_error}")

    messages = agents_client.messages.list(thread_id=thread_id)
    async for msg in messages:
        if msg.role == MessageRole.AGENT:
            return msg.text_messages[-1].text.value

    return "(no response)"


async def main():
    credential = AzureCliCredential()

    # ✅ AgentsClient is constructed directly — NOT via project.agents
    async with AgentsClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        credential=credential,
    ) as agents_client:

        # 1. Create vector store — lives directly on AgentsClient
        vector_store = await agents_client.vector_stores.create_and_poll(
            name="user_memory_store"
        )
        print(f"Vector store: {vector_store.id}")

        # 2. Use FileSearchTool helper for cleaner tool/resource setup
        file_search = FileSearchTool(vector_store_ids=[vector_store.id])

        # 3. Create agent
        agent = await agents_client.create_agent(
            model=os.environ["FOUNDRY_MODEL"],
            name="assistant_with_memory",
            instructions=(
                "You are a helpful assistant. "
                "Remember user preferences and refer back to them naturally. "
                "User scope: user:praveen"
            ),
            tools=file_search.definitions,
            tool_resources=file_search.resources,
        )
        print(f"Agent: {agent.id}")

        # 4. Create a thread — retains full conversation history automatically
        thread = await agents_client.threads.create()
        print(f"Thread: {thread.id}")

        try:
            response = await chat(agents_client, thread.id, agent.id, "My favourite color is blue.")
            print(f"Assistant: {response}")

            response = await chat(agents_client, thread.id, agent.id, "What is my favourite color?")
            print(f"Assistant: {response}")

        finally:
            
            # Clean up — remove if you want the agent/store to persist
            await agents_client.vector_stores.delete(vector_store.id)
            await agents_client.delete_agent(agent.id)


asyncio.run(main())