#!/usr/bin/env python3
"""
A custom shell implementation with basic features
"""

import os
import sys
import subprocess
import readline
import glob
import shlex
from pathlib import Path
from typing import List, Dict, Optional


class CustomShell:
    def __init__(self):
        self.history_file = os.path.expanduser("~/.custom_shell_history")
        self.aliases = {
            'll': 'ls -la',
            'la': 'ls -la',
            'l': 'ls -l',
            '..': 'cd ..',
            '...': 'cd ../..'
        }
        self.env_vars = dict(os.environ)
        self.current_dir = os.getcwd()

        self.setup_readline()
        self.load_history()

    def setup_readline(self):
        """Setup readline for command history and completion"""
        readline.set_completer(self.complete)
        readline.parse_and_bind("tab: complete")
        readline.parse_and_bind("set editing-mode emacs")

    def complete(self, text: str, state: int) -> Optional[str]:
        """Tab completion for commands and files"""
        if state == 0:
            line = readline.get_line_buffer()
            if line.strip() == text:
                # Complete command names
                commands = []
                for path in self.env_vars.get('PATH', '').split(':'):
                    if os.path.isdir(path):
                        try:
                            for cmd in os.listdir(path):
                                if cmd.startswith(text) and os.access(os.path.join(path, cmd), os.X_OK):
                                    commands.append(cmd)
                        except PermissionError:
                            continue

                # Add built-in commands
                builtins = ['cd', 'pwd', 'exit', 'history', 'alias']
                commands.extend([cmd for cmd in builtins if cmd.startswith(text)])

                self.matches = sorted(set(commands))
            else:
                # Complete file names
                self.matches = glob.glob(text + '*')

        try:
            return self.matches[state]
        except IndexError:
            return None

    def load_history(self):
        """Load command history from file"""
        try:
            readline.read_history_file(self.history_file)
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass

    def save_history(self):
        """Save command history to file"""
        try:
            readline.write_history_file(self.history_file)
        except:
            pass

    def get_prompt(self) -> str:
        """Generate shell prompt"""
        user = self.env_vars.get('USER', 'user')
        hostname = self.env_vars.get('HOSTNAME', 'localhost')
        cwd = os.path.basename(self.current_dir) or '/'
        return f"{user}@{hostname}:{cwd}$ "

    def expand_variables(self, command: str) -> str:
        """Expand environment variables in command"""
        # Update env_vars with current environment
        self.env_vars.update(os.environ)
        for var, value in self.env_vars.items():
            command = command.replace(f'${var}', value)
            command = command.replace(f'${{{var}}}', value)
        return command

    def expand_aliases(self, command: str) -> str:
        """Expand aliases in command"""
        parts = command.split()
        if parts and parts[0] in self.aliases:
            parts[0] = self.aliases[parts[0]]
            return ' '.join(parts)
        return command

    def parse_command(self, command: str) -> List[List[str]]:
        """Parse command into pipeline segments"""
        command = self.expand_variables(command)
        command = self.expand_aliases(command)

        # Handle pipes
        segments = command.split('|')
        parsed_segments = []

        for segment in segments:
            try:
                args = shlex.split(segment.strip())
                # Expand globs
                expanded_args = []
                for arg in args:
                    if any(char in arg for char in ['*', '?', '[']):
                        matches = glob.glob(arg)
                        expanded_args.extend(matches if matches else [arg])
                    else:
                        expanded_args.append(arg)
                parsed_segments.append(expanded_args)
            except ValueError:
                parsed_segments.append(segment.strip().split())

        return parsed_segments

    def execute_builtin(self, args: List[str]) -> bool:
        """Execute built-in commands"""
        if not args:
            return False

        cmd = args[0]

        if cmd == 'cd':
            self.builtin_cd(args[1:])
        elif cmd == 'pwd':
            self.builtin_pwd()
        elif cmd == 'exit':
            self.builtin_exit(args[1:])
        elif cmd == 'history':
            self.builtin_history()
        elif cmd == 'alias':
            self.builtin_alias(args[1:])
        elif cmd == 'export':
            self.builtin_export(args[1:])
        else:
            return False

        return True

    def builtin_cd(self, args: List[str]):
        """Change directory"""
        if not args:
            target = self.env_vars.get('HOME', '/')
        else:
            target = args[0]

        target = os.path.expanduser(target)

        try:
            old_pwd = self.current_dir
            os.chdir(target)
            self.current_dir = os.getcwd()
            self.env_vars['PWD'] = self.current_dir
            self.env_vars['OLDPWD'] = old_pwd
        except OSError as e:
            print(f"cd: {e}")

    def builtin_pwd(self):
        """Print working directory"""
        print(self.current_dir)

    def builtin_exit(self, args: List[str]):
        """Exit shell"""
        exit_code = 0
        if args:
            try:
                exit_code = int(args[0])
            except ValueError:
                print("exit: numeric argument required")
                exit_code = 2

        self.save_history()
        sys.exit(exit_code)

    def builtin_history(self):
        """Show command history"""
        for i in range(1, readline.get_current_history_length() + 1):
            line = readline.get_history_item(i)
            if line:
                print(f"{i:5d}  {line}")

    def builtin_alias(self, args: List[str]):
        """Manage aliases"""
        if not args:
            for alias, command in self.aliases.items():
                print(f"alias {alias}='{command}'")
        else:
            for arg in args:
                if '=' in arg:
                    alias, command = arg.split('=', 1)
                    self.aliases[alias] = command.strip('\'"')
                else:
                    if arg in self.aliases:
                        print(f"alias {arg}='{self.aliases[arg]}'")
                    else:
                        print(f"alias: {arg}: not found")

    def builtin_export(self, args: List[str]):
        """Export environment variables"""
        for arg in args:
            if '=' in arg:
                var, value = arg.split('=', 1)
                self.env_vars[var] = value
                os.environ[var] = value
            else:
                if arg in self.env_vars:
                    print(f"export {arg}='{self.env_vars[arg]}'")

    def execute_pipeline(self, segments: List[List[str]]):
        """Execute command pipeline"""
        if not segments:
            return

        if len(segments) == 1:
            if self.execute_builtin(segments[0]):
                return
            self.execute_external(segments[0])
        else:
            self.execute_pipe_chain(segments)

    def execute_external(self, args: List[str]):
        """Execute external command"""
        if not args:
            return

        try:
            result = subprocess.run(
                args,
                cwd=self.current_dir,
                env=self.env_vars
            )
        except FileNotFoundError:
            print(f"{args[0]}: command not found")
        except KeyboardInterrupt:
            print("^C")

    def execute_pipe_chain(self, segments: List[List[str]]):
        """Execute pipeline of commands"""
        processes = []

        try:
            for i, args in enumerate(segments):
                if not args:
                    continue

                stdin_pipe = processes[-1].stdout if processes else None
                stdout_pipe = subprocess.PIPE if i < len(segments) - 1 else None

                proc = subprocess.Popen(
                    args,
                    stdin=stdin_pipe,
                    stdout=stdout_pipe,
                    stderr=subprocess.PIPE,
                    cwd=self.current_dir,
                    env=self.env_vars
                )
                processes.append(proc)

                if stdin_pipe:
                    stdin_pipe.close()

            # Wait for all processes
            for proc in processes:
                proc.wait()

        except FileNotFoundError as e:
            print(f"command not found: {e}")
        except KeyboardInterrupt:
            for proc in processes:
                proc.terminate()
            print("^C")

    def run(self):
        """Main shell loop"""
        print("Custom Shell v1.0")
        print("Type 'exit' to quit")

        while True:
            try:
                command = input(self.get_prompt()).strip()

                if not command:
                    continue

                segments = self.parse_command(command)
                self.execute_pipeline(segments)

            except EOFError:
                print("\nGoodbye!")
                self.save_history()
                break
            except KeyboardInterrupt:
                print("\n^C")
                continue


if __name__ == "__main__":
    shell = CustomShell()
    shell.run()
