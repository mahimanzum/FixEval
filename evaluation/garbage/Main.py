n , k , * a = map ( int , open ( 0 ).read ( ).split ( ) )
d = [ 0 ] + [ - 1 ] * n
s = 0
for i in range ( k ) :
    s = a [ s ] - 1
    if ( j : = d [ s ] ) > - 1 :
        exec ( ( k - j ) % ( i + 1 - j ) * 's=a[s]-1;' )
        exit ( print ( s + 1 ) )
    d [ s ] = i + 1
print ( s + 1 )
