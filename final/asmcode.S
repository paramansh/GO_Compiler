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
	subl $12, %esp
	movl 8(%ebp), %ecx
	movl 12(%ebp), %edx
	addl %ecx, %edx
	movl %edx, -4(%ebp)
	movl -4(%ebp), %ecx
	movl 16(%ebp), %edx
	addl %ecx, %edx
	movl %edx, -8(%ebp)
	movl -8(%ebp), %ecx
	movl 20(%ebp), %edx
	addl %ecx, %edx
	movl %edx, -12(%ebp)
	movl -12(%ebp), %edx
	movl %edx, -4(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $20, %esp
	movl $2, -4(%ebp)
	subl $12, %esp
	movl %esp, -8(%ebp)
	movl -8(%ebp), %edx
	movl 8(%edx), %ecx
	movl %ecx, -12(%ebp)
	movl -8(%ebp), %edx
	movl $37, 8(%edx)
	pushl -4(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	movl $4, -16(%ebp)
	movl -4(%ebp), %ebx
	imul $4, %ebx
	addl -8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -20(%ebp)
	movl -20(%ebp), %edx
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
