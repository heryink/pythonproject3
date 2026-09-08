from anthropic import Anthropic
import os
from dotenv import load_dotenv
import json
from statistics import mean

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
client = Anthropic(
    api_key=api_key,
    base_url="https://openrouter.ai/api")

model = "anthropic/claude-haiku-4-5"

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

with open("system.txt", "r") as file:
    system_prompt = file.read()

def chat(messages,temperature=None,stop_sequences=None):
    params={
        "model": model,
        "max_tokens": 1024,
        "messages": messages,
    }
    if temperature:
      params["temperature"] = temperature
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    answer = client.messages.create(**params)
    return answer.content[0].text


def generate_dataset():
    prompt = """
    Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for simle solutions like testing an api through request. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

    Example output:
    ```json
    [
      {
        "task": "Description of task",
      },
      ...additional
    ]
    ```
    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
    * Focus on tasks that do not require writing much code

    Please generate 3 objects.
    """
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    dataset = json.loads(text)
    return dataset
data = generate_dataset()
with open("datasets.json", "w") as file:
    json.dump(data, file,indent=4)


def run_prompt(test):
    """"merges the prompt together with tasks and other input then return the result"""
    prompt = f"""solve this problems you dumbass:
    {test["task"]}"""
    message = []
    add_user_message(message, prompt)
    output = chat(message)
    return output


def grade_by_model(test,output):
    eval_prompt = f"""
        You are an expert code reviewer. Evaluate this AI-generated solution.

        Task: {test["task"]}
        Solution: {output}

        Respond with JSON. Keep your response concise and direct. the score represent how well it perform based on the instructionbelow
Example response shape:
{{
    "strengths": string[],
    "weaknesses": string[],
    "reasoning": string,
    "score": number
}} """
    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")

    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)


def run_test_case(test):
    """return grading element"""
    output = run_prompt(test)
    model_grade = grade_by_model(test, output)
    score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    return {
        "output": output,
        "test": test,
        "score": score,
        "reasoning": reasoning,
    }

def run_evaluation(dataset):
    """iterate and grade the response to the dataset task """
    results = []

    for test in dataset:
        result = run_test_case(test)
        results.append(result)
    print(results)
    avg_score = mean(result["score"] for result in results)
    print(f"avg score: {avg_score}")
    return results



with open("datasets.json", "r") as file:
    dataset = json.load(file)
    results = run_evaluation(dataset)

print(json.dumps(results, indent=2))




