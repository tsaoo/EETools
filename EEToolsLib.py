import math

class EETools:
    def Notation(value):
        if value == 0:
            return "0"
        if value == math.inf:
            return "∞"
        prefixes = {
            -24: "y",  # yocto
            -21: "z",  # zepto
            -18: "a",  # atto
            -15: "f",  # femto
            -12: "p",  # pico
            -9: "n",  # nano
            -6: "u",  # micro
            -3: "m",  # milli
            0: "",   # no prefix
            3: "K",  # kilo
            6: "M",  # mega
            9: "G",  # giga
            12: "T",  # tera
            15: "P",  # peta
            18: "E",  # exa
            21: "Z",  # zetta
            24: "Y"   # yotta
        }

        exponent = math.floor(math.log10(abs(value)) / 3) * 3  
        baseValue = value / (10 ** exponent) 

        formattedValue = "{:.2f}".format(baseValue).rstrip("0").rstrip(".")

        prefix = prefixes.get(exponent, f"e{exponent}") 

        return f"{formattedValue}{prefix}"