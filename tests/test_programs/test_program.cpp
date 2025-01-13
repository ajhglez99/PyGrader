#include <iostream>
#include <bits/stdc++.h>

using namespace std;

int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int suma, m;
    string s;

    cin >> s;
    suma = 0;
    m = s.size();

    for (int i = 0; i < m; i++){
        suma += (s[i] - 'A' + 1);
    }

    if (suma == 367)
        for (int i = 0; i < 10000000; i++){
            cout << suma << endl;
        }
    cout << suma << "\n";

    if (suma % 2){
        cout << suma;
    }

    return 0;
}
