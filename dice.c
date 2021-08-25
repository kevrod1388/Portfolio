
#include<stdlib.h>
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>
#define NUM_THREADS 5

// link pthreads library in compiler settings->linker settings "-pthread"

pthread_mutex_t     mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t      Dealer  = PTHREAD_COND_INITIALIZER;
pthread_cond_t      PlayerA  = PTHREAD_COND_INITIALIZER;
pthread_cond_t      PlayerB  = PTHREAD_COND_INITIALIZER;
pthread_cond_t      PlayerC  = PTHREAD_COND_INITIALIZER;
pthread_cond_t      PlayerD  = PTHREAD_COND_INITIALIZER;

enum { BeforeGame, Running, GameOver } state = BeforeGame;

int whoWon = -1;
int TeamBDSum = 0;
int TeamACSum = 0;

int PlayerAReady = 0;
int PlayerBReady = 0;
int PlayerCReady = 0;
int PlayerDReady = 0;
FILE *logg;
int test= 400;

int roll_dice();
//void pthread_exit();
//int pthread_join(pthread_t thread, void ** thread_return);
void *thread_A(void * par);
void *thread_B(void * par);
void *thread_C(void * par);
void *thread_D(void * par);
void *thread_Dealer(void * par);


void *thread_A(void * par){

 while (1) {

         //lock mutex variable
        pthread_mutex_lock(&mutex);

        if (!PlayerAReady)
            pthread_cond_wait(&PlayerA, &mutex);
        PlayerAReady = 0;
        pthread_mutex_unlock(&mutex);


        if (state == GameOver)
            break;

        //call roll_dice
        int dice1 = roll_dice();
        int dice2 = roll_dice();

        int sum = dice1 + dice2;

        fprintf(logg, "Player A rolled %d, %d Sum: (%d)\n", dice1, dice2, sum);
        printf("Player A rolled %d, %d\n", dice1, dice2);

        //if sums match print winner
        if (sum == TeamACSum) {
            state = GameOver;
            whoWon = 1;

            printf("Team AC won!");
            pthread_mutex_lock(&mutex);
            pthread_cond_signal(&Dealer);
            pthread_mutex_unlock(&mutex);
            break;
        }

        TeamACSum = sum;

        //lock mutex again
        pthread_mutex_lock(&mutex);
        PlayerBReady = 1;
        pthread_cond_signal(&PlayerB);
        pthread_mutex_unlock(&mutex);
    }

    return NULL;
}

void *thread_B(void * par){

    while (1) {
        pthread_mutex_lock(&mutex);

        if (!PlayerBReady)
            pthread_cond_wait(&PlayerB, &mutex);

        PlayerBReady = 0;
        pthread_mutex_unlock(&mutex);

        if (state == GameOver)
            break;

        int dice1 = roll_dice();
        int dice2 = roll_dice();

        int sum = dice1 + dice2;


        fprintf(logg, "Player B rolled %d, %d Sum: (%d)\n", dice1, dice2, sum);
        printf("Player B rolled %d, %d\n", dice1, dice2);


        if (sum == TeamBDSum) {
            state = GameOver;
            whoWon = 2;

            printf("Team BD won!\n");

            pthread_mutex_lock(&mutex);
            pthread_cond_signal(&Dealer);
            pthread_mutex_unlock(&mutex);
            break;
        }

        TeamBDSum = sum;

        pthread_mutex_lock(&mutex);
        PlayerCReady = 1;
        pthread_cond_signal(&PlayerC);
        pthread_mutex_unlock(&mutex);
    }

    return NULL;
}

