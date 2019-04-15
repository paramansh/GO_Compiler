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
	movl $0, -4(%ebp)

label0:

	movl -4(%ebp), %ecx
	movl $5, %edx
	cmp %ecx, %edx
	jg label1
	jmp label3

label1:

	movl -4(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -12(%ebp)
	movl -4(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl -4(%ebp), %ecx
	movl %ecx, (%ebx)

label2:

	movl -4(%ebp), %edx
	addl $1, %edx
	movl %edx, -8(%ebp)
	movl -8(%ebp), %edx
	movl %edx, -4(%ebp)
	jmp label0

label3:

	movl %ebp, %esp
	pop %ebp
	ret

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $20, %esp
	movl $5, -4(%ebp)
	movl -4(%ebp), %edx
	imul $4, %edx
	subl %edx, %esp
	movl %esp, -8(%ebp)
	pushl -8(%ebp)
	call fun
	addl $4, %esp
	movl $0, -12(%ebp)

label5:

	movl -12(%ebp), %ecx
	movl $5, %edx
	cmp %ecx, %edx
	jg label6
	jmp label8

label6:

	movl -12(%ebp), %ebx
	imul $4, %ebx
	addl -8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -20(%ebp)
	pushl -20(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx

label7:

	movl -12(%ebp), %edx
	addl $1, %edx
	movl %edx, -16(%ebp)
	movl -16(%ebp), %edx
	movl %edx, -12(%ebp)
	jmp label5

label8:


exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
