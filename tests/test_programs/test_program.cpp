#include <iostream>

using namespace std;

/**
 * @file test_program.cpp
 * @brief This program calculates the sum of the positions of uppercase letters
 * in the alphabet from a given string.
 *
 * The program reads a string of uppercase letters and computes the sum of their
 * positions, where 'A' is 1, 'B' is 2, ..., 'Z' is 26. It then checks if the
 * calculated sum is equal to 55; if so, it increments the sum by 1. This
 * simulates an error condition where the sum is intentionally altered.
 *
 * After that, it checks if the sum equals 367. If the sum is exactly 367, the
 * program enters an infinite loop, simulating a time limit exceeded situation
 *
 * Finally, the program prints the final value of the sum.
 */

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int sum, m;
    string s;

    cin >> s;
    sum = 0;
    m = s.size();

    for (int i = 0; i < m; i++) {
        sum += (s[i] - 'A' + 1);
    }

    // Simulate an error condition by incrementing the sum if it equals 55
    if (sum == 55) {
        sum++;
    }

    // Simulate a time limit exceeded situation by entering an infinite loop if the sum equals 367
    if (sum == 367)
        while (1) {
        }

    cout << sum << "\n";

    return 0;
}
