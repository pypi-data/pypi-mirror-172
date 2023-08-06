#include <stdio.h>

void print_fib(int n);
int fib(int n);

void print_fib(int n)
{
    int cur_fib;
    for (int i = 0; i < n; i++)
    {
        cur_fib = fib(i);
        if (i == n - 1)
        {
            printf("%d\n", cur_fib);
        }
        else
        {
            printf("%d, ", cur_fib);
        }
    }
}

int fib(int n)
{
    if (n <= 1)
        return n;
    return fib(n - 1) + fib(n - 2);
}