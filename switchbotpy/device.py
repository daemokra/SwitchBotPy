from abc import ABCMeta, abstractmethod

class Device(metaclass=ABCMeta):
    def __init__(self, id, name, type, hub_id):
        self._id     = id
        self._name   = name
        self._type   = type
        self._hub_id = hub_id

    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def type(self):
        return self._type
    @property
    def hub_id(self):
        return self._hub_id

    @abstractmethod
    def turn_on(self) -> None:
        raise NotImplementedError()
    def turn_off(self) -> None:
        raise NotImplementedError()

class AirConditioner(Device):
    _ac_mode   = {'auto': 1, 'cool': 2, 'dry'   : 3, 'fan' : 4,'heat':5}
    _fan_speed = {'auto': 1, 'low' : 2, 'medium': 3, 'high': 4 }
    def __init__(self, client, id, name, type, hub_id):
        super().__init__(id, name, type, hub_id)
        self._temperature   = 25
        self._mode          = 'auto'
        self._speed         = 'auto'
        self._power_state   = 'off'
        self.set_params()
        self._client = client

    @property
    def temperature(self):
        return self._temperature
    @temperature.setter
    def temperature(self, val):
        """16～30℃の間で設定可能"""
    # TODO: 運転モードが'auto'のときは、相対的な温度になる。Validationのやり方考える。
#        if val < 16:
#            val = 16
#        elif val > 30:
#            val = 30
        self._temperature = val
    @property
    def mode(self):
        return self._mode
    @mode.setter
    def mode(self, val):
        self._mode = val
    @property
    def speed(self):
        return self._speed
    @speed.setter
    def speed(self, val):
        self._speed = val
    @property
    def state(self):
        return self._power_state

    def get_num_of_mode(self):
        """運転モードを数値で返す"""
        return self._ac_mode[self.mode]

    def get_num_of_speed(self):
        """風量を数値で返す"""
        return self._fan_speed[self.speed]

    def set_params(self):
        self._params = {
            "command": "setAll",
            "parameter": f"{self.temperature},{self._ac_mode[self.mode]},{self._fan_speed[self.speed]},{self.state}",
            "commandType": "command"
        }

    def turn_on(self,temp=None, mode=None, speed=None):
        self._power_state = 'on'
        if temp != None:
            self.temperature = temp
        if mode != None:
            self.mode = mode
        if speed != None:
            self.speed = speed
        self.set_params()
        print(self._params)
        return self._client.post_commands(self.id, self._params)

    def turn_off(self):
        self._power_state = 'off'
        self.set_params()
        self._client.post_commands(self.id, self._params)

    def get_status(self):
        return self._client.get_status(self.id)



class HubMini(Device):
    def __init__(self, client, id, name, type, hub_id):
        super().__init__(id, name, type, hub_id)
        self._client = client
    def turn_on(self):
        pass
    def turn_off(self):
        pass
    def get_status(self):
        return self._client.get_status(self.id)