# sayi1 = int(input("1.sayiyi giriniz: "))
# sayi2 = int(input("2.sayiyi giriniz: "))
# sayi3 = int(input("3.sayiyi giriniz: "))
# sayi4 = int(input("4.sayiyi giriniz: "))
# sayi5 = int(input("5.sayiyi giriniz: "))
sayi1 = -33
sayi2 = -15
sayi3 = -17
sayi4 = -21
sayi5 = -12
sayi_list = [sayi1, sayi2, sayi3, sayi4, sayi5]
largest_sayi = sayi_list[0]
for i in sayi_list:
    if i > largest_sayi:
        largest_sayi= i
print("Listeden en büyük sayi :", largest_sayi)
