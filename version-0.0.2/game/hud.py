import pyglet


class LabelFactory:
    def __init__(self, window_width, window_height, batch, subgroup):
        self.window_width = window_width
        self.window_height = window_height
        self.batch = batch
        self.subgroup = subgroup
        self.labels = {}

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
        label.font_size = 36
        label.batch = self.batch
        label.group = self.subgroup

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
        
