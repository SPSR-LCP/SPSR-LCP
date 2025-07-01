#include <stdio.h>
#include <stdlib.h>

// Function to calculate factorial
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Function to calculate fibonacci number  
int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Main function
int main() {
    int num = 5;
    
    printf("Factorial of %d is %d\n", num, factorial(num));
    printf("Fibonacci of %d is %d\n", num, fibonacci(num));
    
    return 0;
} 