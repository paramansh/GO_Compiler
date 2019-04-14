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

sort:

	pushl %ebp
	movl %esp, %ebp
	subl $68, %esp
	movl $0, -8(%ebp)

label6:

	movl 12(%ebp), %edx
	subl $1, %edx
	movl %edx, -12(%ebp)
	movl -8(%ebp), %ecx
	movl -12(%ebp), %edx
	cmp %ecx, %edx
	jg label7
	jmp label9

label7:

	movl $0, -4(%ebp)

label2:

	movl 12(%ebp), %ecx
	movl -8(%ebp), %edx
	subl %edx, %ecx
	movl %ecx, -20(%ebp)
	movl -20(%ebp), %edx
	subl $1, %edx
	movl %edx, -24(%ebp)
	movl -4(%ebp), %ecx
	movl -24(%ebp), %edx
	cmp %ecx, %edx
	jg label3
	jmp label5

label3:

	movl -4(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -32(%ebp)
	movl -4(%ebp), %edx
	addl $1, %edx
	movl %edx, -36(%ebp)
	movl -36(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -40(%ebp)
	movl -32(%ebp), %ecx
	movl -40(%ebp), %edx
	cmp %ecx, %edx
	jl label0
	jmp label1

label0:

	movl -4(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -44(%ebp)
	movl -44(%ebp), %edx
	movl %edx, -48(%ebp)
	movl -4(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -52(%ebp)
	movl -4(%ebp), %edx
	addl $1, %edx
	movl %edx, -56(%ebp)
	movl -56(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -60(%ebp)
	movl -4(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl -60(%ebp), %ecx
	movl %ecx, (%ebx)
	movl -4(%ebp), %edx
	addl $1, %edx
	movl %edx, -64(%ebp)
	movl -64(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -68(%ebp)
	movl -64(%ebp), %ebx
	imul $4, %ebx
	addl 8(%ebp), %ebx
	movl -48(%ebp), %ecx
	movl %ecx, (%ebx)

label1:


label4:

	movl -4(%ebp), %edx
	addl $1, %edx
	movl %edx, -28(%ebp)
	movl -28(%ebp), %edx
	movl %edx, -4(%ebp)
	jmp label2

label5:


label8:

	movl -8(%ebp), %edx
	addl $1, %edx
	movl %edx, -16(%ebp)
	movl -16(%ebp), %edx
	movl %edx, -8(%ebp)
	jmp label6

label9:

	movl %ebp, %esp
	pop %ebp
	ret

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $36, %esp
	subl $20, %esp
	movl %esp, -4(%ebp)
	movl $0, -8(%ebp)

label11:

	movl -8(%ebp), %ecx
	movl $5, %edx
	cmp %ecx, %edx
	jg label12
	jmp label14

label12:

	movl -8(%ebp), %ebx
	imul $4, %ebx
	addl -4(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -16(%ebp)
	movl $5, %edx
	movl -8(%ebp), %ecx
	subl %ecx, %edx
	movl %edx, -20(%ebp)
	movl -8(%ebp), %ebx
	imul $4, %ebx
	addl -4(%ebp), %ebx
	movl -20(%ebp), %ecx
	movl %ecx, (%ebx)
	movl -8(%ebp), %ebx
	imul $4, %ebx
	addl -4(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -24(%ebp)
	pushl -24(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx

label13:

	movl -8(%ebp), %edx
	addl $1, %edx
	movl %edx, -12(%ebp)
	movl -12(%ebp), %edx
	movl %edx, -8(%ebp)
	jmp label11

label14:

	pushl $5
	pushl -4(%ebp)
	call sort
	addl $8, %esp
	movl $0, -28(%ebp)

label15:

	movl -28(%ebp), %ecx
	movl $5, %edx
	cmp %ecx, %edx
	jg label16
	jmp label18

label16:

	movl -28(%ebp), %ebx
	imul $4, %ebx
	addl -4(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -36(%ebp)
	pushl -36(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx

label17:

	movl -28(%ebp), %edx
	addl $1, %edx
	movl %edx, -32(%ebp)
	movl -32(%ebp), %edx
	movl %edx, -28(%ebp)
	jmp label15

label18:


exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
