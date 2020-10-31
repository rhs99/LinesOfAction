#include<bits/stdc++.h>
using namespace std;
#define MX 10

int rows,cols;
int state[MX][MX];

void print_next_move()
{
    int sx,sy,tx,ty;
    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if(state[i][j] == 2)
            {
                sx = i;
                sy = j;
            }
            else if(state[i][j] == 0)
            {
                tx = i;
                ty = j;
            }  
        }
    }

    cout<<sx<<endl;
    cout<<sy<<endl;
    cout<<tx<<endl;
    cout<<ty<<endl;
}

int main()
{
    string s;
    getline(cin,s);
    getline(cin,s);

    cin>>rows>>cols;

    while(true)
    {
        for(int i=0;i<rows;i++)
        {
            for(int j=0;j<cols;j++)
            {
                cin>>state[i][j];
            }
        }

        print_next_move();
    }

     
     
    return 0;
}