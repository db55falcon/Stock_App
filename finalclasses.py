class Stock:
    def __init__(self, id_num, symbl, no_shrs, p_price, c_price, date):
        # simple check and warning to help keep ID numbers normalized
        self.id_num: int = id_num
        self.symbl: str = symbl
        self.no_shrs: float = no_shrs
        self.p_price: float = p_price
        self.date: str = date
    # I wrote this to see what was in the stock list after they get appended to an investor

    def __repr__(self):
        return f"ID:{self.id_num} Stock: {self.symbl}"


class Bond(Stock):
    def __init__(self, id_num, symbl, no_shrs, p_price, c_price, coupon, p_yield, date):
        super().__init__(id_num, symbl, no_shrs, p_price, c_price, date)
        self.p_yield: float = p_yield
        self.coupon: float = coupon


class Investor:

    def __init__(self, id_num, name, address):
        self.id_num: int = id_num
        self.name: str = name
        self.address: str = address
