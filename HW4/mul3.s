        .globl  mul3
        
        .text
mul3:
        mov     %rdi, %rax                # result (rax) initially holds x
        imulq     %rsi, %rax              
        imulq   %rdx, %rax                
        ret                               