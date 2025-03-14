import os
from openai import OpenAI

# Initialize the Mistral-based LLM
class MistralLLM:
    def __init__(self, base_url="http://localhost:1234/v1", model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF", api_key="API_KEY"): # Chnage to LM studio API Key
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def chat(self, prompt, temperature=0.5, max_tokens=30000):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an **expert smart contract auditor**. "
                            "Your task is to analyze the given smart contract and find **all possible security vulnerabilities**.\n\n"

                            "🔹 **Important Rules:**\n"
                            "- **Do NOT summarize a security checklist.**\n"
                            "- **Do NOT list generic security categories.**\n"
                            "- **Only report real vulnerabilities found in the contract.**\n"
                            "- **For each vulnerability, strictly follow this format:**\n\n"

                            "####\n"
                            "**[Title]** - A short, descriptive name for the vulnerability.\n"
                            "**[Description]** - Explain how the issue occurs and why it's a problem.\n"
                            "**[Summary]** - A concise summary of the vulnerability.\n"
                            "**[Impact]** - Describe how an attacker could exploit this issue.\n"
                            "**[Affected Function]** - The function where this vulnerability is located.\n\n"

                            "🔹 **Analysis Process:**\n"
                            "1️⃣ **Understand the Contract:** Read the contract to grasp its intended behavior.\n"
                            "2️⃣ **Determine User Flow:** Analyze how users interact with different functions.\n"
                            "3️⃣ **Identify External Calls:** Detect `call`, `delegatecall`, `transfer`, and `inline assembly` usage.\n"
                            "4️⃣ **Match Against Security Checklist:** Compare implementation with known security patterns.\n"
                            "5️⃣ **Detect Business Logic Flaws:** Look for broken access control, logic errors, and improper conditions.\n"
                            "6️⃣ **Draft Findings in Short:** Use only 5 words max per finding.\n"
                            "7️⃣ **Format Final Structured Report:** Clearly present each vulnerability.\n\n"

                            "🔹 **Final Report Rules:**\n"
                            "- **Each vulnerability must be reported separately.**\n"
                            "- **If multiple vulnerabilities exist, repeat the format for each one.**\n"
                            "- **Findings must be reported after `####`.**\n"
                            "- **If no vulnerabilities exist, state `No vulnerabilities detected` after `####`.**\n"
                            "- **Use Markdown formatting for readability.**\n\n"

                            "Now, analyze the smart contract and generate a **structured vulnerability report** for each issue found."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Access the message content and token usage
            response_content = completion.choices[0].message.content
            usage = completion.usage
            total_tokens = usage.total_tokens if usage else "Unknown"
            return response_content, total_tokens
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Error generating response.", 0

# Function to query the LLM
def query_document(query, llm):
    return llm.chat(query, max_tokens=30000)
