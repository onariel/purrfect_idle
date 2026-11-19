import json

class Convert:

    @staticmethod
    def convert(number: float, power: int) -> str:
        data = json.load(open('convert/convert.json'))
        if str(power) in data:
            return str(round(number,3)) + " " + data[str(power)]
        else:
            return str(round(number,3)) + " *10**" + str(power)