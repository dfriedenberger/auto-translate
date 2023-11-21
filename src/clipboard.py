import win32clipboard
import time

class ClipBoardListener:

    def __init__(self):
        self.text = self._get_clip_board_text()

    def get_text(self):

        while True:
            new_text = self._get_clip_board_text()
            if new_text != self.text:
                self.text = new_text
                return new_text
            time.sleep(0.3)

    def _get_clip_board_text(self):
        # get clipboard data
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        return data