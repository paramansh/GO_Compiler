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

preorder:

	pushl %ebp
	movl %esp, %ebp
	subl $12, %esp
	movl 8(%ebp), %ecx
	movl $0, %edx
	cmp %ecx, %edx
	je label0
	jmp label1

label0:

	movl %ebp, %esp
	pop %ebp
	ret

label1:

	movl 8(%ebp), %edx
	subl $8, %edx
	movl (%edx), %ecx
	movl %ecx, -4(%ebp)
	pushl -4(%ebp)
	call preorder
	addl $4, %esp
	movl 8(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -8(%ebp)
	pushl -8(%ebp)
	pushl $outFormatInt
	call printf
	pop %ebx
	pop %ebx
	movl 8(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -12(%ebp)
	pushl -12(%ebp)
	call preorder
	addl $4, %esp
	movl %ebp, %esp
	pop %ebp
	ret

__main__:

	pushl %ebp
	movl %esp, %ebp
	subl $104, %esp
	subl $4, %esp
	movl %esp ,-32(%ebp)
	subl $8, %esp
	subl $4, %esp
	movl %esp ,-12(%ebp)
	subl $8, %esp
	subl $4, %esp
	movl %esp ,-16(%ebp)
	subl $8, %esp
	subl $4, %esp
	movl %esp ,-20(%ebp)
	subl $8, %esp
	subl $4, %esp
	movl %esp ,-24(%ebp)
	subl $8, %esp
	subl $4, %esp
	movl %esp ,-28(%ebp)
	subl $8, %esp
	movl -32(%ebp), %edx
	movl %edx, -8(%ebp)
	movl -32(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -36(%ebp)
	movl -32(%ebp), %edx
	subl $4, %edx
	movl $7, (%edx)
	movl -32(%ebp), %edx
	subl $8, %edx
	movl (%edx), %ecx
	movl %ecx, -40(%ebp)
	movl -32(%ebp), %edx
	subl $8, %edx
	movl -12(%ebp), %ecx
	movl %ecx, (%edx)
	movl -32(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -44(%ebp)
	movl -32(%ebp), %edx
	subl $0, %edx
	movl -16(%ebp), %ecx
	movl %ecx, (%edx)
	movl -12(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -48(%ebp)
	movl -12(%ebp), %edx
	subl $4, %edx
	movl $4, (%edx)
	movl -12(%ebp), %edx
	subl $8, %edx
	movl (%edx), %ecx
	movl %ecx, -52(%ebp)
	movl -12(%ebp), %edx
	subl $8, %edx
	movl -20(%ebp), %ecx
	movl %ecx, (%edx)
	movl -12(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -56(%ebp)
	movl -12(%ebp), %edx
	subl $0, %edx
	movl $0, (%edx)
	movl -16(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -60(%ebp)
	movl -16(%ebp), %edx
	subl $4, %edx
	movl $11, (%edx)
	movl -16(%ebp), %edx
	subl $8, %edx
	movl (%edx), %ecx
	movl %ecx, -64(%ebp)
	movl -16(%ebp), %edx
	subl $8, %edx
	movl -24(%ebp), %ecx
	movl %ecx, (%edx)
	movl -16(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -68(%ebp)
	movl -16(%ebp), %edx
	subl $0, %edx
	movl -28(%ebp), %ecx
	movl %ecx, (%edx)
	movl -20(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -72(%ebp)
	movl -20(%ebp), %edx
	subl $4, %edx
	movl $1, (%edx)
	movl -20(%ebp), %edx
	subl $8, %edx
	movl (%edx), %ecx
	movl %ecx, -76(%ebp)
	movl -20(%ebp), %edx
	subl $8, %edx
	movl $0, (%edx)
	movl -20(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -80(%ebp)
	movl -20(%ebp), %edx
	subl $0, %edx
	movl $0, (%edx)
	movl -24(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -84(%ebp)
	movl -24(%ebp), %edx
	subl $4, %edx
	movl $9, (%edx)
	movl -24(%ebp), %edx
	subl $8, %edx
	movl (%edx), %ecx
	movl %ecx, -88(%ebp)
	movl -24(%ebp), %edx
	subl $8, %edx
	movl $0, (%edx)
	movl -24(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -92(%ebp)
	movl -24(%ebp), %edx
	subl $0, %edx
	movl $0, (%edx)
	movl -28(%ebp), %edx
	subl $4, %edx
	movl (%edx), %ecx
	movl %ecx, -96(%ebp)
	movl -28(%ebp), %edx
	subl $4, %edx
	movl $13, (%edx)
	movl -28(%ebp), %edx
	subl $8, %edx
	movl (%edx), %ecx
	movl %ecx, -100(%ebp)
	movl -28(%ebp), %edx
	subl $8, %edx
	movl $0, (%edx)
	movl -28(%ebp), %edx
	subl $0, %edx
	movl (%edx), %ecx
	movl %ecx, -104(%ebp)
	movl -28(%ebp), %edx
	subl $0, %edx
	movl $0, (%edx)
	pushl -8(%ebp)
	call preorder
	addl $4, %esp

exit:

	movl $0, %ebx
	movl $1, %eax
	int $0x80
