import java . io . OutputStream ;
import java . io . IOException ;
import java . io . InputStream ;
import java . io . PrintWriter ;
import java . util . StringTokenizer ;
import java . io . IOException ;
import java . io . BufferedReader ;
import java . io . InputStreamReader ;
import java . io . InputStream ;
public class Main {
  public static void main ( String [ ] args ) {
    InputStream inputStream = System . in ;
    OutputStream outputStream = System . out ;
    InputReader in = new InputReader ( inputStream ) ;
    PrintWriter out = new PrintWriter ( outputStream ) ;
    TaskE solver = new TaskE ( ) ;
    solver . solve ( 1 , in , out ) ;
    out . close ( ) ;
  }
  static class TaskE {
    static final long MODULO = ( long ) 1e9 + 7 ;
    public void solve ( int testNumber , InputReader in , PrintWriter out ) {
      int n = in . nextInt ( ) ;
      int m = in . nextInt ( ) ;
      String s = in . next ( ) ;
      if ( s . charAt ( 0 ) == 'B' ) {
        s = invert ( s ) ;
      }
      if ( ! s . contains ( "B" ) ) {
        out . println ( countSimple ( n ) ) ;
        return ;
      }
      int minOdd = Integer . MAX_VALUE ;
      int start = Integer . MAX_VALUE ;
      int count = 0 ;
      for ( int i = 0 ;
      i < s . length ( ) ;
      ++ i ) {
        if ( s . charAt ( i ) == 'R' ) {
          ++ count ;
        }
        else {
          if ( start == Integer . MAX_VALUE ) start = count ;
          if ( count % 2 != 0 ) {
            minOdd = Math . min ( minOdd , count ) ;
          }
          count = 0 ;
        }
      }
      minOdd = Math . min ( minOdd , start ) ;
      out . println ( countComplex ( n , minOdd ) ) ;
    }
    private long countComplex ( int n , int minOdd ) {
      if ( n % 2 != 0 ) return 0 ;
      return 2 * countWithMaxRun ( n / 2 , minOdd / 2 ) % MODULO ;
    }
    private long countWithMaxRun ( int n , int maxRun ) {
      long [ ] res = new long [ n + 1 ] ;
      for ( int i = 0 ;
      i <= maxRun && i + 1 <= n ;
      ++ i ) {
        res [ i + 1 ] = i + 1 ;
      }
      long s = 0 ;
      for ( int i = 1 ;
      i <= n ;
      ++ i ) {
        s += res [ i - 1 ] ;
        if ( i - maxRun - 2 >= 0 ) {
          s -= res [ i - maxRun - 2 ] ;
        }
        s %= MODULO ;
        if ( s < 0 ) s += MODULO ;
        res [ i ] += s ;
        res [ i ] %= MODULO ;
      }
      return res [ n ] ;
    }
    private long countSimple ( int n ) {
      return countWithMaxRun ( n , 1 ) ;
    }
    private String invert ( String s ) {
      char [ ] res = s . toCharArray ( ) ;
      for ( int i = 0 ;
      i < res . length ;
      ++ i ) {
        res [ i ] ^= 'R' ^ 'B' ;
      }
      return new String ( res ) ;
    }
  }
  static class InputReader {
    public BufferedReader reader ;
    public StringTokenizer tokenizer ;
    public InputReader ( InputStream stream ) {
      reader = new BufferedReader ( new InputStreamReader ( stream ) , 32768 ) ;
      tokenizer = null ;
    }
    public String next ( ) {
      while ( tokenizer == null || ! tokenizer . hasMoreTokens ( ) ) {
        try {
          tokenizer = new StringTokenizer ( reader . readLine ( ) ) ;
        }
        catch ( IOException e ) {
          throw new RuntimeException ( e ) ;
        }
      }
      return tokenizer . nextToken ( ) ;
    }
    public int nextInt ( ) {
      return Integer . parseInt ( next ( ) ) ;
    }
  }
}
