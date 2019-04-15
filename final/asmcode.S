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

is_even:

	pushl %ebp
	movl %esp, %ebp
	subl $8, %esp
	movl 8(%ebp), %ecx
	movl $0, %edx
	cmp %ecx, %edx
	je label0
	jmp label1

label0:

	movl $1, %edx
	movl %edx, -4(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret
	jmp label2

label1:

	movl 8(%ebp), %edx
	subl $1, %edx
	movl %edx, -4(%ebp)
	pushl -4(%ebp)
	call is_odd
	movl -12(%esp), %edx
	movl %edx, -8(%ebp)
	addl $4, %esp
	movl -8(%ebp), %edx
	movl %edx, -4(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret

label2:


is_odd:

	pushl %ebp
	movl %esp, %ebp
	subl $8, %esp
	movl 8(%ebp), %ecx
	movl $0, %edx
	cmp %ecx, %edx
	je label4
	jmp label5

label4:

	movl $0, %edx
	movl %edx, -4(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret
	jmp label6

label5:

	movl 8(%ebp), %edx
	subl $1, %edx
	movl %edx, -4(%ebp)
	pushl -4(%ebp)
	call is_even
	movl -12(%esp), %edx
	movl %edx, -8(%ebp)
	addl $4, %esp
	movl -8(%ebp), %edx
	movl %edx, -4(%ebp)
	movl %ebp, %esp
	pop %ebp
	ret

label6:


__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $8, %esp
	pushl $7
	call is_even
	movl -12(%esp), %edx
	movl %edx, -4(%ebp)
	addl $4, %esp
	pushl -4(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	pushl $7
	call is_odd
	movl -12(%esp), %edx
	movl %edx, -8(%ebp)
	addl $4, %esp
	pushl -8(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx

exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
