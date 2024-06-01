import random


class Colours:
    def chart_colour_picker(self):
        hex_colours = ["#28ff00", "#fa0000", "#00defa", "#3700fa", "#fa9a00", "#03fa00", "#514b76", "#defa00",
                       "#2200fa",
                       "#fa4c00", "#be00fa", "#fa0051", "#00b4fa", "#c400fa", "#5c5b45", "#4b764f", "#4b7276",
                       "#764b6a",
                       "#843232", "#516000"]
        return random.choice(hex_colours)


# def calculate_total(data:dict):
#     for key, val in data.items()
#         for v in val:
#             v.