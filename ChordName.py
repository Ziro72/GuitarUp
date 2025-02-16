from Consts import KEY_WORDS


class ChordName:
    def __init__(self, name=''):
        self.name = name
        self.length = len(name)
        self.array = []
        self.refactor()

    def update(self, new_name):
        self.name = new_name
        self.length = len(new_name)
        self.refactor()

    def check_key(self, index, key):
        length = self.length - index
        if length <= len(key) or self.name[index:index + len(key)] != key:
            return 0
        res = len(key) + 1
        if length > res and self.name[index + res].isdigit():
            res += 1
        return res

    def word_push(self, first, second, state):
        if second - first != 0:
            self.array.append((self.name[first:second], state))

    def brackets_push(self, index):
        nex = index
        while nex != self.length and self.name[nex - 1] != ')':
            nex += 1
        self.word_push(index, nex, True)
        return nex

    def refactor(self):
        self.array.clear()
        index = 0
        prev = 0
        while index < self.length:
            if self.name[index] == '(':
                self.word_push(prev, index, False)
                index = self.brackets_push(index)
                prev = index
                continue
            for key in KEY_WORDS:
                word_length = self.check_key(index, key)
                if word_length == 0:
                    continue
                self.word_push(prev, index, False)
                prev = index
                index += word_length
                self.word_push(prev, index, True)
                prev = index
                break
            else:
                index += 1
        self.word_push(prev, index, False)

    def replace(self, a, b):
        self.name = self.name.replace(a, b)
        self.refactor()
