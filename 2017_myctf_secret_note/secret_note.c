#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>


struct note_item {
    long content;
    unsigned long size;
};

long key;
struct note_item note[8];

unsigned int read_wrapper(char* buf, unsigned int size) {
    char c;
    unsigned int i = 0;

    while((c = getchar()) != '\n' && c != EOF && i < size) {
        buf[i++] = c;
    }
    return i;
}

unsigned int get_index() {
    char c;
    read_wrapper(&c, 1);
    return (unsigned int)(c - 48);
}

void main_menu() {
    puts("Secret note");
    puts("1. create new note");
    puts("2. edit note");
    puts("3. list note");
    puts("4. delete note");
    puts("5. exit");
    return;
}

void create() {
    unsigned int index;
    unsigned int count;
    char buf[20];

    puts("input index");
    index = get_index();
    if (index < 0 || index > 8) {
        puts("invalid index");
        return;
    }
    if (note[index].content) {
        puts("this item has been used");
        return;
    }
    puts("input size");
    read_wrapper(buf, 20);
    note[index].size = atol(buf);
    note[index].content = (long)malloc(note[index].size);

    puts("now input your secret");
    count = read_wrapper((char *)(note[index].content), note[index].size);
    ((char *)(note[index].content))[count] = '\0';
    note[index].content ^= key;
    puts("note added");
    return;
}

void edit() {
    unsigned int index;
    unsigned int count;

    puts("input index");
    index = get_index();
    if (index < 0 || index > 8) {
        puts("invalid index");
        return;
    }
    if (!note[index].content) {
        puts("this item is unused");
        return;
    }
    puts("now you can edit your secret");
    count = read_wrapper((char *)(note[index].content ^ key), note[index].size);
    ((char *)(note[index].content ^ key))[count] = '\0';
    puts("edited");
    return;
}

void list() {
    int i;

    for(i = 0; i < 10; i++) {
        if(note[i].content) {
            printf("%d. size: %ld\n", i, note[i].size );     
            printf("   content: **********************\n");
        }
    }
    return;
}

void delete() {
    unsigned int index;
    
    puts("input index of the note you want to delete");
    index = get_index();
    if (index < 0 || index > 8) {
        puts("invalid index");
        return;
    }
    if (note[index].content) {
        free((void *)(note[index].content ^ key));
        note[index].content = 0;
    } else {
        puts("can not delete unused item");
    }
    puts("deleted");
    return;
            
}

int main() {
    char c;
    int fd;

    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    fd = open("/dev/urandom", O_RDONLY);
    read(fd, &key, 8);
    close(fd);

    while(1) {
        main_menu();
        putchar('>');
        read_wrapper(&c, 1);
        switch (c) {
            case '1': create(); break;
            case '2': edit(); break;
            case '3': list(); break;
            case '4': delete(); break;
            case '5': exit(0); break;
            default:
                puts("invalid input");
                break;
        } 
    }

    return 0;
}
