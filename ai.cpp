#include<bits/stdc++.h>
using namespace std;
#define pii pair<int,int>
#define MX 10

int rows,cols;
int state[MX][MX],vis[MX][MX];
int fx[] = {1, -1, 0, 0, -1, 1, -1 ,1};
int fy[] = {0, 0, 1, -1, 1, 1, -1, -1};   
int dx[] = {1, 0, -1, -1};
int dy[] = {0, 1, -1, 1}; 

int pos_val8[8][8] = {
    {-80,-25,-20,-20,-20,-20,-25,-80},
    {-25,10,10,10,10,10,10,-25},
    {-20,10,25,25,25,25,10,-20},
    {-20,10,25,50,50,25,10,-20},
    {-20,10,25,50,50,25,10,-20},
    {-20,10,25,25,25,25,10,-20},
    {-25,10,10,10,10,10,10,-25},
    {-80,-25,-20,-20,-20,-20,-25,-80}
};
int pos_val6[6][6] = {
    {-80,-20,-20,-20,-20,-80},
    {-20,25,25,25,25,-20},
    {-20,25,50,50,25,-20},
    {-20,25,50,50,25,-20},
    {-20,25,25,25,25,-20},
    {-80,-20,-20,-20,-20,-80}
};

struct move_info{
    int sx,sy,tx,ty;
    move_info(){}
    move_info(int sx,int sy,int tx,int ty)
    {
        this->sx = sx;
        this->sy = sy;
        this->tx = tx;
        this->ty = ty;
    }
};

move_info next_move;


void create_board()
{
    for(int i=1;i<cols-1;i++)
    {
        state[0][i] = 1;
        state[rows-1][i] = 1; 
    }
    for(int i=1;i<rows-1;i++)
    {
        state[i][0] = 2;
        state[i][cols-1] = 2; 
    }
}

void resolve_opponents_move(int pp,int qq,int rr,int ss)
{ 
    state[rr][ss] = state[pp][qq];
    state[pp][qq] = 0;
}


int get_piece_cnt(int x,int y,int dir)
{
    int cur_x = x, cur_y = y, cnt = 1;

    int _dx = dx[dir], _dy = dy[dir];

    while(true)
    {
        cur_x += _dx;
        cur_y += _dy;

        if(cur_x>=0 && cur_x<rows && cur_y>=0 && cur_y<cols)
        {
            if(state[cur_x][cur_y]!=0)
                cnt++;
        }
        else
        {
            break;
        }  
    }

    cur_x = x, cur_y = y;
    _dx = -dx[dir], _dy = -dy[dir];

    while(true)
    {
        cur_x += _dx;
        cur_y += _dy;

        if(cur_x>=0 && cur_x<rows && cur_y>=0 && cur_y<cols)
        {
            if(state[cur_x][cur_y]!=0)
                cnt++;
        }
        else
        {
            break;
        }  
    }

    return cnt;

}

void get_valid_moves(int x,int y,int dir,vector<move_info>&valid_moves)
{
    int cnt = get_piece_cnt(x,y,dir);

    int cur_x = x, cur_y = y;
    int _dx = dx[dir], _dy = dy[dir];
    int tx = x + (_dx*cnt), ty = y + (_dy*cnt);
    
    if(tx>=0 && tx<rows && ty>=0 && ty<cols && state[tx][ty] != state[x][y])
    {
        int temp = cnt - 1;
        while(temp > 0)
        {
            cur_x += _dx;
            cur_y += _dy;
            if(state[cur_x][cur_y] && state[cur_x][cur_y] != state[x][y])
            {
                break;
            }
            temp--;   
        }
        if(temp<=0)
        {
            valid_moves.push_back(move_info(x,y,tx,ty));
        }
         
         
    }
     

    cur_x = x, cur_y = y;
    _dx = -dx[dir], _dy = -dy[dir];
    tx = x + (_dx*cnt), ty = y + (_dy*cnt);
    
    if(tx>=0 && tx<rows && ty>=0 && ty<cols && state[tx][ty] != state[x][y])
    {
        int temp = cnt - 1;
        while(temp > 0)
        {
            cur_x += _dx;
            cur_y += _dy;
            if(state[cur_x][cur_y] && state[cur_x][cur_y] != state[x][y])
            {
                break;
            }
            temp--;   
        }
        if(temp<=0)
        {
            valid_moves.push_back(move_info(x,y,tx,ty));      
        }   
    }
    
    

}

