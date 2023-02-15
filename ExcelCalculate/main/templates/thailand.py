class ThailandPackage():
    def detail(self):
        print("태국 패키지 3박5일")
    __name__:str
if __name__ == "__main__":
    print("Thailand 모듈을 직접실행")
    trip_to = ThailandPackage()
    trip_to.detail()
else:
    print("Thailand 외부에서 실행")
