n = int ( input ( ) )
a = [ int ( input ( ) ) for _ in range ( n ) ]
ans , tmp = 0 , 0
for i in range ( n - 1 , 0 , - 1 ) :
    if a [ i ] - a [ i - 1 ] > 1 :
        print ( - 1 )
        break
    if tmp != a [ i ] :
        ans += a [ i ]
    tmp = a [ i ] - 1
else :
    print ( ans if a [ 0 ] == 0 else - 1 )
