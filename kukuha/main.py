import cmd
import logging

import git

from kukuha.kukuha_app import KukuhaApp

REPO = git.Repo(search_parent_directories=True)
GIT_SHA = REPO.head.object.hexsha[:8]

logger = logging.getLogger(__name__)

app = KukuhaApp(git_version=GIT_SHA)


class KukuhaShell(cmd.Cmd):
    """
    @see https://docs.python.org/3/library/cmd.html
    """
    intro = f'Welcome to the Kukuha shell. Type help or ? to list commands. (Git sha {GIT_SHA})\n'
    prompt = 'Request: '

    def default(self, arg):
        """Input request: REQUEST"""
        print(app.handle_request(arg))

    def do_exit(self, arg):
        """Stop recording, close the Kukuha window, and exit: EXIT"""
        print('Thank you for using Kukuha')
        app.exit()
        return True


if __name__ == '__main__':
    KukuhaShell().cmdloop()
