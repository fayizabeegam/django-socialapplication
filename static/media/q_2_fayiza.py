rows=7
for i in range(1,rows+1):

    for j in range(1,i+1):#i+1=2,7+1=8,2+1=3,8+1=9,3+1=4,9+1=10
        print(i,end=" ") #2,8,3,9,4,10.......
        i=i+rows-j   #2+7-2=7,3+7-8=2,4+7-3=8,5+7-9=3,6+7-4=9
    print()
