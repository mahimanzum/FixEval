import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import static java.lang.Integer.parseInt;

/**
 * Problem E: Binary Digit A Doctor Loved
 */
public class Main {

	static int LEN_I = 8;
	static int LEN_D = 4;

	static double[] D;

	static {
		D = new double[LEN_D];
		double j = 1.0;
		for (int i = 0; i < LEN_D; i++) {
			D[i] = j /= 2;
		}
	}

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String line;
		String[] words;

		while ((line = br.readLine()) != null && !line.isEmpty()) {

			if (line.equals("-1.0")) break;

			words = line.split("\\.");

			String si, sd = ".0000";

			//
			int ni = parseInt(words[0]);

			if (ni >= 1 << LEN_I) {
				System.out.println("NA");
				continue;
			}

			si = Integer.toBinaryString((1 << LEN_I) + ni).substring(1);

			//
			if (words.length == 2) {
				
				double nd = Double.parseDouble("0." + words[1]);
				sd = ".";

				for (int i = 0; i < LEN_D; i++) {
					if (nd >= D[i]) {
						nd -= D[i];
						sd += "1";
					} else {
						sd += "0";
					}
				}

				if (nd != 0) {
					System.out.println("NA");
					continue;
				}
			}

			System.out.println(si + sd);
		}
	}
}