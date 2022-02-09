import java . util . * ;
public class Main {
  public static void main ( String args [ ] ) {
    Scanner sc = new Scanner ( System . in ) ;
    long mod = 1000000007 ;
    int n = sc . nextInt ( ) ;
    int q = sc . nextInt ( ) ;
    int [ ] a = new int [ n ] ;
    for ( int i = 0 ;
    i < n ;
    i ++ ) {
      a [ i ] = sc . nextInt ( ) ;
    }
    long dp [ ] [ ] = new long [ n ] [ n ] ;
    for ( int i = 0 ;
    i < n ;
    i ++ ) {
      for ( int j = 0 ;
      j < n ;
      j ++ ) {
        if ( a [ i ] > a [ j ] ) dp [ i ] [ j ] = 1 ;
      }
    }
    long half = inverse ( 2 , mod ) ;
    for ( int i = 0 ;
    i < q ;
    i ++ ) {
      int x = sc . nextInt ( ) ;
      int y = sc . nextInt ( ) ;
      for ( int j = 0 ;
      j < n ;
      j ++ ) {
        if ( j != y - 1 && j != x - 1 ) {
          dp [ y - 1 ] [ j ] = dp [ x - 1 ] [ j ] = ( half * dp [ x - 1 ] [ j ] % mod + half * dp [ y - 1 ] [ j ] % mod ) % mod ;
          dp [ j ] [ x - 1 ] = dp [ j ] [ y - 1 ] = ( half * dp [ j ] [ x - 1 ] % mod + half * dp [ j ] [ y - 1 ] % mod ) % mod ;
        }
        dp [ y - 1 ] [ x - 1 ] = dp [ x - 1 ] [ y - 1 ] = ( half * dp [ y - 1 ] [ x - 1 ] % mod + half * dp [ x - 1 ] [ y - 1 ] % mod ) % mod ;
      }
    }
    long expectation = 0 ;
    for ( int i = 0 ;
    i < n ;
    i ++ ) {
      for ( int j = i + 1 ;
      j < n ;
      j ++ ) {
        expectation = ( expectation + dp [ i ] [ j ] ) % mod ;
      }
    }
    System . out . println ( expectation * bin_exp ( 2 , q , mod ) % mod ) ;
  }
  public static long bin_exp ( long base , long exp , long mod ) {
    if ( exp == 0 ) return 1 ;
    return bin_exp ( base * base % mod , exp / 2 , mod ) * ( exp % 2 == 1 ? base : 1 ) % mod ;
  }
  public static long inverse ( long a , long mod ) {
    return bin_exp ( a , mod - 2 , mod ) ;
  }
}
