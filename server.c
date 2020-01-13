#include <iostream>
#include <stdlib.h>
#include <unistd.h>
#include <cstring>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <time.h>
#include <string>

#define BUF_SIZE 100
#define MAX_CLNT 256

void* handle_clnt(void* arg);
void send_msg(char* msg, int len);
void error_handling(char* msg);
void server_state(char* port);
int clnt_cnt = 0;
int clnt_socks[MAX_CLNT];
pthread_mutex_t mutx;

int main(int argc, char *argv[])
{
    // 서버 소켓과 클라이언트 소켓
    int serv_sock, clnt_sock;

    //Time log
    struct tm *timeLog;
    time_t timer = time(NULL);
    timeLog = localtime(&timer);

    // 서버의 주소와 클라이언트의 주소
    struct sockaddr_in serv_addr;
    struct sockaddr_in clnt_addr;
    socklen_t clnt_addr_size;
    // pthread 변수
    pthread_t t_id;
    
    server_state(argv[1]);

    if(argc != 2)
    {
        std::cout << "Usage : " << argv[0] << "<port>" << std::endl;
        exit(1);
    }
    // pthread의 초기화
    pthread_mutex_init(&mutx, NULL);
    // 소켓 연결, 디스크립터라고 하며, 소켓을 생성하면 지정된 숫자를 serv_sock으로 넘겨준다.
    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    // 소켓의 생성을 확인
    if(serv_sock == -1)
        error_handling("socket() error!");

    // 구조체 변수를 저장하기 위해 앞서 serv_addr을 0으로 초기화
    memset(&serv_addr, 0, sizeof(serv_addr));
    // IP주소와 port번호를 할당
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(atoi(argv[1]));

    // 소켓 정보를 bind에 전달, bind에 주소 정보 할당
    if(bind(serv_sock,(struct sockaddr*) &serv_addr, sizeof(serv_addr)) == -1)
        error_handling("bind() error!");
    
    // 소켓을 받아들일 수 있는 상태로 만듦
    if(listen(serv_sock, 5) == -1)
    error_handling("Listen() error!");

    /*
    // accept함수로 누가 연결(전화)를 걸면 값을 반환하여 체크
    clnt_addr_size = sizeof(cint_addr);
    clnt_sock = accept(serv_sock, (struct sockaddr*)&cint_addr, &cint_addr_size);
    if(clnt_sock == -1)
        error_handling("accept() error!");  
    */

    while(1)
    {
        timeLog = localtime(&timer);
        // accept함수로 누가 연결을 걸면 값을 반환하여 체크
        clnt_addr_size = sizeof(clnt_addr);
        clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr,&clnt_addr_size);
        if(clnt_sock == -1)
            error_handling("accept() error!");
        // Critical Section 시작
        pthread_mutex_lock(&mutx);
        clnt_socks[clnt_cnt++] = clnt_sock;
        // Critical Section 종료
        pthread_mutex_unlock(&mutx);

        // 쓰레드 생성
        pthread_create(&t_id, NULL, handle_clnt,(void*)&clnt_sock);
        // 쓰레드 분리
        pthread_detach(t_id);
        std::cout << "Connected client IP : " << inet_ntoa(clnt_addr.sin_addr);
        std::cout << "(" << timeLog->tm_year+1900 << "-" 
        << timeLog->tm_mon + 1 << "-" << timeLog->tm_mday << "-" 
        << timeLog->tm_hour << "-" << timeLog->tm_min << ")" <<  std::endl;
        std::cout << "chatter (" << clnt_cnt << "/" << MAX_CLNT << ")\n";
    }
    close(serv_sock);
    return 0;
}

void server_state(char* port)
{
    using std::cout;
    using std::endl;
    using std::string;
    cout << "Server Port : " << port << endl;
    cout << "Server State : " << clnt_cnt << " / " << MAX_CLNT << endl;
    cout << endl;
}


void* handle_clnt(void* arg)
{        
    int clnt_sock=*((int*)arg);
    int str_len=0,i;
    char msg[BUF_SIZE];

    while((str_len=read(clnt_sock, msg, sizeof(msg)))!=0)
        send_msg(msg, str_len);

    pthread_mutex_lock(&mutx);
    for(i=0; i<clnt_cnt; i++) //remove disconnected client
    {
        if(clnt_sock==clnt_socks[i])
        {
            while(i++<clnt_cnt-1)
                clnt_socks[i]=clnt_socks[i+1];
            break;
        }
    }
    clnt_cnt--;
    pthread_mutex_unlock(&mutx);
    close(clnt_sock);
    return NULL;
}

void send_msg(char *msg, int len) // send to all
{
        int i;
        pthread_mutex_lock(&mutx);
        for(i=0; i<clnt_cnt; i++)
                write(clnt_socks[i], msg, len);
        pthread_mutex_unlock(&mutx);
}
void error_handling(char* msg)
{
        fputs(msg, stderr);
        fputc('\n', stderr);
        exit(1);
}
