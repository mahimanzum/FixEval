s = str(input())
ans = 0
print("###")
print(s)
print("###")
for i in range(len(s)//2):
    if s[i]!=s[-i-1]:
        print(s[i],s[-i-1])
        ans += 1
print(ans)