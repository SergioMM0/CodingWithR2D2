from autogen import AssistantAgent
from autogen.coding.local_commandline_code_executor import LocalCommandLineCodeExecutor

from config import LLM_CONFIG

def after_execution(agent, execution_result):
    if execution_result.get('success'):
        output = execution_result.get('output', '')
        agent.send_message("The code executed successfully.")
        if output:
            agent.send_message(f"The output is:\n```\n{output}\n```")
    else:
        error_output = execution_result.get('output', 'No output available.')
        agent.send_message(f"There was an error executing the code:\n```\n{error_output}\n```")
        agent.send_message("Please debug the code and provide a corrected version.")

def create_coding_agent() -> AssistantAgent:
    agent = AssistantAgent(
        name="Coding Agent",
        system_message=(
            "You are a helpful AI assistant. "
            "You can help with writing Python code, "
            "verify the correctness of the code by executing it, "
            "provide debugging assistance if there are errors, "
            "display the output in a code block, "
            "and return 'TERMINATE' when the task is done."
        ),
        llm_config=LLM_CONFIG,
        code_execution_config={
            "allow_code_execution": True,
            "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
            "max_output_length": 1000,
        },
    )

    # Set the after_execution callback
    agent.after_execution = after_execution

    return agent


def create_user_proxy():
    user_proxy = AssistantAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )
    return user_proxy


def main():
    user_proxy = create_user_proxy()
    coding_agent = create_coding_agent()

    # Prompt the user for input
    message = ""
    while not message.strip():
        message = input("Please enter your question or task for the assistant:\n")

    chat_result = user_proxy.initiate_chat(
        coding_agent,
        cache=None,
        message=message
    )
    print(chat_result)


if __name__ == "__main__":
    main()
