import argparse
import os
import win32api
import webview

from src.server import WebServer


def parse_args():

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for translating pot files to po files')

    parser.add_argument("--input-language", required=True,
                        metavar="INPUT_LANGUAGE",
                        choices=['de', 'en', 'es'],
                        help="language of input file (de,en,es)")
    parser.add_argument("--output-language", required=True,
                        metavar="OUTPUT_LANGUAGE",
                        choices=['de', 'en', 'es'],
                        help="language of output file (de,en,es)")
    parser.add_argument("--debug-console", action='store_true',
                        help="show debug console")



    args = parser.parse_args()

    return args.input_language, args.output_language, args.debug_console


def signal_handler(_sig, _frame=None):
    print('You pressed Ctrl+C!')
    # window.destroy()
    os._exit(0)


def on_closed():
    print('window is closed')
    os._exit(0)


input_language, output_language, debug = parse_args()

server = WebServer("127.0.0.1", 8000, input_language, output_language)
server.start()


window = webview.create_window('Woah dude!', "http://localhost:8000/", width=1200, height=100, x=0, y=0, on_top=True)

win32api.SetConsoleCtrlHandler(signal_handler, True)

window.events.minimized += server.pause
window.events.restored += server.resume
window.events.closed += on_closed


webview.start(debug=debug)
