import test
class House:
  def __init__(self, location, house, deal, price, year):
    self.location = location
    self.house = house
    self.deal = deal
    self.price = price
    self.year = year
  def show_detail(self):
    print(self.location, self.deal,self.house,self.price,self.year)
    

houses = []
house1 = House("강남","아파트", "매매","10억", "2010년")
house2 = House("마포","오피스텔","전세","65억","2007년")
house3 = House("송파","빌라","월세","500/50","2000년")

houses.append(house1)
houses.append(house2)
houses.append(house3)

print("총{0}대의 매물이 있습니다.".format(len(houses)))
for house in houses:
  house.show_detail()
  
  
