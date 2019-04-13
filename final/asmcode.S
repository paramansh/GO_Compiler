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


__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $36, %esp
	movl $6, -20(%ebp)
	movl $0, -16(%ebp)
	movl $1, -8(%ebp)
	movl $0, -24(%ebp)

label0:

	movl -24(%ebp), %ecx
	movl -20(%ebp), %edx
	cmp %ecx, %edx
	jg label1
	jmp label3

label1:

	movl -8(%ebp), %ecx
	movl -16(%ebp), %edx
	addl %ecx, %edx
	movl %edx, -32(%ebp)
	movl -32(%ebp), %edx
	movl %edx, -12(%ebp)
	movl -8(%ebp), %edx
	movl %edx, -16(%ebp)
	movl -12(%ebp), %edx
	movl %edx, -8(%ebp)
	pushl -8(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx

label2:

	movl -24(%ebp), %edx
	addl $1, %edx
	movl %edx, -28(%ebp)
	movl -28(%ebp), %edx
	movl %edx, -24(%ebp)
	jmp label0

label3:


exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