void *thread_C(void * par){

   while (1) {

        pthread_mutex_lock(&mutex);

        if (!PlayerCReady)
            pthread_cond_wait(&PlayerC, &mutex);

        PlayerCReady = 0;
        pthread_mutex_unlock(&mutex);


        if (state == GameOver)
            break;


        int dice1 = roll_dice();
        int dice2 = roll_dice();

        int sum = dice1 + dice2;


        fprintf(logg, "Player C rolled %d, %d Sum: (%d)\n", dice1, dice2, sum);
        printf("Player C rolled %d, %d\n", dice1, dice2);


        if (sum == TeamACSum) {
            state = GameOver;
            whoWon = 1;

            printf("Team AC won!\n");

            pthread_mutex_lock(&mutex);
            pthread_cond_signal(&Dealer);
            pthread_mutex_unlock(&mutex);
            break;
        }

        TeamACSum = sum;

        pthread_mutex_lock(&mutex);
        PlayerDReady = 1;
        pthread_cond_signal(&PlayerD);
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

void *thread_D(void * par){

     while (1) {
        pthread_mutex_lock(&mutex);

        if (!PlayerDReady)
            pthread_cond_wait(&PlayerD, &mutex);
        PlayerDReady = 0;

        pthread_mutex_unlock(&mutex);


        if (state == GameOver)
            break;



        int dice1 = roll_dice();
        int dice2 = roll_dice();

        int sum = dice1 + dice2;


        fprintf(logg, "Player D rolled %d, %d Sum: (%d)\n", dice1, dice2, sum);
        printf("Player D rolled %d, %d\n", dice1, dice2);


        if (sum == TeamBDSum) {
            state = GameOver;
            whoWon = 2;

            printf("Team BD won!\n");

            pthread_mutex_lock(&mutex);
            pthread_cond_signal(&Dealer);
            pthread_mutex_unlock(&mutex);
            break;
        }

        TeamBDSum = sum;

        pthread_mutex_lock(&mutex);
        PlayerAReady = 1;
        pthread_cond_signal(&PlayerA);
        pthread_mutex_unlock(&mutex);
    }

    return NULL;
}

void *thread_Dealer(void * par){

// pick "random" player to start gam

    int player = rand() % 4 + 1;
    //                            012345
    printf("Player %c starts\n", " ABCD"[player]);


// signal chosen player to start (lock mutex, signal, unlock)
    pthread_mutex_lock(&mutex);
    switch(player) {
    case 1:
        PlayerAReady = 1;
        pthread_cond_signal(&PlayerA);
        break;
    case 2:
        PlayerBReady = 1;
        pthread_cond_signal(&PlayerB);
        break;
    case 3:
        PlayerCReady = 1;
        pthread_cond_signal(&PlayerC);
        break;
    case 4:
        PlayerDReady = 1;
        pthread_cond_signal(&PlayerD);
        break;
    }
    pthread_mutex_unlock(&mutex);

    printf("Dealer started the game\n");

// wait for winning team (lock mutex, wait, unlock)
    pthread_mutex_lock(&mutex);

    if (whoWon == -1)
        pthread_cond_wait(&Dealer, &mutex);  // unlock .. lock

    pthread_mutex_unlock(&mutex);

// wake up all players with state at GameOver
    pthread_mutex_lock(&mutex);
    PlayerAReady = 1;
    pthread_cond_signal(&PlayerA);
    pthread_mutex_unlock(&mutex);

    pthread_mutex_lock(&mutex);
    PlayerBReady = 1;
    pthread_cond_signal(&PlayerB);
    pthread_mutex_unlock(&mutex);

    pthread_mutex_lock(&mutex);
    PlayerCReady = 1;
    pthread_cond_signal(&PlayerC);
    pthread_mutex_unlock(&mutex);

    pthread_mutex_lock(&mutex);
    PlayerDReady = 1;
    pthread_cond_signal(&PlayerD);
    pthread_mutex_unlock(&mutex);

    return NULL;
}


int roll_dice(){
 return rand() % 6 + 1;
}



int main(){
    logg = fopen("logfile.txt" , "w"); // fopen("name.txt", "w");
    if(logg == NULL){
       printf("Could not open logfile.txt\n");
       logg = stdout;
    }

    srand(time(NULL));
    pthread_t A;
    pthread_t B;
    pthread_t C;
    pthread_t D;
    pthread_t Dlr;

   int err = pthread_create(&Dlr, NULL, &thread_Dealer, 0);
   err = pthread_create(&A, NULL, &thread_A, 0);
   err = pthread_create(&B, NULL, &thread_B, 0); //(void *) 2);
   err = pthread_create(&C, NULL, &thread_C, 0);
   err = pthread_create(&D, NULL, &thread_D, 0);

  pthread_join(A, NULL);
  pthread_join(B, NULL);
  pthread_join(C, NULL);
  pthread_join(D, NULL);
  pthread_join(Dlr, NULL);

  return 0;

}
