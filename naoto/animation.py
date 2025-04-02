
class Animation:

    def __init__(self, images):
        self.images = images
        self.speed = .1
        self.current_frame = self.images[0]
        self.current_index = 0
        self.current_time = 0
        self.last_updated_time = 0

    def update(self, dt):
        self.current_time += dt

        if self.current_time > self.last_updated_time + self.speed:
            self.current_index += 1
            self.last_updated_time = self.current_time

    def reset(self):
        self.current_index = 0

    def is_finished(self):

        if self.current_index >= len(self.images) - 1:
            return True

        return False

    def get_frame(self):
        return self.images[self.current_index % len(self.images)]