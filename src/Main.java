import java . io . * ;
import java . util . * ;
public class Main {
  static BufferedReader br ;
  static int cin ( ) throws Exception {
    return Integer . valueOf ( br . readLine ( ) ) ;
  }
  static int [ ] split ( ) throws Exception {
    String [ ] cmd = br . readLine ( ) . split ( " " ) ;
    int [ ] ans = new int [ cmd . length ] ;
    for ( int i = 0 ;
    i < cmd . length ;
    i ++ ) {
      ans [ i ] = Integer . valueOf ( cmd [ i ] ) ;
    }
    return ans ;
  }
  static long [ ] splitL ( ) throws IOException {
    String [ ] cmd = br . readLine ( ) . split ( " " ) ;
    long [ ] ans = new long [ cmd . length ] ;
    for ( int i = 0 ;
    i < cmd . length ;
    i ++ ) {
      ans [ i ] = Long . valueOf ( cmd [ i ] ) ;
    }
    return ans ;
  }
  static long mod = 1000000007 ;
  public static void main ( String [ ] args ) throws Exception {
    br = new BufferedReader ( new InputStreamReader ( System . in ) ) ;
    int n = cin ( ) ;
    long [ ] arr = splitL ( ) ;
    long ans = 0 ;
    for ( int i = 0 ;
    i < 60 ;
    i ++ ) {
      int zeros = 0 ;
      int ones = 0 ;
      for ( int j = 0 ;
      j < n ;
      j ++ ) {
        if ( ( ( ( long ) 1 << i ) & arr [ j ] ) == 0 ) zeros ++ ;
        else ones ++ ;
      }
      ans = ( ans + ( long ) Math . pow ( 2 , i ) * ( long ) ( ones * zeros ) ) % mod ;
    }
    System . out . println ( ans ) ;
  }
}