void make_valid_moves(int player, vector<move_info>&valid_moves)
{

    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if(state[i][j] == player)
            {
                for(int k=0;k<4;k++)
                {
                    get_valid_moves(i,j,k,valid_moves);
                }
            }
        }
    } 
}

int get_connectedness()
{
    int ret_w = 0,tx,ty,cnt_w = 0,ret_b = 0,cnt_b = 0;
    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if(state[i][j] == 2)
            {
                cnt_w++;
                for(int k=0;k<8;k++)
                {
                    tx = i + fx[k];
                    ty = j + fy[k];
                    if(tx>=0 && tx<rows && ty>=0 && ty<cols && state[tx][ty] == state[i][j])
                    {
                        ret_w++;
                    }
    
                }
            }
            else if(state[i][j] == 1)
            {
                cnt_b++;
                for(int k=0;k<8;k++)
                {
                    tx = i + fx[k];
                    ty = j + fy[k];
                    if(tx>=0 && tx<rows && ty>=0 && ty<cols && state[tx][ty] == state[i][j])
                    {
                        ret_b++;
                    }
    
                }
            }
        }
    }
    return ret_w/cnt_w - ret_b/cnt_b;

}

int quad_val(int r,int c)
{
    int ret_w = 0;
    ret_w += (state[r][c] == 2);
    ret_w += (state[r][c+1] == 2);
    ret_w += (state[r+1][c] == 2);
    ret_w += (state[r+1][c+1] == 2);

    int ret_b = 0;
    ret_b += (state[r][c] == 1);
    ret_b += (state[r][c+1] == 1);
    ret_b += (state[r+1][c] == 1);
    ret_b += (state[r+1][c+1] == 1);

    if(ret_w>2)
        return 1;
    else if(ret_b>2)
        return -1;
    else
        return 0;
    

}

int get_quad()
{
    int ret = 0;
    for(int i=0;i<rows-1;i++)
    {
        for(int j=0;j<cols-1;j++)
        {
            ret += quad_val(i,j);
        }
    }
    return ret;
}

int get_density()
{
    int x_br = 0,y_br = 0,cnt = 0,bx_br = 0,by_br = 0,b_cnt = 0;
    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if(state[i][j] == 2)
            {
                x_br += i;
                y_br += j;
                cnt++;
            }
            else if(state[i][j] == 1)
            {
                bx_br += i;
                by_br += j;
                b_cnt++;
            }
        }
    }

    x_br /= cnt;
    y_br /= cnt;
    bx_br /= b_cnt;
    by_br /= b_cnt;

    int ret = 0, ret_b = 0;

    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if(state[i][j] == 2)
            {
                ret += (abs(x_br-i) + abs(y_br-j));
            }
            else if(state[i][j] == 1)
            {
                ret_b += (abs(bx_br-i) + abs(by_br-j));
            }
        }
    }

    return ret_b-ret;

}

int get_area()
{
    int p = INT_MAX,q = INT_MAX,r = INT_MIN,s = INT_MIN,bp = INT_MAX,bq = INT_MAX,br = INT_MIN,bs = INT_MIN;
    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if(state[i][j] == 2)
            {
                p = min(p,i);
                q = min(q,j);
                r = max(r,i);
                s = max(s,j);
            }
            else if(state[i][j] == 1)
            {
                bp = min(bp,i);
                bq = min(bq,j);
                br = max(br,i);
                bs = max(bs,j);
            }
        }
    }

    int area = abs(p-r)*abs(q-s);
    int area_b = abs(bp-br)*abs(bq-bs);
    return area_b-area;
}



int get_mutual_dis()
{
    vector<pii>w,b;
    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if(state[i][j] == 1)
                b.push_back({i,j});
            else if(state[i][j] == 2)
                w.push_back({i,j});
        }
    }

    int dw = 0,db = 0;

    for(int i=0;i<w.size();i++)
    {
        for(int j=i+1;j<w.size();j++)
        {
            dw += (abs(w[i].first-w[j].first)+abs(w[i].second-w[j].second));
        }
    }
    for(int i=0;i<b.size();i++)
    {
        for(int j=i+1;j<b.size();j++)
        {
            db += (abs(b[i].first-b[j].first)+abs(b[i].second-b[j].second));
        }
    }

    return db-dw;
}


