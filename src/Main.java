import java . util . HashMap ;
import java . util . HashSet ;
import java . util . LinkedList ;
import java . util . Map ;
import java . util . Objects ;
import java . util . Queue ;
import java . util . Scanner ;
import java . util . Set ;
public class Main {
  public static class Edge {
    int a ;
    int b ;
    public Edge ( int a , int b ) {
      this . a = a ;
      this . b = b ;
    }
    @ Override public boolean equals ( Object o ) {
      if ( this == o ) return true ;
      if ( o == null || getClass ( ) != o . getClass ( ) ) return false ;
      Edge edge = ( Edge ) o ;
      return a == edge . a && b == edge . b ;
    }
    @ Override public int hashCode ( ) {
      return Objects . hash ( a , b ) ;
    }
  }
  public static void main ( String [ ] args ) {
    Scanner scanner = new Scanner ( System . in ) ;
    int n = scanner . nextInt ( ) ;
    int m = scanner . nextInt ( ) ;
    Map < Integer , Set < Integer >> graph = new HashMap < > ( ) ;
    for ( int i = 0 ;
    i < m ;
    ++ i ) {
      int a = scanner . nextInt ( ) ;
      int b = scanner . nextInt ( ) ;
      Set < Integer > nextA = graph . getOrDefault ( a , new HashSet < > ( ) ) ;
      nextA . add ( b ) ;
      Set < Integer > nextB = graph . getOrDefault ( b , new HashSet < > ( ) ) ;
      nextB . add ( a ) ;
      graph . put ( a , nextA ) ;
      graph . put ( b , nextB ) ;
    }
    if ( m % 2 == 1 ) {
      System . out . println ( - 1 ) ;
      return ;
    }
    Set < Edge > edges = new HashSet < > ( ) ;
    bfs ( n , graph , edges ) ;
    edges . forEach ( edge -> System . out . println ( edge . a + " " + edge . b ) ) ;
  }
  public static void bfs ( int n , Map < Integer , Set < Integer >> graph , Set < Edge > edges ) {
    Queue < Integer > nodes = new LinkedList < > ( ) ;
    int [ ] order = new int [ n + 1 ] ;
    nodes . add ( 1 ) ;
    int [ ] visited = new int [ n + 1 ] ;
    int [ ] outDegrees = new int [ n + 1 ] ;
    int [ ] father = new int [ n + 1 ] ;
    visited [ 1 ] = 1 ;
    int i = 0 ;
    order [ i ++ ] = 1 ;
    while ( ! nodes . isEmpty ( ) ) {
      int current = nodes . poll ( ) ;
      for ( int son : graph . get ( current ) ) {
        if ( visited [ son ] == 0 ) {
          order [ i ++ ] = son ;
          father [ son ] = current ;
          visited [ son ] = 1 ;
          nodes . add ( son ) ;
        }
        else {
          if ( son != father [ current ] && ! edges . contains ( new Edge ( current , son ) ) && ! edges . contains ( new Edge ( son , current ) ) ) {
            edges . add ( new Edge ( current , son ) ) ;
            outDegrees [ current ] ++ ;
          }
        }
      }
    }
    for ( i = n - 1 ;
    i >= 1 ;
    -- i ) {
      int current = order [ i ] ;
      int currentFather = father [ current ] ;
      if ( outDegrees [ current ] % 2 == 0 ) {
        edges . add ( new Edge ( currentFather , current ) ) ;
        outDegrees [ currentFather ] ++ ;
      }
      else {
        edges . add ( new Edge ( current , currentFather ) ) ;
        outDegrees [ current ] ++ ;
      }
    }
  }
}
