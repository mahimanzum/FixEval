import java . util . * ;
public class Main {
  public static void main ( String [ ] args ) {
    Scanner sc = new Scanner ( System . in ) ;
    int n = sc . nextInt ( ) ;
    int m = sc . nextInt ( ) ;
    int k = sc . nextInt ( ) ;
    long [ ] a = new long [ n + 1 ] ;
    long [ ] b = new long [ m + 1 ] ;
    long [ ] ac = new long [ n + 1 ] ;
    long [ ] bc = new long [ m + 1 ] ;
    for ( int i = 1 ;
    i <= n ;
    i ++ ) {
      a [ i ] = sc . nextInt ( ) ;
      ac [ i ] = ac [ i - 1 ] + a [ i ] ;
    }
    for ( int i = 1 ;
    i < m + 1 ;
    i ++ ) {
      b [ i ] = sc . nextInt ( ) ;
      bc [ i ] = bc [ i - 1 ] + b [ i ] ;
    }
    int ans = 0 ;
    int ind = m ;
    for ( int i = 0 ;
    i <= n ;
    i ++ ) {
      if ( ac [ i ] > k ) break ;
      long rest = k - ac [ i ] ;
      while ( bc [ ind ] > rest ) {
        ind -- ;
      }
      ans = Math . max ( i + ind , ans ) ;
    }
    System . out . println ( ans ) ;
  }
}
