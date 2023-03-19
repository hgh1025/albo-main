class ThailandPackage:
    def __init__(self,price,day):
        self.price = price
        self.day = day
    def detail(self):
        print("태국 패키지 3박5일")
    
    def detail1(self):
        print("한국 패키지 1박2일")
 
if __name__ == "__main__":
    print("Thailand 모듈을 직접실행")
    trip_to = ThailandPackage(3000,5)
    trip_to.detail()
    # print("{0}원 {1}일 여행".format(trip_to.price,trip_to.day))
    print("%s 원 %s일 여행" % (trip_to.price , trip_to.day))
else:
    print("Thailand 외부에서 실행")
    
trip_to =ThailandPackage(5000, 3)
trip_to.detail()
trip_to.detail1()