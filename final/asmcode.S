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
	subl $0, %esp
	pushl 16(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	pushl 12(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	pushl 8(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	movl %ebp, %esp
	pop %ebp
	ret

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $28, %esp
	movl $2, -4(%ebp)
	movl $4, -12(%ebp)
	movl $33, -8(%ebp)
	pushl -4(%ebp)
	pushl -8(%ebp)
	pushl -12(%ebp)
	call fun
	addl $12, %esp

exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
