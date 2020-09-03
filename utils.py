"""
MIT License

Copyright (c) 2020 Tremeschin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import neotermcolor
import shutil
import sys
import os

cprint = neotermcolor.cprint

# Set neotermcolor styles
neotermcolor.set_style('a', color='magenta', attrs='bold') # Action
neotermcolor.set_style('e', color='red',     attrs='bold') # Error
neotermcolor.set_style('w', color='yellow',  attrs='bold') # Warning
neotermcolor.set_style('i', color='cyan',    attrs='bold') # Info
neotermcolor.set_style('q', color='yellow',  attrs='bold') # Question
neotermcolor.set_style('c', color='blue',    attrs='bold') # Check
neotermcolor.set_style('o', color='green',   attrs='bold') # Ok


# Intents for printing pretty stuff
class Indents:
    ACTION =   "\n\n  >> text\n"
    ERROR =    "[## ERROR ##] text"
    WARNING =  "[WARNING] :: text"
    INFO =     "[INFO] text"
    QUESTION = " > text:"
    CHECK =    "[CHECKING] text"
    OK =       "[OK] text"


# Utilities class
class Utils:
    def __init__(self, main):
        self.main = main
        self.ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
    
    # (S)tyled (print) with indents
    def sprint(self, text: str, style="info") -> None:
        # Defaults and indents
        indent = {
            "a": Indents.ACTION,
            "e": Indents.ERROR,
            "w": Indents.WARNING,
            "q": Indents.QUESTION,
            "c": Indents.CHECK,
            "o": Indents.OK,
        }.get(style[0], Indents.INFO)
        
        cprint(indent.replace("text", text), style=style)

    # Make directory if doesn't exist
    def mkdir_dne(self, path: str, check: bool = True) -> None:
        
        # Warn "checking" for the user
        self.sprint(f"MKDIR DNE [{path}]", 'c')

        # Does directory already exist?
        if not os.path.exists(path):
            self.sprint(f"Directory doesn't exist, creating", 'w')
            os.makedirs(path)
            if check:
                if not os.path.exists(path):
                    self.sprint(f"Could NOT create directory [{path}]", 'e')
                    sys.exit(-1)
            self.sprint("Directory created successfully!!", 'o')
        else:
            # Path already exist
            self.sprint("Path already exists", 'o')
    
    # Delete a directory and its contents
    def rmdir(self, path: str) -> None:

        # Warn "checking" for the user
        self.sprint(f"RMDIR [{path}]", 'c')
        
        if os.path.isdir(path):

            # Delete the directory
            shutil.rmtree(path, ignore_errors=True)
            
            # Directory still exists? Ew, error
            if os.path.isdir(path):
                self.sprint(f"Tried to remove directory [{path}] but still exists", 'e')
                sys.exit(-1)
        else:
            self.sprint("Directory doesn't exist, skipping...", 'o')

    # Same as `sed -i "s/old/new/g" path`
    def sed_replace(self, old: str, new: str, path: str) -> None:

        self.sprint(f"Replacing [ \"{old}\" ] --> [ \"{new}\" ] on file [{path}]", 'i')
        
        # Read every line of original file
        with open(path, "r") as f:
            data = [line for line in f]
        
        # Replace every line from old to new
        data = [line.replace(old, new) for line in data]
        
        # Overwrite the file with new replaced values
        with open(path, "w") as f:
            for line in data:
                f.write(line)

    # Get the environment vars modified with env_vars dict
    def custom_env(self, env_vars: dict) -> dict:
        env = os.environ.copy()
        for env_var in env_vars.keys():
            env[env_var] = env_vars[env_var]
        return env


# Python's subprocess utilities because I'm lazy remembering things
class SubprocessUtils():

    def __init__(self, name, utils, context):

        debug_prefix = "[SubprocessUtils.__init__]"

        self.name = name
        self.utils = utils
        self.context = context

        print(debug_prefix, "Creating SubprocessUtils with name: [%s]" % name)

    # Get the commands from a list to call the subprocess
    def from_list(self, list):

        debug_prefix = "[SubprocessUtils.run]"

        print(debug_prefix, "Getting command from list:")
        print(debug_prefix, list)

        self.command = list

    # Run the subprocess with or without a env / working directory
    def run(self, working_directory=None, env=None, shell=False):

        debug_prefix = "[SubprocessUtils.run]"
        
        print(debug_prefix, "Popen SubprocessUtils with name [%s]" % self.name)
        
        # Copy the environment if nothing was changed and passed as argument
        if env is None:
            env = os.environ.copy()
        
        # Runs the subprocess based on if we set or not a working_directory
        if working_directory == None:
            self.process = subprocess.Popen(self.command, env=env, stdout=subprocess.PIPE, shell=shell)
        else:
            self.process = subprocess.Popen(self.command, env=env, cwd=working_directory, stdout=subprocess.PIPE, shell=shell)

    # Get the newlines from the subprocess
    # This is used for communicating Dandere2x C++ with Python, simplifies having dealing with files
    def realtime_output(self):
        while True:
            # Read next line
            output = self.process.stdout.readline()

            # If output is empty and process is not alive, quit
            if output == '' and self.process.poll() is not None:
                break
            
            # Else yield the decoded output as subprocess send bytes
            if output:
                yield output.strip().decode("utf-8")

    # Wait until the subprocess has finished
    def wait(self):

        debug_prefix = "[SubprocessUtils.wait]"

        print(debug_prefix, "Waiting SubprocessUtils with name [%s] to finish" % self.name)

        self.process.wait()

    # Kill subprocess
    def terminate(self):

        debug_prefix = "[SubprocessUtils.terminate]"

        print(debug_prefix, "Terminating SubprocessUtils with name [%s]" % self.name)

        self.process.terminate()

    # See if subprocess is still running
    def is_alive(self):

        debug_prefix = "[SubprocessUtils.is_alive]"

        # Get the status of the subprocess
        status = self.process.poll()

        # None? alive
        if status == None:
            return True
        else:
            print(debug_prefix, "SubprocessUtils with name [%s] is not alive" % self.name)
            return False