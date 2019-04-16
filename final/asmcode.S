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
	subl $48, %esp
	subl $4, %esp
	movl %esp ,-8(%ebp)
	subl $4, %esp
	movl -8(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -16(%ebp)
	movl -8(%ebp), %edx
	subl $0, %edx
	movl $-1, (%edx)
	movl -8(%ebp), %edx
	movl %edx, -12(%ebp)
	movl -8(%ebp), %edx
	movl %edx, -4(%ebp)
	movl $0, -24(%ebp)

label0:

	movl -24(%ebp), %ecx
	movl $5, %edx
	cmp %ecx, %edx
	jg label1
	jmp label3

label1:

	subl $4, %esp
	movl %esp ,-8(%ebp)
	subl $4, %esp
	movl -8(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -32(%ebp)
	movl -8(%ebp), %edx
	subl $0, %edx
	movl -24(%ebp), %ecx
	movl %ecx, (%edx)
	movl -8(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -36(%ebp)
	movl -8(%ebp), %edx
	subl $4, %edx
	movl $0, (%edx)
	movl -4(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -40(%ebp)
	movl -4(%ebp), %edx
	subl $4, %edx
	movl -8(%ebp), %ecx
	movl %ecx, (%edx)
	movl -8(%ebp), %edx
	movl %edx, -4(%ebp)

label2:

	movl -24(%ebp), %edx
	addl $1, %edx
	movl %edx, -28(%ebp)
	movl -28(%ebp), %edx
	movl %edx, -24(%ebp)
	jmp label0

label3:

	movl $-10, -20(%ebp)
	movl -12(%ebp), %edx
	movl %edx, -8(%ebp)

label6:

	movl -8(%ebp), %ecx
	movl $0, %edx
	cmp %ecx, %edx
	jne label7
	jmp label8

label7:

	movl -8(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -44(%ebp)
	movl -44(%ebp), %ecx
	movl -20(%ebp), %edx
	cmp %ecx, %edx
	je label4
	jmp label5

label4:

	movl $1, %edx
	pushl %edx
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	jmp label8

label5:

	movl -8(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -48(%ebp)
	movl -48(%ebp), %edx
	movl %edx, -8(%ebp)
	jmp label6

label8:


exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
