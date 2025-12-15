class WhatHaveIDone(Exception):
    """
    Litwo! Ojczyzno moja! ty jesteś jak zdrowie.
    Ile cię trzeba cenić, ten tylko się dowie,
    Kto cię stracił. Dziś piękność twą w całej ozdobie
    Widzę i opisuję, bo tęsknię po tobie.


    Panno Święta, co Jasnej bronisz Częstochowy
    I w Ostrej świecisz Bramie! Ty, co gród zamkowy
    Nowogródzki ochraniasz z jego wiernym ludem!
    Jak mnie dziecko do zdrowia powróciłaś cudem
    (Gdy od płaczącej matki pod Twoję opiekę
    Ofiarowany, martwą podniosłem powiekę
    I zaraz mogłem pieszo do Twych świątyń progu
    Iść za wrócone życie podziękować Bogu),
    Tak nas powrócisz cudem na Ojczyzny łono.
    Tymczasem przenoś moję duszę utęsknioną
    Do tych pagórków leśnych, do tych łąk zielonych,
    Szeroko nad błękitnym Niemnem rozciągnionych;
    Do tych pól malowanych zbożem rozmaitem,
    Wyzłacanych pszenicą, posrebrzanych żytem;
    Gdzie bursztynowy świerzop, gryka jak śnieg biała,
    Gdzie panieńskim rumieńcem dzięcielina pała,
    A wszystko przepasane, jakby wstęgą, miedzą
    Zieloną, na niej z rzadka ciche grusze siedzą.
    """

    def __init__(self, message="Ohayo informatyk-kun ≧◡≦. I really want to be fixed UwU", errors=None):
        super().__init__(message)
        self.errors = errors


class ToMakeCodeWorkError(Exception):
    def __init__(self, message="Behold This Is NOT A Bug. It's A Feature", errors="Explode"):
        super().__init__(message)
        self.errors = errors


class Abortion(Exception):
    def __init__(self, message="This Cog shouldn't be loaded", errors="UwU"):
        super().__init__(message)
        self.errors = errors
