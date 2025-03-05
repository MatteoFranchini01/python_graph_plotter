class ModelData:
    def __init__(self):
        self.full_data_x = []

        self.full_data_y = []

    def add_data(self, x, y):
        self.full_data_x.append(x)

        self.full_data_y.append(y)

    def get_data(self):
        return self.full_data_x, self.full_data_y
