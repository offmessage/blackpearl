from blackpearl.projects import BaseProject


class DiscoLights:
    listening_for = ['slider',]
    hardware_required = ['slider', 'rainbow']
    def data(self, data):
        value = (data['slider']['value'])/1000.0
        hue = self.rainbow.hue(value)
        self.rainbow.set_all(hue)
        self.rainbow.update()


class Project(BaseProject):
    required_modules = [DiscoLights, ]
    

if __name__ == '__main__':
    SimpleSlider()