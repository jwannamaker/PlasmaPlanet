import pyglet

Hud = pyglet.graphics.Batch()

class LabelFactory:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.labels = {}
        
    def create_title(self, title: str):
        label_text = f'{title:=^50}'
        self.labels['title'] = pyglet.text.Label(text=label_text, bold=True)
        self.format(self.labels['title'])
        return 'title'
        
    def create_updatable(self, fixed_text: str, default_value: int):
        label_text = f'{fixed_text:<9}-{default_value:>40}'
        self.labels[fixed_text.lower()] = pyglet.text.Label(text=label_text)
        self.format(self.labels[fixed_text.lower()])
        return fixed_text.lower()
    
    def format(self, label):
        label.anchor_x = 'left'
        label.anchor_y = 'top'
        label.font_name = 'monogram'
        label.font_size = 36
        label.batch = Hud
        
    def get_label(self, fixed_text) -> pyglet.text.Label:
        return self.labels[fixed_text]
    
    def set_xy(self, label_name, x, y):
        self.labels[label_name].x = x
        self.labels[label_name].y = y
    
    def update(self, label_name, new_value):
        fixed_text = self.labels[label_name].text[:self.labels[label_name].text.find('-')]
        self.labels[label_name].text = f'{fixed_text}{new_value:>40}'