import subprocess


class IpmiTool:

    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password

    def run_cmd(self, cmd: str) -> str:
        basecmd = f'ipmitool -H {self.host} -I lanplus -U {self.username} -P {self.password}'
        command = f'{basecmd} {cmd}'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(
                f'execute command {cmd} failed:{result.stderr}'
            )

        return result.stdout

    def mc_info(self) -> str:
        """
        execute ipmitool command mc info
        :return:
        """
        return self.run_cmd(cmd='mc info')

    def sensor(self) -> str:
        """
        execute ipmitool command sensor
        :return:
        """
        return self.run_cmd(cmd='sensor')

    def temperature(self) -> list:
        """
        get current temperature
        :return:
        """
        data = self.sensor()
        temperatures = []

        for line in data.splitlines():
            if 'Temp' in line:
                temperatures.append(float(line.split('|')[1].strip()))

        return temperatures

    def switch_fan_mode(self, auto: bool):
        """
        switch the fan mode
        :param auto:
        :return:
        """
        manual_cmd = 'raw 0x30 0x30 0x01 0x00'
        auto_cmd = 'raw 0x30 0x30 0x01 0x01'
        return self.run_cmd(cmd=auto_cmd) if auto else self.run_cmd(cmd=manual_cmd)

    def set_fan_speed(self, speed: int):
        """
        set fan speed
        :param speed:
        :return:
        """
        if speed < 10 or speed > 100:
            raise ValueError(
                'speed must be between 10 and 100'
            )

        self.switch_fan_mode(auto=False)
        base_cmd = 'raw 0x30 0x30 0x02 0xff'
        return self.run_cmd(cmd=f'{base_cmd} {hex(speed)}')
