import cmd
import logging

from kukuha.kukuha_app import KukuhaApp

logger = logging.getLogger(__name__)

app = KukuhaApp()


class KukuhaShell(cmd.Cmd):
    """
    @see https://docs.python.org/3/library/cmd.html
    """
    intro = 'Welcome to the Kukuha shell. Type help or ? to list commands.\n'
    prompt = 'Request: '

    def default(self, arg):
        """Input request: text"""
        print(app.handle_request(arg))

    def do_exit(self, arg):
        """Stop recording, close the Kukuha window, and exit: EXIT"""
        print('Thank you for using Kukuha')
        app.exit()
        return True


if __name__ == '__main__':
    KukuhaShell().cmdloop()
