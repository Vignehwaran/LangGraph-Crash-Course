

---

### 📄 `README.md` – Version 2

````markdown
# 🧠 LangGraph Crash Course

A hands-on beginner-to-pro crash course to learn and build with **LangGraph**, the framework for building **multi-step**, **stateful**, and **agent-powered** AI workflows using graphs.

---

## 🔍 What is LangGraph?

LangGraph is a graph-based orchestration engine built on top of [LangChain](https://github.com/langchain-ai/langchain), designed to manage **LLM workflows**, **tool calling**, and **state transitions** through **nodes and edges** — like a real graph.

It works well for:
- 🤖 Agent systems (e.g., planner → tool caller → summarizer)
- 👨‍⚖️ Human-in-the-loop approval flows
- 🧵 Stateful conversational agents
- 📄 Document processing pipelines

---

## 🧩 Key Components

| Component     | Description                                      |
|---------------|--------------------------------------------------|
| 🔹 Node        | A function or action unit in the graph           |
| 🔸 Edge        | Logical connections between nodes                |
| 📦 State       | Shared memory that flows between nodes           |
| 🧬 Graph       | A composition of nodes and edges (workflow)      |
| ⚙️ Statemachine | Optional logic engine to control next actions    |

---

## 🖼️ Visual Overview

![LangGraph Overview](./Screenshot%202025-07-14%20125642.png)

LangGraph builds on top of LangChain and integrates well with LangSmith for observability and tracing.

---

## 📁 What’s Inside This Repo?

| File | Description |
|------|-------------|
| `basic_graph.py`         | Hello world LangGraph using one node |
| `chat_with_memory.py`    | Stateful chatbot using `add_messages` |
| `tool_interrupt.py`      | HITL flow using `interrupt()` before tool calls |
| `multi_step_agents.py`   | Multi-node chain with conditional routing |
| `wrappers_logging.py`    | Wrapper example for logging tool calls |

---

## ⚙️ Setup

```bash
# Install dependencies
pip install langgraph langchain openai python-dotenv
````

If using Groq or Claude:

```bash
pip install langchain_groq
```

---

## 🚀 Run the Example

```bash
python basic_graph.py
```

Then start chatting and see how the flow works.

---

## 🛠️ Tools Integrated

* ✅ LangChain
* ✅ LangGraph
* ✅ OpenAI (or Groq, Claude, etc.)
* ✅ LangSmith (optional for debugging)
* ✅ dotenv (for environment management)

---

## 🌍 Resources

* [LangGraph Docs](https://docs.langchain.com/langgraph/)
* [LangChain GitHub](https://github.com/langchain-ai/langchain)
* [LangSmith Platform](https://smith.langchain.com/)

---

## 🙋‍♂️ Author

Built with ❤️ by **\[vigneshwaran]**
If this helped, give a ⭐ and feel free to contribute!

---

```

---

`
