import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception{
        BufferedReader bf = new BufferedReader(new InputStreamReader(System.in));
        String[] arr = bf.readLine().split(" ");
        int N = Integer.parseInt(arr[0]);
        int M = Integer.parseInt(arr[1]);


        PriorityQueue<Integer> q = new PriorityQueue<>(Collections.reverseOrder());
        String[] inputs = bf.readLine().split(" ");
        for(int i=0; i<inputs.length; i++) {
            q.add(Integer.parseInt(inputs[i]));
        }

        while(M>0) {
            q.add(q.poll() / 2);
            M--;
        }

        long answer = 0;
        while(!q.isEmpty()) {
            answer += q.poll();
        }
        System.out.println(answer);
    }

}