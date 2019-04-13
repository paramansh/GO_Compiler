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

A:

	pushl %ebp
	movl %esp, %ebp
	subl $28, %esp
	movl 8(%ebp), %ecx
	movl $0, %edx
	cmp %ecx, %edx
	je label0
	jmp label1

label0:

	movl 12(%ebp), %edx
	addl $1, %edx
	movl %edx, -20(%ebp)
	movl -20(%ebp), %edx
	movl %edx, -4(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret

label1:

	movl 8(%ebp), %ecx
	movl $0, %edx
	cmp %ecx, %edx
	jl label2
	jmp label4

label2:

	movl 12(%ebp), %ecx
	movl $0, %edx
	cmp %ecx, %edx
	je label3
	jmp label4

label3:

	movl 8(%ebp), %edx
	subl $1, %edx
	movl %edx, -24(%ebp)
	pushl $1
	pushl -24(%ebp)
	call A
	movl -12(%esp), %edx
	movl %edx, -28(%ebp)
	addl $4, %esp
	movl -28(%ebp), %edx
	movl %edx, -4(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret

label4:

	movl 8(%ebp), %edx
	subl $1, %edx
	movl %edx, -4(%ebp)
	movl 12(%ebp), %edx
	subl $1, %edx
	movl %edx, -8(%ebp)
	pushl -8(%ebp)
	pushl 8(%ebp)
	call A
	movl -12(%esp), %edx
	movl %edx, -12(%ebp)
	addl $4, %esp
	pushl -12(%ebp)
	pushl -4(%ebp)
	call A
	movl -12(%esp), %edx
	movl %edx, -16(%ebp)
	addl $4, %esp
	movl -16(%ebp), %edx
	movl %edx, -4(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $20, %esp
	movl $0, -4(%ebp)

label10:

	movl -4(%ebp), %ecx
	movl $4, %edx
	cmp %ecx, %edx
	jg label11
	jmp label13

label11:

	movl $0, -12(%ebp)

label6:

	movl -12(%ebp), %ecx
	movl $5, %edx
	cmp %ecx, %edx
	jg label7
	jmp label9

label7:

	pushl -12(%ebp)
	pushl -4(%ebp)
	call A
	movl -12(%esp), %edx
	movl %edx, -20(%ebp)
	addl $4, %esp
	pushl -20(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx

label8:

	movl -12(%ebp), %edx
	addl $1, %edx
	movl %edx, -16(%ebp)
	movl -16(%ebp), %edx
	movl %edx, -12(%ebp)
	jmp label6

label9:


label12:

	movl -4(%ebp), %edx
	addl $1, %edx
	movl %edx, -8(%ebp)
	movl -8(%ebp), %edx
	movl %edx, -4(%ebp)
	jmp label10

label13:


exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
