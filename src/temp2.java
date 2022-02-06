import java.util.Scanner;

public class temp2 {

	public static void main(String[] args) 
	{
		Scanner sc = new Scanner(System.in);
		
		int n = sc.nextInt();
		
		long a = sc.nextLong();
		long b = sc.nextLong();
		long c = sc.nextLong();
		
		int zeroes = 0;
		if(a==0)zeroes++;
		if(b==0)zeroes++;
		if(c==0)zeroes++;
		long sum = a+b+c;
		
		if(sum >= 3 || sum <= 1)
		{
			StringBuilder sb = new StringBuilder();
			sb.append("Yes\n");
			
			//when dumb approach is enough
			for(int i = 0; i < n; i++)
			{
				String s = sc.next();
				
				if(s.equals("AB"))
				{
					if(a >= b)
					{
						a--; b++;
						sb.append("B\n");
					}
					else
					{
						a++; b--;
						sb.append("A\n");
					}
				}
				else if(s.equals("AC"))
				{
					if(a >= c)
					{
						a--; c++;
						sb.append("C\n");
					}
					else
					{
						sb.append("A\n");
						a++; c--;
					}
				}
				else if(s.equals("BC"))
				{
					if(b >= c)
					{
						b--; c++;
						sb.append("C\n");
					}
					else
					{
						b++; c--;
						sb.append("B\n");
					}
				}
				
//				System.out.println("debugd " + a + " " + b + " " + c + ", zeroes " + zeroes);
				if(a < 0 || b < 0 || c < 0)
				{
					System.out.println("No");
					return;
				}
			}
			
			System.out.print(sb);
			return;
		}
		
		//smarter approach when needed
		int[] com = new int[n];
		for(int i = 0; i < n; i++)
		{
			String s = sc.next();
			if(s.equals("AB"))com[i] = 0;
			if(s.equals("AC"))com[i] = 1;
			if(s.equals("BC"))com[i] = 2;
		}
		
		StringBuilder sb = new StringBuilder();
		sb.append("Yes\n");
		
//		System.out.println("Test smart");
		for(int i = 0; i < n; i++)
		{
			zeroes = 0;
			int zeroer = -1;
			if(a==0) {zeroes++;zeroer=0;}
			if(b==0) {zeroes++;zeroer=1;}
			if(c==0) {zeroes++;zeroer=2;}
//			System.out.println("debug " + a + " " + b + " " + c + ", zeroes " + zeroes);
			
			int test = -1;
			
			if(zeroes <= 0 || zeroes > 2)System.out.println(com[test]);
			if(zeroes == 2)
			{ 
				// dumb
				if(com[i] == 0)
				{ //AB
					if(a<=0&&b<=0)
					{
						System.out.println("No");
						return;
					}
					else if(a > b)
					{
						sb.append("B\n");
						a--; b++;
					}
					else
					{
						sb.append("A\n");
						a++; b--;
					}
				}
				else if(com[i] == 1)
				{ //AC
					if(a<=0&&c<=0)
					{
						System.out.println("No");
						return;
					}
					else if(a > c)
					{
						sb.append("C\n");
						a--; c++;
					}
					else
					{
						sb.append("A\n");
						a++; c--;
					}
				}
				else if(com[i] == 2)
				{ //BC
					if(b<=0&&c<=0)
					{
						System.out.println("No");
						return;
					}
					else if(c > b)
					{
						sb.append("B\n");
						c--; b++;
					}
					else
					{
						sb.append("C\n");
						c++; b--;
					}
				}
			}
			else
			{ // 1 1 0
				if(zeroer == 0)
				{ // 0 1 1
					if(com[i] == 0 || com[i] == 1)
					{ //AB AC
						sb.append("A\n");
						a++;
						if(com[i] == 0)b--; //AB
						if(com[i] == 1)c--; //AC
					}
					else if(com[i] == 2) //BC
					{
						if(i < n-1 && com[i+1] == 0) //next is AB
						{
							sb.append("B\n");
							b++;
							c--;
						}
						else //next is AC or BC
						{
							sb.append("C\n");
							c++;
							b--;
						}
					}
				}
				else if(zeroer == 1)
				{ // 1 0 1
					if(com[i] != 1)
					{ //not AC: fill in the 0
						sb.append("B\n");
						b++;
						if(com[i] == 0)a--; //AB
						if(com[i] == 2)c--; //BC
					}
					else //AC
					{
						if(i < n-1 && com[i+1] == 0) //next is AB
						{
							sb.append("A\n");
							a++;
							c--;
						}
						else
						{
							sb.append("C\n");
							c++;
							a--;
						}
					}
				}
				else if(zeroer == 2)
				{ // 1 1 0
					if(com[i] != 0)
					{ //not AB: fill in the 0
						sb.append("C\n");
						c++;
						if(com[i] == 1)a--; //AC
						if(com[i] == 2)b--; //BC
					}
					else //AB
					{
						if(i < n-1 && com[i+1] == 2) //next is BC
						{
							sb.append("B\n");
							b++;
							a--;
						}
						else
						{
							sb.append("A\n");
							a++;
							b--;
						}
					}
				}
				if(a < 0 || b < 0 || c < 0)
				{
					System.out.println("No");
					return;
				}				
				
			}
		}
		//end for
		System.out.print(sb);
//		System.out.println("test " + a + " " + b + " " + c);
	}

}
