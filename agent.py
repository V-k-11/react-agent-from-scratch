import re
import json
from pathlib import Path
from groq import Groq
from utils.message import Message
from tools import TOOLS, TOOLS_DESCRIPTION, get_tool


class ReActAgent:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile", max_iterations: int = 10):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.max_iterations = max_iterations
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        template = Path("prompts/system_prompt.txt").read_text()
        return template.format(tools_description=TOOLS_DESCRIPTION)

    def _call_llm(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[m.to_dict() for m in messages],
            temperature=0.1,
            max_tokens=1024,
            stop=["PAUSE"],
        )
        return response.choices[0].message.content.strip()

    def _parse_action(self, text: str):
        """Returns (tool_name, params_dict) or None."""
        match = re.search(r"Action:\s*(\w+):\s*(\{.*?\})", text, re.DOTALL)
        if not match:
            return None
        tool_name = match.group(1).strip()
        try:
            params = json.loads(match.group(2))
        except json.JSONDecodeError:
            params = {}
        return tool_name, params

    def _extract_final_answer(self, text: str):
        match = re.search(r"Final Answer:\s*(.*)", text, re.DOTALL)
        return match.group(1).strip() if match else None

    def run(self, user_query: str):
        """
        Generator yielding step dicts:
          {"type": "thought"|"action"|"observation"|"final"|"error", "content": str, "step": int}
        """
        messages = [
            Message("system", self.system_prompt),
            Message("user", user_query),
        ]

        for step in range(1, self.max_iterations + 1):
            llm_output = self._call_llm(messages)
            messages.append(Message("assistant", llm_output))

            # Yield thought
            thought_match = re.search(r"Thought:(.*?)(?=Action:|Final Answer:|$)", llm_output, re.DOTALL)
            if thought_match:
                yield {"type": "thought", "content": thought_match.group(1).strip(), "step": step}

            # Check for final answer
            final = self._extract_final_answer(llm_output)
            if final:
                yield {"type": "final", "content": final, "step": step}
                return

            # Parse and execute action
            action = self._parse_action(llm_output)
            if not action:
                yield {"type": "error", "content": "No valid Action found in LLM response. Stopping.", "step": step}
                return

            tool_name, params = action
            yield {
                "type": "action",
                "content": f"Tool: **{tool_name}**  |  Input: `{json.dumps(params)}`",
                "step": step
            }

            tool_fn = get_tool(tool_name)
            if not tool_fn:
                observation = f"Unknown tool '{tool_name}'. Available: {list(TOOLS.keys())}"
            else:
                try:
                    observation = tool_fn(params)
                except Exception as e:
                    observation = f"Tool execution error: {e}"

            yield {"type": "observation", "content": observation, "step": step}
            messages.append(Message("user", f"Observation: {observation}"))

        yield {"type": "error", "content": "Reached maximum iterations without a final answer.", "step": self.max_iterations}