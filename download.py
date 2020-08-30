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

from git import Repo, RemoteProgress
from tqdm import tqdm
import time
import wget


class Download:
    def __init__(self, main):
        self.main = main

    def git_clone(self, url, save):
        if url.endswith("/"):
            url = url[0:-1]
        self.repo_name = url.split("/")[-1]
        self.main.utils.sprint(f"Clone repo [{self.repo_name}] from url [{url}] saving to [{save}]", 'i')
        Repo.clone_from(url, save, progress=self.git_clone_progress_bar)

    def git_clone_progress_bar(self, _, current, total, speed):
        percentage = (current/total)*100
        print(f"\r Cloning repo [{self.repo_name}] | {percentage:0.2f}% | {speed}", end='', flush=True)

    def wget_progress_bar(self, current, total, width=80):
        # current         \propto time.time() - startdownload 
        # total - current \propto eta
        # eta = (total-current)*(time.time()-startdownload)) / current

        try: # div by zero
            eta = int(( (time.time() - self.start) * (total - current) ) / current)
        except Exception:
            eta = 0

        avgdown = ( current / (time.time() - self.start) ) / 1024

        currentpercentage = int(current / total * 100)
        
        print("\r Downloading file [{}]: [{}%] [{:.2f} MB / {:.2f} MB] ETA: [{} sec] AVG: [{:.2f} kB/s]".format(self.download_name, currentpercentage, current/1024/1024, total/1024/1024, eta, avgdown), end='', flush=True)
            

    def wget(self, url, save, name="Undefined"):
        self.download_name = name
        self.start = time.time()
        self.main.utils.sprint(f"Get file from URL [{url}] saving to [{save}]", 'i')
        wget.download(url, save, bar=self.wget_progress_bar)