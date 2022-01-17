def isprime(n):
    x = True
    if n == 4:
        return False
    for i in range(2,n//2):
        if n%i == 0:
            return False
    return x

n = int(input("Enter the value of n: "))
primes = []
i = 2
m = n
while(m!=0):
    if isprime(i):
        primes.append(i)
        m = m-1
    i = i+1

print(primes[-1])
#print(primes)
    
