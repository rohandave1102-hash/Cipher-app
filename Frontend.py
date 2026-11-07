import ctypes
import os
import sys
import time
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

Window.clearcolor = (0.01, 0.02, 0.01, 1)

# Inbuilt application password
INBUILT_PASSWORD = "30feb"

# ---------------------------------------------------------
# DIRECT C-BACKEND BINDING VIA CTYPES
# ---------------------------------------------------------
lib_name = "crypting1.dll" if sys.platform == "win32" else "libcrypting.so"
base_dir = os.path.dirname(os.path.abspath(__file__))

candidate_paths = [
    os.path.join(base_dir, lib_name),
    os.path.join(base_dir, "lib", lib_name),
    lib_name
]

c_lib = None
load_err_msg = ""

for p in candidate_paths:
    if os.path.exists(p):
        try:
            c_lib = ctypes.CDLL(p)
            break
        except Exception as err:
            load_err_msg = str(err)

if c_lib is None:
    try:
        c_lib = ctypes.CDLL(lib_name)
    except Exception as err:
        load_err_msg = str(err)

if c_lib is not None:
    try:
        c_lib.Converterletters.argtypes = [ctypes.c_char]
        c_lib.Converterletters.restype = ctypes.c_char_p

        c_lib.Deconverterletters.argtypes = [ctypes.c_char_p]
        c_lib.Deconverterletters.restype = ctypes.c_char_p

        if hasattr(c_lib, 'srand'):
            c_lib.srand.argtypes = [ctypes.c_uint]
            c_lib.srand.restype = None
            c_lib.srand(int(time.time()))
    except Exception as ae:
        c_lib = None
        load_err_msg = f"Symbol error: {ae}"


def c_encrypt(data: str) -> str:
    if not c_lib:
        return f"[Backend Error: {load_err_msg}]"
    result = []
    for ch in data:
        byte_char = ch.encode('latin-1', errors='ignore')
        if not byte_char:
            continue
        c_res = c_lib.Converterletters(byte_char)
        if c_res:
            result.append(c_res.decode('latin-1'))
        else:
            result.append(ch)
    return "".join(result)


def c_decrypt(data: str) -> str:
    if not c_lib:
        return f"[Backend Error: {load_err_msg}]"
    result = []
    i = 0
    size = len(data)
    while i < size:
        matched_len = 0
        decoded_char = None
        for length in (3, 2, 1):
            if i + length <= size:
                substr = data[i:i + length].encode('latin-1')
                res = c_lib.Deconverterletters(substr)
                if res:
                    matched_len = length
                    decoded_char = res.decode('latin-1')[0]
                    break
        if matched_len > 0 and decoded_char is not None:
            result.append(decoded_char)
            i += matched_len
        else:
            result.append(data[i])
            i += 1
    return "".join(result)


# ---------------------------------------------------------
# KIVY PHONE INTERFACE
# ---------------------------------------------------------
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # 90s blank white screen
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=15, size_hint=(0.85, None), height=200)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.pass_input = TextInput(
            password=True, multiline=False, halign='center',
            font_size='18sp', size_hint=(1, None), height=48,
            background_color=(0.95, 0.95, 0.95, 1), foreground_color=(0, 0, 0, 1)
        )
        self.pass_input.bind(on_text_validate=self.check_pwd)

        btn_go = Button(
            text="GO", font_size='16sp', bold=True,
            size_hint=(0.45, None), height=44, pos_hint={'center_x': 0.5},
            background_color=(0.8, 0.8, 0.8, 1), color=(0, 0, 0, 1)
        )
        btn_go.bind(on_release=self.check_pwd)

        layout.add_widget(self.pass_input)
        layout.add_widget(btn_go)
        self.add_widget(layout)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def check_pwd(self, *args):
        if self.pass_input.text == INBUILT_PASSWORD:
            self.manager.current = 'dashboard'
        else:
            self.pass_input.text = ""


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.01, 0.03, 0.02, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=8)

        lbl_title = Label(
            text="[b]◆ ENCRYPTION WORKSTATION ◆[/b]", markup=True,
            font_size='18sp', color=(0.22, 1.0, 0.08, 1),
            size_hint=(1, None), height=36
        )

        lbl_in = Label(text="INPUT STRING / PLAINTEXT", font_size='11sp', color=(0.65, 0.87, 0.71, 1), size_hint=(1, None), height=20)
        self.txt_in = TextInput(
            multiline=True, font_size='14sp', size_hint=(1, 0.28),
            background_color=(0.02, 0.09, 0.05, 1), foreground_color=(0.9, 1.0, 0.92, 1)
        )

        btn_row = BoxLayout(size_hint=(1, None), height=42, spacing=15)
        btn_enc = Button(text="→ ENCRYPT", bold=True, background_color=(0.07, 0.27, 0.17, 1), color=(0.84, 1.0, 0.88, 1))
        btn_dec = Button(text="← DECRYPT", bold=True, background_color=(0.07, 0.27, 0.17, 1), color=(0.84, 1.0, 0.88, 1))
        btn_enc.bind(on_release=self.do_encrypt)
        btn_dec.bind(on_release=self.do_decrypt)
        btn_row.add_widget(btn_enc)
        btn_row.add_widget(btn_dec)

        lbl_out = Label(text="OUTPUT RESULT", font_size='11sp', color=(0.65, 0.87, 0.71, 1), size_hint=(1, None), height=20)
        self.txt_out = TextInput(
            multiline=True, readonly=True, font_size='14sp', size_hint=(1, 0.28),
            background_color=(0.02, 0.09, 0.05, 1), foreground_color=(0.9, 1.0, 0.92, 1)
        )

        # Action row with Copy Output and Clear buttons
        action_row = BoxLayout(size_hint=(1, None), height=40, spacing=15)
        
        self.btn_copy = Button(
            text="COPY OUTPUT", bold=True,
            background_color=(0.07, 0.27, 0.17, 1), color=(0.84, 1.0, 0.88, 1)
        )
        self.btn_copy.bind(on_release=self.copy_output)

        btn_clr = Button(
            text="CLEAR ALL", bold=True,
            background_color=(0.07, 0.27, 0.17, 1), color=(0.84, 1.0, 0.88, 1)
        )
        btn_clr.bind(on_release=self.clear_all)

        action_row.add_widget(self.btn_copy)
        action_row.add_widget(btn_clr)

        layout.add_widget(lbl_title)
        layout.add_widget(lbl_in)
        layout.add_widget(self.txt_in)
        layout.add_widget(btn_row)
        layout.add_widget(lbl_out)
        layout.add_widget(self.txt_out)
        layout.add_widget(action_row)

        self.add_widget(layout)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def do_encrypt(self, *args):
        self.txt_out.text = c_encrypt(self.txt_in.text)
        self.btn_copy.text = "COPY OUTPUT"

    def do_decrypt(self, *args):
        self.txt_out.text = c_decrypt(self.txt_in.text)
        self.btn_copy.text = "COPY OUTPUT"

    def copy_output(self, *args):
        if self.txt_out.text:
            Clipboard.copy(self.txt_out.text)
            self.btn_copy.text = "COPIED! ✓"

    def clear_all(self, *args):
        self.txt_in.text = ""
        self.txt_out.text = ""
        self.btn_copy.text = "COPY OUTPUT"


class CipherMatrixApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm


if __name__ == '__main__':
    CipherMatrixApp().run()
