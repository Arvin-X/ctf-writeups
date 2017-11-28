#include <iostream>
#include <fstream>

// key: #7Fn@(2A

int check_size(std::string &key) __attribute((__annotate__(("nofla")))) __attribute((__annotate__(("nosub")))) __attribute((__annotate__(("nobcf"))));
int check_first_char(char c) __attribute((__annotate__(("nofla")))) __attribute((__annotate__(("nosub")))) __attribute((__annotate__(("nobcf"))));

int check_size(std::string &key) {
    if (key.size() != 8)
        return 1;
    return 0;
}

int check_first_char(char c) {
    c += 2;
    c ^= 0x14;
    c -= 20;
    c ^= 0x2f;
    // std::cout << std::showbase << std::hex;
    // std::cout << "0: " << static_cast<short>(c) << std::endl;
    if (c != 0x32) 
        return 1;
    return 0;
}


int main() {
    std::string key;
    unsigned char c;
    int i, j;

    std::cout << "Show me the right key and I will give you the flag." << std::endl;
    std::cin >> key;

    if (check_size(key))
        return -1;

    // 0
    if (check_first_char(key[0]))
        return -1;

    // 1
    c = key[1];
    for (i = 0; i < 4; i++) {
        c <<= 1;
        c += 0x9;
        c &= 0xef;
        c >>= 1;
        c -= 0x2;
    }
    // std::cout << "1: " << static_cast<short>(c) << std::endl;
    if (c != 0x2f) 
        return -1;

    // 2
    c = key[2];
    for (i = 0; i < 4; i++) {
        c += 6;
        c <<= 1;
        c ^= 0x13;
        c >>= 1;
        for (j = 0; j < 2; j++) {
            c -= 4;
            c ^= 0x24;
            c += 2;
        }
    }
    // std::cout << "2: " << static_cast<short>(c) << std::endl;
    if (c != 0x2e)
        return -1;

    // 3
    c = key[3];
    for (i = 0; i < 4; i++) {
        c <<= 1;
        c ^= 0x38;
        c >> 2;
        c += 2;
        for (j = 0; j < 4; j++) {
            c -= 4;
            c &= 0x2f;
        }
        c >>= 1;
    }
    // std::cout << "3: " << static_cast<short>(c) << std::endl;
    if (c != 0x12)
        return -1;

    // 4
    c = key[4];
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 4; j++) {
            c -= 6;
            c <<= 1;
            c += 0x23;
            c >>= 1;
        }
        c <<= 2;
        c |= 0x2;
        c >>= 2;
        c >> 3;
        c += 1;
    }
    // std::cout << "4: " << static_cast<short>(c) << std::endl;
    if (c != 0x1a)
        return -1;

    // 5
    c = key[5];
    for (i = 0; i < 4; i++) {
        c <<= 1;
        c += 5;
        c >>= 1;
        c << 2;
        for (j = 0; j < 4; j++) {
            c -= 5;
            c ^= 0x33;
            c += 1;
        }
    }
    // std::cout << "5: " << static_cast<short>(c) << std::endl;
    if (c != 0x30)
        return -1;

    // 6
    c = key[6];
    for (i = 0; i < 4; i++) {
        c <<= 1;
        c ^= 0x22;
        c += 3;
        c += 0x23;
        for (j = 0; j < 2; j++) {
            c -= 4;
            c |= 0x11;
            c += 0x15;
        }
        c >>= 1;
    }
    // std::cout << "6: " << static_cast<short>(c) << std::endl;
    if (c != 0x3a)
        return -1;

    // 7
    c = key[7];
    for (i = 0; i < 4; i++) {
        for (j = 0; j < 2; j++) {
            c -= 4;
            c ^= 0x27;
            c -= 7;
        }
        c <<= 1;
        c += 0x80;
        c &= 0x75;
        c >>= 1;
    }
    // std::cout << "7: " << static_cast<short>(c) << std::endl;
    if (c != 0x30)
        return -1;

    std::cout << "Congratulations" << std::endl;
    std::ifstream ifs("./flag");
    if (ifs.is_open()) {
        std::cout << ifs.rdbuf() << std::endl;
    }

    return 0;
}
