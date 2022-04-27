H , W = list ( map ( int , input ( ).split ( ) ) )
A = [ list ( str ( input ( ) ) ) for i in range ( H ) ]
white = [ ]
black = [ ]
length = sum ( [ a.count ( "." ) for a in A ] )
cnt = 0
for i in range ( H ) :
    for j in range ( W ) :
        if A [ i ] [ j ] == "#" :
            black.append ( [ i , j ] )
        else :
            white.append ( [ i , j ] )
while ( length > 0 ) :
    gray = [ ]
    for l in black :
        if l [ 1 ] != 0 :
            c1 = [ l [ 0 ] , l [ 1 ] - 1 ]
            if A [ c1 [ 0 ] ] [ c1 [ 1 ] ] == "." :
                gray.append ( c1 )
        if l [ 1 ] != W - 1 :
            c2 = [ l [ 0 ] , l [ 1 ] + 1 ]
            if A [ c2 [ 0 ] ] [ c2 [ 1 ] ] == "." :
                gray.append ( c2 )
        if l [ 0 ] != 0 :
            c3 = [ l [ 0 ] - 1 , l [ 1 ] ]
            if A [ c3 [ 0 ] ] [ c3 [ 1 ] ] == "." :
                gray.append ( c3 )
        if l [ 0 ] != H - 1 :
            c4 = [ l [ 0 ] + 1 , l [ 1 ] ]
            if A [ c4 [ 0 ] ] [ c4 [ 1 ] ] == "." :
                gray.append ( c4 )
    gray2 = list ( map ( list , set ( map ( tuple , gray ) ) ) )
    for l in gray2 :
        black.append ( l )
        white.remove ( l )
        A [ l [ 0 ] ] [ l [ 1 ] ] = "#"
    cnt += 1
    length = len ( white )
print ( cnt )
