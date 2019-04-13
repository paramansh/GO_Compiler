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
	subl $12, %esp
	movl $3, -8(%ebp)
	movl $4, -12(%ebp)
	movl -8(%ebp), %ecx
	movl -12(%ebp), %edx
	cmp %ecx, %edx
	je label0
	jmp label1

label0:

	movl $10, -8(%ebp)
	pushl -8(%ebp)
	pushl $outFormatInt
	call printf

label1:

	movl $5, -12(%ebp)
	movl -12(%ebp), %ecx
	neg %ecx
	movl %ecx, -16(%ebp)
	movl -16(%ebp), %edx
	movl %edx, -8(%ebp)

exit:

	pushl -8(%ebp)
	pushl $outFormatInt
	call printf
	movl $0, %ebx
	movl $1, %eax
	int $0x80
