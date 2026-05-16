# MSFoundryAgentMemory

This repository demonstrates how to build an Azure Foundry agent with persistent user memory using the Azure AI Agents SDK (Python, async).

## Features
- Creates an agent with vector store memory for user preferences
- Uses Azure AI Agents and Projects SDKs
- Demonstrates FileSearchTool integration for memory
- Example chat loop: remembers and recalls user preferences
- Cleans up resources after execution

## Requirements
- Python 3.8+
- Azure CLI (for authentication)
- Azure AI Agents SDK (`azure-ai-agents`)
- Azure Identity SDK (`azure-identity`)
- python-dotenv
- An Azure Foundry project endpoint and model

## Setup
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install azure-ai-agents azure-identity python-dotenv
   ```
3. Create a `.env` file with the following variables:
   ```env
   FOUNDRY_PROJECT_ENDPOINT=<your_foundry_project_endpoint>
   FOUNDRY_MODEL=<your_foundry_model_name>
   ```
4. Login to Azure CLI:
   ```bash
   az login
   ```

## Usage
Run the main script:
```bash
python agent_memory.py
```

The script will:
- Create a vector store for user memory
- Create an agent with memory and file search capabilities
- Start a conversation, storing and recalling user preferences
- Clean up resources at the end

## Notes
- To persist agent and memory, remove the cleanup section in `main()`.
- This is a minimal example for learning and experimentation.

## License
MIT License
