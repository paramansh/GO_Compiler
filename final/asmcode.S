.data

blank:
	.int	0
outFormatInt:
	.asciz	"%d\n"
outFormatStr:
	.asciz	"%s\n"
inFormat:
	.ascii	"%d"

.text

.global main

main:

	call __main__
	jmp exit

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $52, %esp
	movl $3, -16(%ebp)
	movl -24(%ebp), %edx
	movl 136(%edx), %ecx
	movl %ecx, -32(%ebp)
	movl -36(%ebp), %edx
	movl %edx, -16(%ebp)
	movl $0, -40(%ebp)
	movl $0, -44(%ebp)
	movl %ebp, %edx
	addl $-16, %edx
	movl %edx, -48(%ebp)
	movl -48(%ebp), %edx
	movl (%edx), %ecx
	movl %ecx, -52(%ebp)
	movl -48(%ebp), %edx
	movl $4, (%edx)
	pushl -16(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx

exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
