	.file	"asm2.c"
	.text
	.section	.rodata
.LC0:
	.string	" "
.LC1:
	.string	"%d\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$5552, %rsp
	movq	$0, -128(%rbp)
	movq	$0, -120(%rbp)
	movq	$0, -112(%rbp)
	movq	$0, -104(%rbp)
	movq	$0, -96(%rbp)
	movq	$0, -88(%rbp)
	movq	$0, -80(%rbp)
	movq	$0, -72(%rbp)
	movq	$0, -64(%rbp)
	movq	$0, -56(%rbp)
	movq	$0, -48(%rbp)
	movq	$0, -40(%rbp)
	movl	$0, -32(%rbp)
	movq	stdin(%rip), %rdx
	leaq	-128(%rbp), %rax
	movl	$100, %esi
	movq	%rax, %rdi
	call	fgets@PLT
	leaq	-128(%rbp), %rax
	movq	%rax, %rdi
	call	atoi@PLT
	movl	%eax, -24(%rbp)
	leaq	-544(%rbp), %rdx
	movl	$0, %eax
	movl	$50, %ecx
	movq	%rdx, %rdi
	rep stosq
	movq	%rdi, %rdx
	movl	%eax, (%rdx)
	addq	$4, %rdx
	movq	$0, -5552(%rbp)
	movq	$0, -5544(%rbp)
	leaq	-5536(%rbp), %rdx
	movl	$0, %eax
	movl	$623, %ecx
	movq	%rdx, %rdi
	rep stosq
	movq	stdin(%rip), %rdx
	leaq	-5552(%rbp), %rax
	movl	$5000, %esi
	movq	%rax, %rdi
	call	fgets@PLT
	leaq	-5552(%rbp), %rax
	leaq	.LC0(%rip), %rsi
	movq	%rax, %rdi
	call	strtok@PLT
	movq	%rax, -8(%rbp)
	movl	$0, -12(%rbp)
	jmp	.L2
.L5:
	cmpq	$0, -8(%rbp)
	je	.L9
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	call	atoi@PLT
	movslq	%eax, %rdx
	movl	-544(%rbp,%rdx,4), %edx
	addl	$1, %edx
	cltq
	movl	%edx, -544(%rbp,%rax,4)
	leaq	.LC0(%rip), %rsi
	movl	$0, %edi
	call	strtok@PLT
	movq	%rax, -8(%rbp)
	addl	$1, -12(%rbp)
.L2:
	movl	-12(%rbp), %eax
	cmpl	-24(%rbp), %eax
	jl	.L5
	jmp	.L4
.L9:
	nop
.L4:
	movl	$0, -16(%rbp)
	movl	$1, -20(%rbp)
	jmp	.L6
.L7:
	movl	-20(%rbp), %eax
	cltq
	movl	-544(%rbp,%rax,4), %eax
	cmpl	%eax, -16(%rbp)
	cmovge	-16(%rbp), %eax
	movl	%eax, -16(%rbp)
	addl	$1, -20(%rbp)
.L6:
	cmpl	$100, -20(%rbp)
	jle	.L7
	movl	-16(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC1(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.ident	"GCC: (Debian 10.2.1-6) 10.2.1 20210110"
	.section	.note.GNU-stack,"",@progbits
