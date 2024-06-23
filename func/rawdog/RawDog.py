import subprocess
import json
import ast
import tempfile
import sys
from dotenv import get_key


class LLM:
    def __init__(self) -> None:self.messages = [];self.c = None
    def add_message(self, role: str, content: str, base64_image: str = "") -> None:...
    def run(self, prompt: str) -> str:...


class RawDog:
    def __init__(self, prompt: str, llm: LLM) -> None:
        self.llm = llm
        self.prompt = prompt

    def install_pip_packages(self, *packages: str):
        python_executable = rf'{get_key(".env", "PYTHON_EXE")}'
        print(f"Installing {', '.join(packages)} with pip...")
        return subprocess.run(
            [python_executable, "-m", "pip", "install", *packages],
            capture_output=True,
            check=True,
        )
    
    def parse_script(self, response: str) -> tuple[str, str]:
        """Split the response into a message and a script.

        Expected use is: run the script if there is one, otherwise print the message.
        """
        # Parse delimiter
        n_delimiters = response.count("```")
        if n_delimiters < 2:
            return response, ""
        segments = response.split("```")
        message = f"{segments[0]}\n{segments[-1]}"
        script = "```".join(segments[1:-1]).strip()  # Leave 'inner' delimiters alone

        # Check for common mistakes
        if script.split("\n")[0].startswith("python"):
            script = "\n".join(script.split("\n")[1:])
        try:  # Make sure it isn't json
            script = json.loads(script)
        except Exception:
            pass
        try:  # Make sure it's valid python
            ast.parse(script)
        except SyntaxError:
            return f"Script contains invalid Python:\n{response}", ""
        return message, script

    def _execute_script_in_subprocess(self, script) -> tuple[str, str, int]:
        """Write script to tempfile, execute from .rawdog/venv, stream and return output"""
        output, error, return_code = "", "", 0
        try:
            python_executable = rf'{get_key(".env", "PYTHON_EXE")}'
            with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_script:
                tmp_script_name = tmp_script.name
                tmp_script.write(script)
                tmp_script.flush()

                process = subprocess.Popen(
                    [python_executable, tmp_script_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.DEVNULL,  # Raises EOF error if subprocess asks for input
                    text=True,
                )
                while True:
                    _stdout = process.stdout.readline()
                    _stderr = process.stderr.readline()
                    if _stdout:
                        output += _stdout
                        print(_stdout, end="")
                    if _stderr:
                        error += _stderr
                        print(_stderr, end="", file=sys.stderr)
                    if _stdout == "" and _stderr == "" and process.poll() is not None:
                        break
                return_code = process.returncode
        except Exception as e:
            error += str(e)
            print(e)
            return_code = 1
        return output, error, return_code

    def execute_script(self, script: str) -> tuple[str, str, int]:
        """Execute script in subprocess and stream output"""
        return self._execute_script_in_subprocess(script)        
    
    def run(self, keepHistory: bool = False) -> ...:
        the_copy = self.llm.messages.copy()
        self.llm.add_message("user", self.prompt)
        _continue = True
        while _continue is True:
            _continue = False
            error, script, output, return_code = "", "", "", 0
            try:
                message, script = self.parse_script(self.llm.run())
                if script:
                    output, error, return_code = self.execute_script(script)
                elif message:
                    print(message)
            except KeyboardInterrupt:
                break

            if output:
                self.llm.add_message("user", f"LAST SCRIPT OUTPUT:\n{output}")
                if output.strip().endswith("CONTINUE"):
                    _continue = True
            if error:
                self.llm.add_message("user", f"Error: {error}")
            if return_code != 0:
                retries -= 1
                if retries > 0:
                    print("Retrying...\n")
                    _continue = True

        if not keepHistory:
            self.llm.messages = the_copy