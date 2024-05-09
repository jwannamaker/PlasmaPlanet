import pyglet

import game.util as util


class LabelFactory:
    def __init__(self, font_size, first_row_height):
        self.next_row_height = first_row_height
        self.row_spacing = font_size + font_size // 4
        self.labels = {}
    
    def next_row(self) -> int:
        self.next_row_height += self.row_spacing
        return self.next_row_height
    
    def create_title(self, title: str):
        label_text = f'{title:=^50}'
        self.labels['title'] = pyglet.text.Label(text=label_text, bold=True)
        self.format(self.labels['title'])
        return 'title'

    def create_updatable(self, fixed_text: str, default_value: int):
        label_text = f'{fixed_text:<9} {default_value:>40}'
        self.labels[fixed_text.lower()] = pyglet.text.Label(text=label_text)
        self.format(self.labels[fixed_text.lower()])
        return fixed_text.lower()

    def format(self, label):
        label.anchor_x = 'left'
        label.anchor_y = 'top'
        label.font_name = 'monogram'
        label.font_size = self.font_size
        label.batch = util.text_batch
        label.group = util.background

    def get_label(self, fixed_text) -> pyglet.text.Label:
        return self.labels[fixed_text]

    def set_xy(self, label_name, x, y):
        self.labels[label_name].x = x
        self.labels[label_name].y = y

    def update(self, dt, label_name):
        label_text = self.labels[label_name].text
        split_index = label_text.find(' ')
        fixed_text = label_text[:split_index].strip()
        value = int(label_text[split_index:].strip()) + 1
        self.labels[label_name].text = f'{fixed_text:<9} {value:>40}'
        
