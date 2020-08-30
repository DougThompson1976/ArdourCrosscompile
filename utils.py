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
    ACTION =   "  >> text"
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
    def sprint(self, text, style="info"):
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
    def mkdir_dne(self, path, check=True):
        
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
    def rmdir(self, path):

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
    def sed_replace(self, old, new, path):
        # Read every line of original file
        with open(path, "r") as f:
            data = [line for line in f]
        
        # Replace every line from old to new
        data = [line.replace(old, new) for line in data]
        
        # Overwrite the file with new replaced values
        with open(path, "w") as f:
            for line in data:
                f.write(line)

