class romanNotation:
    rn = ['M','D','C','L','X','V','I']
    def __init__(self,v: str):
        self.v = v.upper()
        self.w = self.__splitV()
    def __splitV(self):
        res = []
        cw = False
        for i,l in enumerate(self.v):
            if i != len(self.v)-1: 
                if romanNotation.rn.index(l) >= romanNotation.rn.index(self.v[i+1]):
                    if cw:
                        res[-1] += l
                    else:
                        res.append(l)
                    cw = True
                else:
                    if cw:
                        res[-1] += l
                    else:
                        res.append(l)
                    cw = False
            else:
                if cw:
                        res[-1] += l
                else:
                    res.append(l)
        return res
    def __lt__(self, other):
        for i in range(len(self.w) if len(self.w) < len(other.w) else len(other.w)):
            if len(self.w[i]) > 1 or len(other.w[i])>1:
                if romanNotation.rn.index(self.w[i][-1]) < romanNotation.rn.index(self.w[i][-1]):
                    return False
                elif romanNotation.rn.index(self.w[i][-1]) > romanNotation.rn.index(self.w[i][-1]):
                    return True
                else:
                    if sum([romanNotation.rn.index(x) for x in self.w[i]]) > sum([romanNotation.rn.index(x) for x in other.w[i]]):
                        return True
                    elif sum([romanNotation.rn.index(x) for x in self.w[i]]) < sum([romanNotation.rn.index(x) for x in other.w[i]]):
                        return False
            else:
                if romanNotation.rn.index(self.w[i]) < romanNotation.rn.index(self.w[i]):
                    return False
                elif romanNotation.rn.index(self.w[i]) > romanNotation.rn.index(self.w[i]):
                    return True
                else:
                    return len(self.w) < len(other.w)
        return False
    def __gt__(self, other):
        return not self.__lt__(other) and not self.v == other.v

a1 = romanNotation('MM')
a2 = romanNotation('MDCCCCLXXXXVIIII')
print(a1.v,'>',a2.v,a1>a2,'\n'+a1.v,'<',a2.v, a1<a2)