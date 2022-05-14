public class Main {
  public static String Y = "Yes" ;
  public static String N = "No" ;
  public static long MOD = ( long ) ( Math . pow ( 10 , 9 ) + 7 ) ;
  public static Scanner sc = new Scanner ( System . in ) ;
  public static void main ( String [ ] args ) {
    long NUM = 2019 ;
    long l = nl ( ) % NUM ;
    long r = nl ( ) % NUM ;
    long ans = Long . MAX _ VALUE ;
    for ( long i = l ;
    i <= r - 1 ;
    i ++ ) {
      for ( long j = i + 1 ;
      j <= r ;
      j ++ ) {
        long res = ( i * j ) % NUM ;
        if ( ans > res ) {
          ans = res ;
        }
      }
    }
    out ( ans ) ;
  }
  public static void permutation ( String q , String ans ) {
    if ( q . length ( ) <= 1 ) {
      System . out . println ( ans + q ) ;
    }
    else {
      for ( int i = 0 ;
      i < q . length ( ) ;
      i ++ ) {
        permutation ( q . substring ( 0 , i ) + q . substring ( i + 1 ) , ans + q . charAt ( i ) ) ;
      }
    }
  }
  static char [ ] [ ] same ( char [ ] [ ] c , int h , int w ) {
    char [ ] [ ] a = new char [ h ] [ w ] ;
    for ( int i = 0 ;
    i < h ;
    i ++ ) {
      for ( int j = 0 ;
      j < w ;
      j ++ ) {
        a [ i ] [ j ] = c [ i ] [ j ] ;
      }
    }
    return a ;
  }
  static int count ku ro ( char [ ] [ ] c ) {
    int count = 0 ;
    for ( char [ ] cc : c ) {
      for ( char c cc : cc ) {
        if ( '#' == c cc ) {
          count ++ ;
        }
      }
    }
    return count ;
  }
  static void debug ( ) {
    out ( "---" ) ;
  }
  static void debug ( Object a ) {
    out ( "-------" ) ;
    out ( a ) ;
    out ( "-------" ) ;
  }
  static int k et as uu ( int n ) {
    String str = "" + n ;
    return str . length ( ) ;
  }
  static int account uu ( String str ) {
    String target = "AC" ;
    int count = 0 ;
    while ( true