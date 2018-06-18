import strings
import SaveStuff


class SetupScreenListener:
    def __init__(self, room_num_tbox, stacked_widget):
        self.room_num_tbox = room_num_tbox
        self.stacked_widget = stacked_widget

    def save_press(self):
        data = {'room': str(self.room_num_tbox.text())}
        SaveStuff.write(data, strings.f_config)
        self.stacked_widget.setCurrentIndex(0)
