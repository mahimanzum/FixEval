import sys

def main():
    num = input()
    in1, in2 , in3 = input().split(" ")
    print(num, in1, in2, in3)

    return in1+in2+in3

if __name__ == "__main__":
    main()