import pygame


allKeys = '''1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./ '''


class Keyboard:
    def __init__(self):
        self._keys = {}
        self._toggleKeys = {}

    def give_event(self, event):
        if event.type == pygame.KEYDOWN:
            self._keys[chr(event.key)] = True
            self._toggleKeys[chr(event.key)] = True

        if event.type == pygame.KEYUP:
            self._keys[chr(event.key)] = False

    def get_key(self, key):
        return self._keys.get(key, False)

    def reset_toggle(self):
        self._toggleKeys = {}

    def get_toggle(self, item):
        return self._toggleKeys.get(item, False)

    def __getitem__(self, item):
        return self._keys.get(item, False)


class KeyMap:
    def __init__(self, map):
        self._map = map

    def get_key(self, key):
        return kbrd[self._map[key]]

    def assign_key(self, from_key, to_key):
        self._map[from_key] = to_key

    def get_toggle(self, key):
        return kbrd.get_toggle(self._map[key])

    def __getitem__(self, item):
        return kbrd[item]


def default_keymap():
    ret_map = {}
    for letter in allKeys:
        ret_map[letter] = letter

    return KeyMap(ret_map)


kbrd = Keyboard()

