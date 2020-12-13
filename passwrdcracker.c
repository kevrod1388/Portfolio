#include<string.h>
#include<stdlib.h>
#include<stdio.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include<openssl/des.h>


int main() {
    
    // open file to decrypt
    
    int fdp=open("secret.pdf.enc1", O_RDONLY);
    
    if(fdp )

    // open file with contents "%PDF-1.X" to try to revese the key
    int fdc = open("key.txt", O_RDONLY);
    // read the first 8 bytes
    
    unsigned long long buf;
    read(fdp, (char*)&buf, 8);
    
    unsigned long long k;
    read(fdc, (char*)&k, 8);
    
    unsigned long long key = buf ^ k;

    printf("%llx \n",buf);
    printf("%x \n",key);
    
    close(fdp);
    close(fdc);
    
    
    
    
}


