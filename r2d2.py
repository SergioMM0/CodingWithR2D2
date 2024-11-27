from autogen import AssistantAgent
from autogen.coding.local_commandline_code_executor import LocalCommandLineCodeExecutor
from autogen import UserProxyAgent

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


def execute_code_block(message_content: str) -> str:
    """
    Extract and execute Python code from the user's request.
    :param message_content: The content of the user's message.
    :return: Execution result or error message.
    """
    executor = LocalCommandLineCodeExecutor(work_dir="coding")
    code_block = executor.code_extractor.extract_code_blocks(message_content)
    if code_block:
        try:
            result = executor.execute_code_blocks(code_block)
            return result
        except Exception as e:
            return str(e)
    return None


def create_coding_agent() -> AssistantAgent:
    agent = AssistantAgent(
        name="Coding Agent",
        system_message=(
            "You are an advanced coding assistant. "
            "You can interpret user prompts, generate Python code, execute it, "
            "and assist with debugging or enhancements as needed. "
            "Provide clear, detailed explanations of your actions."
            "Display the code code you generate in a single code block in your answer."
            "Don't generate markdown code, only for code you provide and only once"
            "and return 'TERMINATE' when the task is done."
        ),
        llm_config=LLM_CONFIG,
        # code_execution_config={
        #    "allow_code_execution": True,
        #    "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
        #    "max_output_length": 1000,
        # },
    )

    # Set the after_execution callback
    agent.after_execution = after_execution

    return agent


def create_user_proxy():
    user_proxy = UserProxyAgent(
        name="User",
        llm_config=False,
        human_input_mode="NEVER",
        code_execution_config={
            "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
        }
    )

    user_proxy.register_for_execution(name="execute_python")(execute_code_block)

    return user_proxy


def main():
    user_proxy = create_user_proxy()
    coding_agent = create_coding_agent()

    # Start the conversation
    chat_result = user_proxy.initiate_chat(
        coding_agent,
        cache=None,
    )
    print(chat_result)


if __name__ == "__main__":
    main()
