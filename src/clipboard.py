import time
import logging
import win32clipboard


formats = {val: name for name, val in vars(win32clipboard).items() if name.startswith('CF_')}

def format_name(fmt):
    if fmt in formats:
        return formats[fmt]
    try:
        return win32clipboard.GetClipboardFormatName(fmt)
    except:
        return "unknown"



class ClipBoardListener:

    def __init__(self):
        self.text = self.get_clip_board_text()

    def get_text(self):

        while True:
            new_text = self.get_clip_board_text()
            if new_text != self.text:
                self.text = new_text
                return new_text
            time.sleep(0.3)


    def print_available_formats(self):
        win32clipboard.OpenClipboard()

        fmt = 0
        while True:
            fmt = win32clipboard.EnumClipboardFormats(fmt)
            if fmt == 0: break
            logging.info(f'{fmt:5} ({format_name(fmt)})')

        win32clipboard.CloseClipboard()

    def get_clip_board_text(self):
        # get clipboard data
        data = None
        win32clipboard.OpenClipboard()


        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)

        win32clipboard.CloseClipboard()
        return data
