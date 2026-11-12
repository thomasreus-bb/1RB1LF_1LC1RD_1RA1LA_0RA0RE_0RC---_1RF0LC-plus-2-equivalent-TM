// xmap M TAPE MAXSTEPS: mirrored machine A, start "head on the blank left of TAPE" in state C, TAPE = 0 0 1^m S;
// run to the next config with the head left of all nonzero cells in state C; print "X steps tape" or HALT/MAX
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; const char*T=v[2]; long long n=atoll(v[3]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<24; unsigned char*t=calloc(SZ,1); long p=SZ/4; long L=strlen(T); for(long i=0;i<L;i++) t[p+1+i]=T[i]-'0';
 int q=2; long lo=p,hi=p+L,first=p+1; while(first<=hi&&!t[first])first++;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s+1);return 0;} t[p]=W[q][b]; if(W[q][b]&&p<first)first=p;
  p+=D[q][b]; q=N[q][b]; if(p<lo)lo=p; if(p>hi)hi=p; if(p<2||p>SZ-3){printf("EDGE\n");return 0;}
  if(q==2 && p<first){ while(first<=hi&&!t[first])first++;
   if(p<first && s>0){ printf("X %lld ",s+1); long h=hi; while(h>p&&!t[h])h--; for(long i=p+1;i<=h;i++) putchar('0'+t[i]); putchar('\n'); return 0; } } }
 printf("MAX\n"); }
