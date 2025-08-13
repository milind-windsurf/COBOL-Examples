#!/usr/bin/env python3
"""
Advanced features for the custom shell
"""

import os
import re
import fnmatch
from typing import List, Dict, Optional


class AdvancedFeatures:
    """Additional zsh-like features"""
    
    @staticmethod
    def glob_expand(pattern: str) -> List[str]:
        """Expand glob patterns like *.py, **/*.txt"""
        import glob
        
        if '**' in pattern:
            return glob.glob(pattern, recursive=True)
        else:
            return glob.glob(pattern)
            
    @staticmethod
    def brace_expand(text: str) -> List[str]:
        """Expand brace patterns like {a,b,c} or {1..10}"""
        brace_pattern = r'\{([^}]+)\}'
        match = re.search(brace_pattern, text)
        
        if not match:
            return [text]
            
        brace_content = match.group(1)
        prefix = text[:match.start()]
        suffix = text[match.end():]
        
        if '..' in brace_content:
            parts = brace_content.split('..')
            if len(parts) == 2:
                try:
                    start, end = int(parts[0]), int(parts[1])
                    return [f"{prefix}{i}{suffix}" for i in range(start, end + 1)]
                except ValueError:
                    pass
                    
        items = brace_content.split(',')
        results = []
        for item in items:
            expanded = AdvancedFeatures.brace_expand(f"{prefix}{item.strip()}{suffix}")
            results.extend(expanded)
            
        return results
        
    @staticmethod
    def command_substitution(command: str) -> str:
        """Handle command substitution like $(command) or `command`"""
        import subprocess
        
        dollar_pattern = r'\$\(([^)]+)\)'
        
        def replace_dollar(match):
            cmd = match.group(1)
            try:
                result = subprocess.check_output(
                    cmd, shell=True, text=True, stderr=subprocess.DEVNULL
                ).strip()
                return result
            except subprocess.CalledProcessError:
                return ""
                
        command = re.sub(dollar_pattern, replace_dollar, command)
        
        backtick_pattern = r'`([^`]+)`'
        
        def replace_backtick(match):
            cmd = match.group(1)
            try:
                result = subprocess.check_output(
                    cmd, shell=True, text=True, stderr=subprocess.DEVNULL
                ).strip()
                return result
            except subprocess.CalledProcessError:
                return ""
                
        command = re.sub(backtick_pattern, replace_backtick, command)
        
        return command
        
    @staticmethod
    def tilde_expand(path: str) -> str:
        """Expand ~ to home directory"""
        return os.path.expanduser(path)
        
    @staticmethod
    def process_redirections(args: List[str]) -> tuple:
        """Process redirection operators like >, >>, <"""
        stdin_file = None
        stdout_file = None
        stderr_file = None
        append_mode = False
        
        filtered_args = []
        i = 0
        
        while i < len(args):
            arg = args[i]
            
            if arg == '>':
                if i + 1 < len(args):
                    stdout_file = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg == '>>':
                if i + 1 < len(args):
                    stdout_file = args[i + 1]
                    append_mode = True
                    i += 2
                else:
                    i += 1
            elif arg == '<':
                if i + 1 < len(args):
                    stdin_file = args[i + 1]
                    i += 2
                else:
                    i += 1
            elif arg == '2>':
                if i + 1 < len(args):
                    stderr_file = args[i + 1]
                    i += 2
                else:
                    i += 1
            else:
                filtered_args.append(arg)
                i += 1
                
        return filtered_args, stdin_file, stdout_file, stderr_file, append_mode


class JobControl:
    """Job control functionality"""
    
    def __init__(self):
        self.jobs = {}
        self.job_counter = 0
        
    def add_job(self, process, command: str) -> int:
        """Add a background job"""
        self.job_counter += 1
        self.jobs[self.job_counter] = {
            'process': process,
            'command': command,
            'status': 'running'
        }
        return self.job_counter
        
    def list_jobs(self):
        """List all jobs"""
        for job_id, job_info in self.jobs.items():
            status = job_info['status']
            command = job_info['command']
            print(f"[{job_id}]  {status}    {command}")
            
    def kill_job(self, job_id: int):
        """Kill a specific job"""
        if job_id in self.jobs:
            process = self.jobs[job_id]['process']
            process.terminate()
            del self.jobs[job_id]
            
    def update_job_status(self):
        """Update status of all jobs"""
        completed_jobs = []
        for job_id, job_info in self.jobs.items():
            process = job_info['process']
            if process.poll() is not None:
                job_info['status'] = 'done'
                completed_jobs.append(job_id)
                
        for job_id in completed_jobs:
            del self.jobs[job_id]


class ZshLikeCompletion:
    """Advanced completion features"""
    
    @staticmethod
    def complete_git_commands(text: str) -> List[str]:
        """Complete git subcommands"""
        git_commands = [
            'add', 'branch', 'checkout', 'clone', 'commit', 'diff',
            'fetch', 'init', 'log', 'merge', 'pull', 'push', 'rebase',
            'reset', 'status', 'tag'
        ]
        return [cmd for cmd in git_commands if cmd.startswith(text)]
        
    @staticmethod
    def complete_file_extensions(text: str, extensions: List[str]) -> List[str]:
        """Complete files with specific extensions"""
        import glob
        results = []
        for ext in extensions:
            pattern = f"{text}*.{ext}"
            results.extend(glob.glob(pattern))
        return results
        
    @staticmethod
    def smart_completion(text: str, context: str) -> List[str]:
        """Context-aware completion"""
        if context.startswith('cd '):
            import glob
            dirs = glob.glob(text + '*/')
            return [d.rstrip('/') for d in dirs]
        elif context.startswith('git '):
            return ZshLikeCompletion.complete_git_commands(text)
        else:
            import glob
            return glob.glob(text + '*')