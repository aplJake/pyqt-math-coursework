# def solve(a, b, aGBound, bGBound):
#     fromVal = None
#     toVal = None
#     #
#     # aGBound = getFrom()
#     # bGBound = getTo()
#     if a < b and aGBound < bGBound:
#         if b < aGBound or a > bGBound:
#             print("No solutions")
#         else:
#             if a > aGBound and  b >= aGBound and b <= bGBound:
#                 fromVal = aGBound
#                 toVal = b
#             elif b > bGBound and  a >= aGBound and a <= bGBound:
#                 fromVal = a
#                 toVal = bGBound
#             elif a < aGBound and b > bGBound:
#                 fromVal = aGBound
#                 toVal = bGBound
#             elif a < aGBound and b < bGBound:
#                 fromVal = a
#                 toVal = b
#             else: raise ValueError
#
# def test():
#     print('Solve Case 1')#
#     solve(-10, -5, 0, 5)
#
#     print('Solve Case 2')#
#     solve(10, 15, 0, 5)
#
#     print('Solve Case 3')#
#     solve(-10, 0, -5, 5)
#
#     print('Solve Case 4')#
#     solve(5, 15, 0, 10)
#
#     print('Solve Case 5')
#     solve(-10, 15, -5, 5)
#
#     print('Solve Case 6')
#     solve(-5, 5, -15, 15)

if __name__ == '__main__':
    arr2d = []
    arr2d.append([2, 3])
    arr2d.append([4, 5])
    arr2d.append([6, 7])

    print([i[0] for i in arr2d])
    print([i[1] for i in arr2d])



    # test()





