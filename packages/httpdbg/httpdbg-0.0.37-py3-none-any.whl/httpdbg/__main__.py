# -*- coding: utf-8 -*-
try:
    import readline  # noqa: F401 enable the 'up arrow' history in the console
except ImportError:
    pass  # readline is not available on Windows
import pkg_resources
import sys
import time

from httpdbg.args import read_args
from httpdbg.server import httpdbg
from httpdbg.mode_console import run_console
from httpdbg.mode_pytest import run_pytest
from httpdbg.mode_script import run_script
from httpdbg.webapp import httpdebugk7


def print_msg(msg):
    sep = ".... - - .--. -.. -... --. .... - - .--. -.. -... --. .... - - .--. -.. -... --."
    msg = f"{sep}\n{msg}\n{sep}"
    print(msg)


def pyhttpdbg(params, subparams, test_mode=False):

    url = f"http://localhost:{params.port}/{'?hi=on' if params.console else ''}"

    print_msg(f"  httpdbg - HTTP(S) requests available at {url}")

    with httpdbg(params.port):

        if params.pytest:
            run_pytest(subparams)
        elif params.script:
            run_script(subparams)
        else:
            run_console(test_mode)

        if not (params.force_quit or test_mode):

            print_msg(f"  httpdbg - HTTP(S) requests available at {url}")

            if params.keep_up:
                input("Press enter to quit")
            else:
                # we keep the server up until all the requests have been loaded in the web interface
                while httpdebugk7.unread:
                    time.sleep(0.5)


def pyhttpdbg_entry_point(test_mode=False):
    params, subparams = read_args(sys.argv[1:])
    if params.version:
        print(pkg_resources.get_distribution("httpdbg").version)
    else:
        pyhttpdbg(params, subparams, test_mode=test_mode)


if __name__ == "__main__":
    pyhttpdbg_entry_point()
