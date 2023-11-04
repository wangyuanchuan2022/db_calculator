import kivy.lang
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
from functools import partial

from s import User


LabelBase.register(name='Roboto', fn_regular='./msyh.ttc')


class MainWindow(BoxLayout):
    def __init__(self):
        super().__init__(orientation='vertical', spacing=10)
        # kivy.lang.Builder.load_file('./db.kv')
        self.user = User()
        self.special_key_word = [str(i) for i in range(10)]
        self.special_key_word += ['的', '个', '生产器', '雷劈剑', '丢下个', '连', '合一', '反弹盾', ' ', '/']
        self.special_key_word += self.user.generator_num.keys()
        key_word = self.special_key_word.copy()
        key_word += self.user.special_attack.keys()
        key_word += self.user.basic_r_text2num.keys()
        key_word.append('吞')
        key_word += self.user.attack_text2num.keys()
        key_word += self.user.shield2num.keys()
        key_word += self.user.curse.keys()
        key_word += self.user.attack2shield.keys()
        key_word.append('Back')
        self.special_key_word.append('Back')
        # print(self.special_key_word)
        # print(key_word)
        width = 6
        self._btn_list = []
        for i in range(int(len(key_word)/width)+1):
            box = BoxLayout(orientation='horizontal', spacing=2)
            for j in range(width):
                try:
                    btn = Button(text=key_word[i * width + j])
                    btn.bind(on_press=partial(self.add_text))
                    # btn.set_disabled(True)
                    box.add_widget(btn)
                    self._btn_list.append(btn)
                except IndexError:
                    break
            self.ids['box_l'].add_widget(box)

        self.move = ''
        self.attack = ''
        self.set_disabled_btn()

    def add_text(self, btn):
        if btn.text == 'Back':
            self.ids['txt_input'].text = self.ids['txt_input'].text[:-1]
        else:
            self.ids['txt_input'].text += btn.text
        self.set_disabled_btn()

    def set_disabled_btn(self):
        if self.ids['txt_input'].hint_text == 'move:':
            for button in self._btn_list:
                if button.text not in self.special_key_word:
                    try:
                        move = self.ids['txt_input'].text + button.text
                        self.user.move_calculation(move, is_try=True)
                        button.set_disabled(False)
                    except Exception:
                        _move = move + '生产器'
                        try:
                            self.user.move_calculation(_move, is_try=True)
                            button.set_disabled(False)
                        except Exception:
                            _move = move + '合一'
                            try:
                                self.user.move_calculation(_move, is_try=True)
                                button.set_disabled(False)
                            except Exception:
                                button.set_disabled(True)

    def set_disabled_all(self, value):
        for btn in self._btn_list:
            btn.set_disabled(value)

    def send(self):
        # self.set_disabled_btn()
        if self.ids['txt_input'].hint_text == 'move:':
            self.move = str(self.ids['txt_input'].text)
            self.ids['label_2'].text = (self.ids['txt_input'].hint_text +
                                        self.ids['txt_input'].text + '\n')
            self.set_disabled_all(False)
        else:
            # self.set_disabled_all(False)
            self.attack = str(self.ids['txt_input'].text)
            self.ids['label_2'].text += (self.ids['txt_input'].hint_text +
                                         self.ids['txt_input'].text + '\n')
            try:
                self.ids['label_2'].text += self.user.step(self.move, self.attack)
            except Exception as e:
                self.ids['label_2'].text = str(e)
                self.user.restart()
            self.user.generator_move()
        self.ids['txt_input'].hint_text = 'move:' if self.ids['txt_input'].hint_text.startswith('attack') else 'attack:'
        self.ids['txt_input'].text = ''
        self.ids['label_1'].text = str(self.user)
        self.set_disabled_btn()

    def restart(self):
        self.ids['label_2'].text = ''
        self.user.restart()

    def show_shield(self):
        self.ids['label_2'].text = self.user.show_shield()

    def show_generator(self):
        g_set = set(self.user.generator_list)
        for g in g_set:
            self.ids['label_2'].text += f'{self.user.generator_list.count(g)}个{g}\n'


class DbApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    DbApp().run()
