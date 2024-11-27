from typing import Optional

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


async def execute_code_block(message_content: str) -> Optional[str]:
    """
    Extract and execute Python code from the user's request asynchronously.
    :param message_content: The content of the user's message.
    :return: Execution result or error message, or None if no code block is found.
    """
    executor = LocalCommandLineCodeExecutor(work_dir="coding")
    code_block = executor.code_extractor.extract_code_blocks(message_content)

    if not code_block:
        return "No code block found in the message."

    try:
        # Execute code asynchronously (using asyncio.subprocess.create_subprocess_exec) 
        process = await asyncio.create_subprocess_exec(
            "python", "-c", code_block[0],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stderr:
            return f"Error executing code: {stderr.decode()}"
        else:
            return stdout.decode()

    except SyntaxError as e:
        return f"Syntax error in code: {e}"
    except NameError as e:
        return f"Name error in code: {e}"
    except IndexError as e:
        return f"Index error in code: {e}"
    except TypeError as e:
        return f"Type error in code: {e}"
    except ZeroDivisionError as e:
        return f"Division by zero error in code: {e}"
    except Exception as e:  # Catch other unexpected errors
        return f"An unexpected error occurred: {e}"


def execute_code_block_sync(message_content: str) -> Optional[str]:
    """
    Synchronous wrapper for execute_code_block.
    """
    return asyncio.run(execute_code_block(message_content))


def create_coding_agent() -> AssistantAgent:
    agent = AssistantAgent(
        name="Coding Agent",
        system_message=(
            "You are an advanced coding assistant. "
            "You can interpret user prompts, generate Python code, execute it, "
            "and assist with debugging or enhancements as needed. "
            "Provide clear, detailed explanations of your actions."
            "Display the code you generate in a single code block in your answer."
            "Don't generate markdown code, only for code you provide and only once"
            "and return 'TERMINATE' when the task is done."
        ),
        llm_config=LLM_CONFIG,
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

    # Register the synchronous wrapper function
    user_proxy.register_for_execution(name="execute_python")(execute_code_block_sync)

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