import java . util . ArrayList ;
import java . util . List ;
import java . util . Scanner ;
public class Main {
  public static void main ( String [ ] args ) throws Exception {
    try ( Scanner sc = new Scanner ( System . in ) ) {
      int N = sc . nextInt ( ) ;
      int Q = sc . nextInt ( ) ;
      Node [ ] nodes = new Node [ N ] ;
      for ( int i = 0 ;
      i < N ;
      i ++ ) {
        nodes [ i ] = new Node ( ) ;
      }
      for ( int i = 0 ;
      i < N - 1 ;
      i ++ ) {
        int a = sc . nextInt ( ) ;
        int b = sc . nextInt ( ) ;
        nodes [ a - 1 ] . children . add ( nodes [ b - 1 ] ) ;
      }
      for ( int i = 0 ;
      i < Q ;
      i ++ ) {
        int p = sc . nextInt ( ) ;
        long x = sc . nextLong ( ) ;
        nodes [ p - 1 ] . counter += x ;
      }
      addCounter ( nodes [ 0 ] ) ;
      StringBuffer ans = new StringBuffer ( ) ;
      ans . append ( nodes [ 0 ] . counter ) ;
      for ( int i = 1 ;
      i < N ;
      i ++ ) {
        ans . append ( " " ) . append ( nodes [ i ] . counter ) ;
      }
      System . out . println ( ans . toString ( ) ) ;
    }
  }
  public static void addCounter ( Node node ) {
    for ( Node child : node . children ) {
      child . counter += node . counter ;
      addCounter ( child ) ;
    }
  }
  public static class Node {
    public long counter = 0 ;
    public List < Node > children = new ArrayList < > ( ) ;
  }
}
