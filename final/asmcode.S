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

fun:

	pushl %ebp
	movl %esp, %ebp
	subl $0, %esp
	movl %ebp, %esp
	pop %ebp
	ret

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $16, %esp
	movl $4, -4(%ebp)
	movl %ebp, %edx
	addl $-8, %edx
	movl %edx, -12(%ebp)
	movl %ebp, %edx
	addl $-4, %edx
	movl %edx, -16(%ebp)
	pushl -8(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx

exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
