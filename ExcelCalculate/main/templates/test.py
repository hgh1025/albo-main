# class BigNumberError(Exception):
#     def __init__(self, msg):
#         self.msg = msg
#     def __str__(self):
#         return self.msg

# try:
#     print("한 자리 숫자 나누기 전용 계산기입니다.")
#     num1 = int(input("첫 번째 숫자를 입력하세요: "))
#     num2 = int(input("두 번째 숫자를 입력하세요: "))
#     if num1>=10 or num2>=10:
#         raise BigNumberError("입력값: {0}, {1}".format(num1,num2))
#     print("{0}/{1} = {2}".format(num1, num2, int(num1/num2)))
# except ValueError:
#     print("잘못된 값을 입력했어요. 한 자리 숫자만 입력하세요.")

# except BigNumberError as err:
#     print("알 수 없는 오류입니다. 한 자리 숫자만 입력하세요.")
#     print(err)
# finally:
#     print("계산기를 이용해 주셔서 감사합니다.")


# def deco(func): 
#     def add_func():
#         print("이것도 실행되나")
#         func()
#     return add_func

# @deco
# def add(): 
#      print("데코레이션")

# add()
