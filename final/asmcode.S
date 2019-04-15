.data

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

fun:

	pushl %ebp
	movl %esp, %ebp
	subl $4, %esp
	movl 8(%ebp), %edx
	movl 56(%edx), %ecx
	movl %ecx, -4(%ebp)
	pushl -4(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $44, %esp
	movl $5, -4(%ebp)
	movl $4, -8(%ebp)
	movl $4, %edx
	movl -8(%ebp), %ecx
	imul %ecx, %edx
	movl %edx, -12(%ebp)
	movl -12(%ebp), %edx
	imul $4, %edx
	subl %edx, %esp
	movl %esp, -16(%ebp)
	movl $3, %edx
	movl -8(%ebp), %ecx
	imul %ecx, %edx
	movl %edx, -24(%ebp)
	movl -24(%ebp), %edx
	addl $2, %edx
	movl %edx, -28(%ebp)
	movl -28(%ebp), %ebx
	imul $4, %ebx
	addl -16(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -20(%ebp)
	movl -28(%ebp), %ebx
	imul $4, %ebx
	addl -16(%ebp), %ebx
	movl $4, (%ebx)
	movl $3, %edx
	movl -8(%ebp), %ecx
	imul %ecx, %edx
	movl %edx, -36(%ebp)
	movl -36(%ebp), %edx
	addl $2, %edx
	movl %edx, -40(%ebp)
	movl -40(%ebp), %ebx
	imul $4, %ebx
	addl -16(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -32(%ebp)
	movl -32(%ebp), %edx
	movl %edx, -44(%ebp)
	pushl -44(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	pushl -16(%ebp)
	call fun
	addl $4, %esp

exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
