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

exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
