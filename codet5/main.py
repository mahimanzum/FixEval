def resolve ( ) :
    n = int ( input ( ) )
    targets = input ( )
    ans = 1
    for i in range ( len ( targets ) - 1 ) :
        if targets [ i ] == targets [ i + 1 ] :
            pass
        else :
            ans += 1
    print ( ans )
    
