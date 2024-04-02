
class emodic:
    with open("assets/positive_dict.txt",encoding="big5",mode="r") as file:
        positive = []
        for line in file:
            positive.append(line.strip())


    with open("assets/negative_dict.txt",encoding="big5",mode="r") as file:
        negative = []
        for line in file:
            negative.append(line.strip())
    
    def PositiveDict(self):
        return self.positive
    
    def NegativeDict(self):
        return self.negative
