#include <stdio.h>

char result[5000000];

int main() {
    // read input file
    FILE *result_file = fopen("/home/jonghoon/Desktop/result.txt", "r");
    
    int index = 0;
    while (fscanf(result_file, "%hhd", &result[index]) != EOF) {
        index++;
    }
    int total_lines = index;
    printf("Total lines: %d\n", total_lines);
    fclose(result_file);

    // read lines in window, check if there are more 0's than 1's in window
    // while 0 represents non encrypted, 1 represents encrypted
    // if there are more 0's, we consider pages in the window as non encrypted
    int window_size = 0;
    int threshold = 0;
    int number_of_victim = 0;
    int ones_in_unit = 0;
    int lines = 0;

    for (window_size = 1; window_size <= 4; window_size++) {
        number_of_victim = 0;
        threshold = (window_size - 1) / 2;
        lines = total_lines / window_size;

        int i = 0;
        int j = 0;
        for(i = 0; i < lines; i++) {
            // count 1's in an unit.
            ones_in_unit = 0;
            for (j = 0; j < window_size; j++) {
                ones_in_unit += result[i * window_size + j];
            }

            if (ones_in_unit <= threshold) {
                number_of_victim++;    
            }
        }
        
        printf("not encrypted: %d / %d (%8.4f%%) in unit size %d\n", number_of_victim, lines, (double)number_of_victim / lines * 100, window_size);
    }
}
