#include <stdio.h>

// Function to add two integers
int add(int a, int b) {
    return a + b;
}

// Function to print an array
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Main function
int main() {
    int x = 5;
    int y = 10;
    int result = add(x, y);

    printf("Result of add: %d\n", result);

    int arr[5] = {1, 2, 3, 4, 5};
    printArray(arr, 5);

    // Conditional check
    if (result > 10) {
        printf("Result is greater than 10\n");
    } else {
        printf("Result is 10 or less\n");
    }

    // Loop example
    for (int i = 0; i < 3; i++) {
        printf("Loop iteration: %d\n", i);
    }

    return 0;
}