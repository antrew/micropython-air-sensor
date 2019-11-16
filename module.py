class Module:
    def readValue(self):
        return {}

    def getDisplayLines(self, moduleData):
        return []

    def test(self):
        data = self.readValue()
        for line in self.getDisplayLines(data):
            print(line)
