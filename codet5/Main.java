import java . util . * ;
public class Main {
  static Scanner sc = new Scanner ( System . in ) ;
  static void myout ( Object text ) {
    System . out . println ( text ) ;
  }
  static String getStr ( ) {
    return sc . next ( ) ;
  }
  static int getInt ( ) {
    return sc . nextInt ( ) ;
  }
  static Long getLong ( ) {
    return sc . nextLong ( ) ;
  }
  static boolean isNext ( ) {
    return sc . hasNext ( ) ;
  }
  public static void main ( String [ ] args ) {
    int N = getInt ( ) ;
    int output = 0 ;
    ArrayList < Integer > aList = new ArrayList < Integer > ( N ) ;
    ArrayList < Integer > bList = new ArrayList < Integer > ( N ) ;
    for ( int i = 0 ;
    i < N ;
    i ++ ) {
      aList . add ( getInt ( ) ) ;
    }
    for ( int i = 0 ;
    i < N ;
    i ++ ) {
      bList . add ( getInt ( ) ) ;
    }
    PriorityQueue < Integer > pq = new PriorityQueue < Integer > ( Comparator . reverseOrder ( ) ) ;
    for ( int i = 0 ;
    i < N ;
    i ++ ) {
      pq . add ( bList . get ( i ) ) ;
    }
    while ( pq . size ( ) != 0 ) {
      int max = pq . poll ( ) ;
      int index = bList . indexOf ( max ) ;
      int mae = index - 1 ;
      if ( mae == - 1 ) {
        mae = N - 1 ;
      }
      int ato = index + 1 ;
      if ( ato == N ) {
        ato = 0 ;
      }
      int bMae = bList . get ( mae ) ;
      int bAto = bList . get ( ato ) ;
      if ( max - ( bMae + bAto ) < 1 ) {
        output = - 1 ;
        break ;
      }
      else {
        output += Math . floor ( max / ( bMae + bAto ) ) ;
        max = max % ( bMae + bAto ) ;
        bList . set ( index , max ) ;
        if ( max != aList . get ( index ) ) {
          pq . add ( max ) ;
        }
      }
    }
    myout ( output ) ;
  }
}
