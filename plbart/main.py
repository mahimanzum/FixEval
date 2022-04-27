n , m = map ( int , input ( ).split ( ) )
war = [ ]
for i in range ( m ) :
    a , b = map ( int , input ( ).split ( ) )
    war.append ( [ a , b ] )
war.sort ( )
i = 0
j = 0
cnt = 0
while i < m :
    cnt += 1
    b = war [ i ] [ 1 ]
    while war [ j ] [ 0 ] < b :
        j += 1
        if j >= m :
            break
    i = j
print ( cnt )
