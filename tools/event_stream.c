// event_stream M START MAXSTEPS: run M from the blank tape; at each event (state C, head left of all nonzero cells)
// print m and the first 8 runs of S (tape 0 0 1^m 0 1^a1 0 1^a2 ...), or a note if the form differs.
#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; int q=v[2][0]-'A'; long long n=atoll(v[3]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<30; unsigned char*t=calloc(SZ,1); long p=SZ-(1L<<20); long first=SZ;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s);return 0;}
  t[p]=W[q][b]; if(W[q][b]&&p<first)first=p; p+=D[q][b]; q=N[q][b]; if(p<1||p>=SZ-1){printf("EDGE %lld\n",s);return 0;}
  if(q==2 && p<first){ while(!t[first])first++; if(p<first){
    long i=p+1; if(t[i]||t[i+1]){printf("E %lld form\n",s);continue;} i+=2; long m=0; while(t[i]){m++;i++;}
    printf("E %lld %ld",s,m); for(int k=0;k<8;k++){ if(t[i]) break; i++; long a=0; while(t[i]){a++;i++;} if(a==0 && !t[i]) { if(!t[i+1]&&!t[i+2]&&!t[i+3]) break; } printf(" %ld",a);} printf("\n"); } } }
 printf("MAX\n"); }
