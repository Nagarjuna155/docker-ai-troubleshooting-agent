from fastmcp import FastMCP
import subprocess

mcp = FastMCP("Docker MCP Server") #instance

#tools
@mcp.tool
def show_running_containers():
    """ Tool1: Show Running Containers"""
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def show_all_containers():
    """ Tool1: Show all continers"""
    result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def show_container_logs_by_name(container_name: str):
    """
    Tool2: Show logs for a specific Docker container by its name or ID.

    Use this when the user asks to see logs, debug an issue, investigate
    errors, or perform root cause analysis (RCA) for a particular container.

    Args:
        container_name: The name or container ID of the Docker container
            (e.g. "nginx", "my_app_1", or a container ID like "a1b2c3d4").

    Returns:
        The stdout/stderr log output of the container as a string.
        Returns an error message if the container does not exist or
        the docker command fails.
    """
    result = subprocess.run(["docker", "logs", "--tail", "200", container_name.strip()], capture_output=True, text=True)
    if result.returncode != 0:
            return f"Error fetching logs for '{container_name}': {result.stderr.strip()}"
    output = result.stdout.strip()
    return output if output else f"No logs found for container '{container_name}'."

if __name__ == "__main__":
    mcp.run()