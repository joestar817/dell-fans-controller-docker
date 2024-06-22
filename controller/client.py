from controller.logger import logger

from controller.ipmi import IpmiTool


class FanController:

    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password

        self.ipmi = IpmiTool(self.host, self.username, self.password)

    def set_fan_speed(self, speed: int):
        logger.info(f'Set fan speed: {speed}%')
        self.ipmi.set_fan_speed(speed)

    def run(self):
        temperature: int = max(self.ipmi.temperature())
        logger.info(f'Current maximum temperature: {temperature}')

        if 0 < temperature <= 50:
            self.set_fan_speed(10)
        elif 50 < temperature <= 55:
            self.set_fan_speed(20)
        elif 55 < temperature <= 60:
            self.set_fan_speed(30)
        elif 60 < temperature <= 65:
            self.set_fan_speed(40)
        else:
            logger.info(f'Switch fan control to auto mode')
            self.ipmi.switch_fan_mode(auto=True)
