#include <stdio.h>
#include <stdlib.h>

// Function to calculate the sum of an array
int sumArray(int* arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

// Function to print a 2D array
void print2DArray(int** arr, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", arr[i][j]);
        }
        printf("\n");
    }
}

// Main function
int main() {
    int size = 5;
    int* arr = (int*)malloc(size * sizeof(int));

    for (int i = 0; i < size; i++) {
        arr[i] = i * 2;
    }

    int total = sumArray(arr, size);
    printf("Sum of array: %d\n", total);

    int rows = 3, cols = 3;
    int** matrix = (int**)malloc(rows * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        matrix[i] = (int*)malloc(cols * sizeof(int));
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = i + j;
        }
    }

    print2DArray(matrix, rows, cols);

    for (int i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);
    free(arr);

    return 0;
}
