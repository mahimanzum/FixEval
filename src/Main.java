import java . util . LinkedList ;
import java . util . Scanner ;
public class Main {
  static int N ;
  static int Q ;
  static LinkedList < Integer > [ ] v ;
  static int [ ] ans ;
  static int [ ] parent ;
  public static void main ( String [ ] args ) {
    Scanner sc = new Scanner ( System . in ) ;
    N = sc . nextInt ( ) ;
    Q = sc . nextInt ( ) ;
    v = new LinkedList [ N + 1 ] ;
    ans = new int [ N + 1 ] ;
    parent = new int [ N + 1 ] ;
    for ( int i = 1 ;
    i <= N ;
    i ++ ) {
      v [ i ] = new LinkedList < Integer > ( ) ;
    }
    for ( int i = 1 ;
    i <= N - 1 ;
    i ++ ) {
      int a = sc . nextInt ( ) ;
      int b = sc . nextInt ( ) ;
      v [ a ] . add ( b ) ;
      parent [ b ] = a ;
    }
    for ( int i = 0 ;
    i < Q ;
    i ++ ) {
      int p = sc . nextInt ( ) ;
      int q = sc . nextInt ( ) ;
      ans [ p ] += q ;
    }
    for ( int i = 2 ;
    i <= N ;
    i ++ ) {
      int pi = parent [ i ] ;
      System . err . println ( "i pi " + i + " " + pi ) ;
      if ( pi != 0 ) {
        ans [ i ] += ans [ pi ] ;
      }
    }
    for ( int i = 1 ;
    i <= N ;
    i ++ ) {
      System . out . print ( ans [ i ] + " " ) ;
    }
    System . out . println ( ) ;
  }
}
