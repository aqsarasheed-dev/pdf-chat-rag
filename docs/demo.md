Type your question. Type 'exit' to quit.

You: guarrails
Assistant: I don't know based on the document. (retrieval confidence too low)
Debug: best_distance=0.8454 (threshold=0.45)

You: /find guardrails
Assistant: Found 1 chunk(s) containing 'guardrails':
  page=2 chunk_in_page=0
   * Observability tools track how many input and output tokens are used per user, per feature, or per day. * This helps developers catch runaway costs or optimize prompts to save money. #### 4. Performance and Latency AI models are notoriously slow com
--------------------------------------------------

You: guardrails

Assistant: Observability monitors security risks in real-time, specifically detecting **Prompt Injections** where a user attempts to "jailbreak" or hack the AI.
Citations: page 2

Sources used:
  Source 1: page=2 distance=0.7984

You: tracking

Assistant: Based on the sources, **tracking** is a key component of **LLM Observability**, which refers to the practice of tracking, measuring, and understanding the internal state and behavior of Large Language Model (LLM) applications in real-time.

Specifically, **Tracing** (tracking the workflow) is one of the 5 Key Pillars of LLM Observability. It tracks the entire journey of a request through modern AI applications that may use chains, agents, and databases (such as RAG). Additionally, LLM providers charge money based on **tokens**, which are roughly parts of words, making token tracking relevant for cost management.
Citations: page 1

Sources used:
  Source 1: page=1 distance=0.6765
  Source 2: page=1 distance=0.6765
  Source 3: page=1 distance=0.6765

You: Does the PDF mention guardrails? If yes, quote it and explain

Assistant: Yes, the PDF mentions guardrails.

**Quote:**
"#### 5. Guardrails and Security Observability monitors security risks in real-time: * **Prompt Injections:** Detecting if a user is trying to "jailbreak" or hack the AI"

**Explanation:**
The document lists "Guardrails and Security" as a key area of observability. It explains that observability tools monitorsecurity risks in real-time, specifically highlighting the detection of prompt injections where users attempt to "jailbreak" or hack the AI.
Citations: page 2

Sources used:
  Source 1: page=2 distance=0.6711


You: what is observability in llm

Assistant: LLM Observability is the practice of tracking, measuring, and understanding the internal state and behavior of Large Language Model (LLM) applications in real-time, focusing on the unique, unpredictable nature of AI-generated text and complex AI workflows.

Evidence:
- "LLM Observability refers to the practice of tracking, measuring, and understanding the internal state and behavior of Large Language Model (LLM) applications in real-time." (page 1)
- "LLM Observability focuses on the unique, unpredictable nature of AI-generated text and complex AI workflows." (page 1)
Citations: page 1, page 2

Sources used:
  Source 1: page=1 distance=0.2062
  Source 2: page=1 distance=0.3352
  Source 3: page=2 distance=0.3745
  Source 4: page=2 distance=0.5374
  Source 5: page=2 distance=0.6812
  Source 6: page=1 distance=0.6952
  Source 7: page=1 distance=0.8516
You: exit
Bye.