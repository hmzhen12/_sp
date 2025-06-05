## 0326.c

執行0326.c
```
 gcc 0326.c
 ./a.exe
```
產生組合語言.s檔
```
gcc -S 0326.c
```

產生目的檔.o檔
```
gcc -c 0326.c
```
將該目的檔反組譯
```
objdump -d 0326.o
```
```sh
0326.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <mul2>:
   0:   55                      push   %rbp
   1:   48 89 e5                mov    %rsp,%rbp
   4:   89 4d 10                mov    %ecx,0x10(%rbp)        
   7:   89 55 18                mov    %edx,0x18(%rbp)
   a:   8b 45 10                mov    0x10(%rbp),%eax        
   d:   0f af 45 18             imul   0x18(%rbp),%eax        
  11:   5d                      pop    %rbp
  12:   c3                      retq

0000000000000013 <main>:
  13:   55                      push   %rbp
  14:   48 89 e5                mov    %rsp,%rbp
  17:   48 83 ec 20             sub    $0x20,%rsp
  1b:   e8 00 00 00 00          callq  20 <main+0xd>
  20:   ba 02 00 00 00          mov    $0x2,%edx
  25:   b9 05 00 00 00          mov    $0x5,%ecx
  2a:   e8 d1 ff ff ff          callq  0 <mul2>
  2f:   89 c2                   mov    %eax,%edx
  31:   48 8d 0d 00 00 00 00    lea    0x0(%rip),%rcx        # 38 <main+0x25>
  38:   e8 00 00 00 00          callq  3d <main+0x2a>
  3d:   b8 00 00 00 00          mov    $0x0,%eax
  42:   48 83 c4 20             add    $0x20,%rsp
  46:   5d                      pop    %rbp
  47:   c3                      retq
  48:   90                      nop
  49:   90                      nop
  4a:   90                      nop
  4b:   90                      nop
  4c:   90                      nop
  4d:   90                      nop
  4e:   90                      nop
  4f:   90                      nop
```
印出該目的檔的表頭
```
objdump -h 0326.o
```
```sh
0326.o:     file format pe-x86-64

Sections:
Idx Name          Size      VMA               LMA             
  File off  Algn
  0 .text         00000050  0000000000000000  0000000000000000  0000012c  2**4
                  CONTENTS, ALLOC, LOAD, RELOC, READONLY, CODE
  1 .data         00000000  0000000000000000  0000000000000000  00000000  2**4
                  ALLOC, LOAD, DATA
  2 .bss          00000000  0000000000000000  0000000000000000  00000000  2**4
                  ALLOC
  3 .xdata        00000014  0000000000000000  0000000000000000  0000017c  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA       
  4 .pdata        00000018  0000000000000000  0000000000000000  00000190  2**2
                  CONTENTS, ALLOC, LOAD, RELOC, READONLY, DATA
  5 .rdata        00000010  0000000000000000  0000000000000000  000001a8  2**4
                  CONTENTS, ALLOC, LOAD, READONLY, DATA       
  6 .rdata$zzz    00000040  0000000000000000  0000000000000000  000001b8  2**4
                  CONTENTS, ALLOC, LOAD, READONLY, DATA   
```