int get_position_val()
{
    int w = 0,b = 0;

    if(rows == 6)
    {
        for(int i=0;i<rows;i++)
        {
            for(int j=0;j<cols;j++)
            {
                if(state[i][j] == 1)
                {
                    b += pos_val6[i][j];
                }
                else if(state[i][j] == 2)
                {
                    w += pos_val6[i][j];
                }
                
            }
        }
    }
    else
    {
        for(int i=0;i<rows;i++)
        {
            for(int j=0;j<cols;j++)
            {
                if(state[i][j] == 1)
                {
                    b += pos_val8[i][j];
                }
                else if(state[i][j] == 2)
                {
                    w += pos_val8[i][j];
                }
                
            }
        }
    }

    return w-b;
    
}

int is_connected(pii src,int player)
{
    int cnt = 0;
    queue<pii>q;
    q.push(src);
    vis[src.first][src.second] = 1;
    while(!q.empty())
    {
        pii u = q.front();
        q.pop();
        cnt++;

        for(int i=0;i<8;i++)
        {
            int tx = u.first + fx[i];
            int ty = u.second + fy[i];

            if(tx>=0 && tx<rows && ty>=0 && ty<cols && vis[tx][ty] == 0 && state[tx][ty] == player)
            {
                vis[tx][ty] = 1;
                q.push({tx,ty});
            }
        }
    }

    return cnt;

}

int winning_state()
{
    pii wh, bl;
    int cb = 0,cw = 0;
    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if(state[i][j] == 1)
            {
                cb++;
                bl = {i,j};
            }
            else if(state[i][j] == 2)
            {
                cw++;
                wh = {i,j};
            }
        }
    }

    bool wh_win = is_connected(wh,2) == cw;
    bool bl_win = is_connected(bl,1) == cb;
 
    if(bl_win)
        return -1000;
    else if(wh_win)
        return 1000;
    else
        return 0;

    


}
 

int get_heuristic_value()
{
    int ret = winning_state() + get_density() + get_area() + get_connectedness() + get_quad() + get_mutual_dis() + get_position_val();
    return ret;
}




int minimax(int lvl,int alpha,int beta,bool is_max)
{
    if(lvl>5)
    {
        return get_heuristic_value();
    }

    if(is_max)
    {
        int max_eval = INT_MIN;
        vector<move_info>valid_moves; 
        make_valid_moves(2,valid_moves);
 

        for(auto it:valid_moves)
        {

            
            int prev = state[it.tx][it.ty];
            state[it.tx][it.ty] = state[it.sx][it.sy];
            state[it.sx][it.sy] = 0;

            int eval = minimax(lvl+1,alpha,beta,!is_max);

            state[it.sx][it.sy] = state[it.tx][it.ty];
            state[it.tx][it.ty] = prev;


            max_eval = max(max_eval,eval);

            if(lvl == 1 && eval>alpha)
            {
                next_move = it;
            }

            alpha = max(alpha,eval);
            if(beta<=alpha)
                break;
        }
        return max_eval;
    }
    else
    {
        int min_eval = INT_MAX;
        vector<move_info>valid_moves; 
        make_valid_moves(1,valid_moves);

        for(auto it:valid_moves)
        {
            int prev = state[it.tx][it.ty];
            state[it.tx][it.ty] = state[it.sx][it.sy];
            state[it.sx][it.sy] = 0;

            int eval = minimax(lvl+1,alpha,beta,!is_max);

            state[it.sx][it.sy] = state[it.tx][it.ty];
            state[it.tx][it.ty] = prev;

            min_eval = min(min_eval,eval);
            beta = min(beta,eval);
            if(beta<=alpha)
                break;
        }
        return min_eval;  
    }
}


void print_next_move()
{
    minimax(1,INT_MIN,INT_MAX,true);

    state[next_move.tx][next_move.ty] = state[next_move.sx][next_move.sy];
    state[next_move.sx][next_move.sy] = 0;

    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            cerr<<state[i][j]<<" ";
        }
        cerr<<endl;
    }
    cerr<<endl;
 
    
    cout<<next_move.sx<<endl;
    cout<<next_move.sy<<endl;
    cout<<next_move.tx<<endl;
    cout<<next_move.ty<<endl;
}


 


int main()
{
    string s;
    getline(cin,s);
    getline(cin,s);

    cin>>rows>>cols;

    create_board();

    int pp,qq,rr,ss;

    while(true)
    {
        cin>>pp>>qq>>rr>>ss;
        resolve_opponents_move(pp,qq,rr,ss);
        print_next_move();
         
    }

     
     
    return 0;
}