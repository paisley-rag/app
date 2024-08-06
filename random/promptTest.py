
from llama_index.core import get_response_synthesizer, PromptTemplate
from llama_index.core.response_synthesizers import ResponseMode


def display_prompts(prompts_dict):
    for k, p in prompts_dict.items():
        print(f"Prompt Key:  {k}")
        print("Text: ")
        print(p.get_template())
        print("-"*30)


synth = get_response_synthesizer(
    response_mode=ResponseMode.SIMPLE_SUMMARIZE
)

prompt = synth.get_prompts()

display_prompts(prompt)


new_prompt = (
    "Context information is below.\n"
    "-----------------------------\n"
    "{context_str}\n"
    "-----------------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query in French.\n"
    "Query: {query_str}\n"
    "Answer: "
)
new_template = PromptTemplate(new_prompt)

synth.update_prompts(
    {"text_qa_template": new_template}
)

prompt = synth.get_prompts()

display_prompts(prompt)
