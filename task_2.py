class Version:
    def __init__(self, version):
        self.version = version
         
    def reform(self, ver):
        #метод преобразовывает строку в лист, разбитый по точкам и с видоизмененными значениями
        #все случаи, где используются пререлизные версии, для простоты сравнения, заменяются на символы,
        #имеющие меньшее значение по таблице юникода, чем цифры
        #а там где указан дефис, заменяется на точку
        pre = ("pre-alfa", "alpha", "beta", "rc", "a", "b", "c", "d", "f", "-")
        for i, item in enumerate(pre):
            #в ascii точка - 46ой элемент, чтобы последний элемент pre (-) попал на точку, используется формула ниже
            ver = ver.replace(item, chr(i + 47 - len(pre)))
        return ver.split(".")
    
    def equalize(self, a, b):
        #метод приводит сравниваемые листы версий к одному виду, дополняя нулями меньший
        if len(a) > len(b):
            for i in range(len(a) - len(b)):
                b.append("0")
        elif len(a) < len(b):
            for i in range(len(b) - len(a)):
                a.append("0")
        return a, b
        
    def __eq__(self, other):
        if isinstance(other, Version):
            return self.version == other.version
        else:
            return False
    
    def __ne__(self, other):
        if isinstance(other, Version):
            return not self == other
        else:
            return True
    
    def __lt__(self, other):
        if isinstance(other, Version):
            a, b = self.equalize(self.reform(self.version), self.reform(other.version))
            if len(a) < len(b):
                return True
            elif len(a) > len(b):
                return False
            else:
                for i in range(len(a)):
                    if a[i] > b[i]:
                        return False
                    elif a[i] < b[i]:
                        return True     
        else:
            raise TypeError("Only Version objects are allowed") 
    
    def __le__(self, other):
        if isinstance(other, Version):
            return self == other or self < other
        else:
            raise TypeError("Only Version objects are allowed") 
    
    def __gt__(self, other):
        if isinstance(other, Version):
            return not self <= other
        else:
            raise TypeError("Only Version objects are allowed")  
    
    def __ge__(self, other):
        if isinstance(other, Version):
            return not self < other
        else:
            raise TypeError("Only Version objects are allowed") 

def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
