.data

blank:
	.int	0
TEMP_VAR1:
	.string	"bye"
TEMP_VAR0:
	.string	"hello"
n:
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
	subl $16, %esp
	pushl $TEMP_VAR0
	pushl $outFormatStr
	call printf
	pop %ebx
	pop %ebx
	pushl $TEMP_VAR0
	pushl $outFormatStr
	call printf
	pop %ebx
	pop %ebx
	pushl $TEMP_VAR1
	pushl $outFormatStr
	call printf
	pop %ebx
	pop %ebx

exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
