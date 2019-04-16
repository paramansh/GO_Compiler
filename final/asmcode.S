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
	subl $20, %esp
	movl 8(%ebp), %ecx
	movl 12(%ebp), %edx
	cmp %ecx, %edx
	jl label0
	jmp label1

label0:

	movl 8(%ebp), %ecx
	movl 12(%ebp), %edx
	addl %ecx, %edx
	movl %edx, -16(%ebp)
	movl 12(%ebp), %edx
	movl %edx,-4(%ebp)
	movl -12(%ebp), %edx
	movl %edx,-8(%ebp)
	movl -16(%ebp), %edx
	movl %edx,-12(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret
	jmp label2

label1:

	movl 12(%ebp), %ecx
	movl 8(%ebp), %edx
	subl %edx, %ecx
	movl %ecx, -20(%ebp)
	movl 12(%ebp), %edx
	movl %edx,-4(%ebp)
	movl -12(%ebp), %edx
	movl %edx,-8(%ebp)
	movl -20(%ebp), %edx
	movl %edx,-12(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret

label2:


fun2:

	pushl %ebp
	movl %esp, %ebp
	subl $0, %esp
	movl 8(%ebp), %edx
	movl %edx, -4(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $44, %esp
	movl $2, -4(%ebp)
	movl $3, -8(%ebp)
	pushl -8(%ebp)
	pushl -4(%ebp)
	call fun
	movl -12(%esp), %edx
	movl %edx, -24(%ebp)
	movl -16(%esp), %edx
	movl %edx, -32(%ebp)
	movl -20(%esp), %edx
	movl %edx, -40(%ebp)
	addl $4, %esp
	movl -24(%ebp), %edx
	movl %edx, -12(%ebp)
	movl -32(%ebp), %edx
	movl %edx, -8(%ebp)
	movl -40(%ebp), %edx
	movl %edx, -16(%ebp)
	pushl -16(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	pushl -8(%ebp)
	pushl -4(%ebp)
	call fun2
	movl -12(%esp), %edx
	movl %edx, -44(%ebp)
	addl $4, %esp
	movl -44(%ebp), %edx
	movl %edx, -16(%ebp)
	pushl -16(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx

exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
