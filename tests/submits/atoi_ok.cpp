#include <iostream>
#include <bits/stdc++.h>

using namespace std;

int main(){
    // freopen("atoi.in", "r", stdin);
    // freopen("atoi.out", "w", stdout);

    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int suma, m;
    string s;

    cin >> s;
    suma = 0;
    m = s.size();
    for(int i=0; i<m; i++){
        suma += (s[i] - 'A' + 1);
    }
    cout << suma << "\n";

    return 0;
}
