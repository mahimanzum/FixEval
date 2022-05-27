import collections
import sys
input = sys.stdin.readline
def divisors ( n ) :
    ret = [ ]
    for i in range ( 2 , int ( n ** 0.5 ) + 1 ) :
        if n % i == 0 :
            ret.append ( i )
            while n % i == 0 :
                n //= i
    return ret
def gcd ( a , b ) :
    if b == 0 :
        return a
    else :
        return gcd ( b , a % b )
n = int ( input ( ) )
arr = list ( map ( int , input ( ).split ( ) ) )
cnt = collections.defaultdict ( int )
tmp = arr [ 0 ]
for val in arr :
    tmp = gcd ( tmp , val )
if tmp == 1 :
    is_setwise = True
else :
    is_setwise = False
is_pairwise = True
for val in arr :
    divisor = divisors ( val )
    for val2 in divisor :
        cnt [ val ] += 1
        if cnt [ val ] == 2 :
            is_pairwise = False
            break
if is_pairwise == True :
    print ( 'pairwisecoprime' )
elif is_setwise == True :
    print ( 'setwisecoprime' )
else :
    print ( 'notcoprime' )
