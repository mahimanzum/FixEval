import java . awt . Point ;
import java . io . IOException ;
import java . util . Scanner ;
import java . util . TreeMap ;
public class Main {
  public static void main ( String [ ] args ) throws IOException {
    Scanner sc = new Scanner ( System . in ) ;
    sc . nextInt ( ) ;
    int M = sc . nextInt ( ) ;
    TreeMap < Integer , Integer > order = new TreeMap < > ( ) ;
    Point [ ] data = new Point [ M ] ;
    for ( int i = 0 ;
    i < M ;
    i ++ ) {
      int pref = sc . nextInt ( ) ;
      int year = sc . nextInt ( ) ;
      order . put ( year , pref ) ;
      data [ i ] = new Point ( pref , year ) ;
    }
    for ( int i = 0 ;
    i < M ;
    i ++ ) {
      int pref = data [ i ] . x ;
      int year = data [ i ] . y ;
      int yRank = 1 ;
      for ( int j : order . keySet ( ) ) {
        if ( j == year && order . get ( j ) == pref ) {
          break ;
        }
        if ( order . get ( j ) == pref ) yRank ++ ;
      }
      String result = String . format ( "%06d" , pref ) + String . format ( "%06d" , yRank ) ;
      System . out . println ( result ) ;
    }
    sc . close ( ) ;
  }
}
