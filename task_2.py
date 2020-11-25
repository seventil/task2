from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, version):
        self.version = version
         
    def reform(self, tokens):
    # Метод разбивает строку по точкам в лист, преобразуя элементы
    # все случаи, где используются пререлизные версии, заменяются на символы,
    # имеющие меньшее значение по таблице юникода, чем цифры
    # там где указан дефис, заменяется на точку
        # В ascii точка - 46ой элемент, чтобы "-" попал на точку, нужен оффсет  
        CHAR_OFFSET = 47       
        PRE_ZERO_TOKENS = ("pre-alfa", "alpha", "beta", "rc", "a", "b", "c", "d", "f", "-")
        for index, item in enumerate(PRE_ZERO_TOKENS):            
            tokens = tokens.replace(item, chr(index + CHAR_OFFSET - len(PRE_ZERO_TOKENS)))
        return tokens.split(".")
    
    def equalize(self, a, b):
        # метод приводит сравниваемые листы версий к одному виду, дополняя нулями меньший
        if len(a) > len(b):
            for _ in range(len(a) - len(b)):
                b.append("0")
        elif len(a) < len(b):
            for _ in range(len(b) - len(a)):
                a.append("0")
        return a, b
        
    def __eq__(self, other):
        if isinstance(other, Version):
            return self.version == other.version
        else:
            return False        

    def __lt__(self, other):
        if isinstance(other, Version):
            # ver_1 и ver_2 - дополненые по необходости нулевыми токенами (методом equalize),
            # разбитые по точкам на листы с преобразованными токенами (методом reform)             
            ver_1, ver_2 = self.equalize(self.reform(self.version), self.reform(other.version))
            for ver_1_token, ver_2_token in zip(ver_1, ver_2):
                # если токен длиннее, то он больше
                # если токены равны по длине и не равны по значению
                # возвращает результат прямого сравнения двух токенов           
                if len(ver_1_token) != len(ver_2_token):                    
                    return len(ver_1_token) < len(ver_2_token)                
                elif ver_1_token != ver_2_token:                    
                    return ver_1_token < ver_2_token
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
