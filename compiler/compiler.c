#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <string.h>

int token;
char *src, *old_src;
int poolsize;
int line;

int *text, *old_text, *stack;
char data;
int *pc, *bp, *sp, ax, cycle;

enum{LEA, IMM, JMP, CALL, JZ, JNZ, ENT, ADJ, LEV, LI, LC, SI, SC, PUSH, 
	 OR, XOR, AND, EQ, NE, LT, GT, LE, GE, SHL, SHR, ADD, SUB, MUL, DIV, MOD,
	 OPEN, READ, CLOS, PRTF, MALC, MSET, MCMP, EXIT};

int eval()
{
	return 0;
}
	 
void next()
{
	token = *src++;
	return;
}

void program()
{
	next();
	while(token > 0)
	{
		printf("token is: %c\n", token);
		next();
	}
}

void expression(int level)
{
	
}

int main(int argc, char **argv)
{
	int i, fd;
	
	argc--;
	argv++;
	
	poolsize = 256 * 1024;
	line = 1;
	
	if((fd = open(*argv,0)) < 0)
	{
		printf("could not open(%s)\n", *argv);
		return -1;
	}
	
	if(!(src = old_src = malloc(poolsize)))
	{
		printf("could not malloc(%d) for source area\n", poolsize);
		return -1;
	}
	
	if((i = read(fd, src, poolsize - 1)) <= 0)
	{
		printf("read() return %d\n", i);
		return -1;
	}
	
	src[i] = 0;
	close(fd);
	
	if(!(text = old_text = malloc(poolsize)))
	{
		printf("could not malloc(%d) for text area\n", poolsize);
		return -1;
	}
	
	if(!(data = malloc(poolsize)))
	{
		printf("could not malloc(%d) for data area\n", poolsize);
		return -1;
	}
	
	if(!(stack = malloc(poolsize)))
	{
		printf("could not malloc(%d) for stack area\n", poolsize);
		return -1;
	}
	
	memset(text, 0, poolsize);
	memset(data, 0, poolsize);
	memset(stack, 0, poolsize);
	
	bp = sp =(int *)((int) stack + poolsize);
	ax = 0;
	i = 0;
	text[i++] = IMM;
	text[i++] = 10;
	text[i++] = PUSH;
	text[i++] = IMM;
	text[i++] = 20;
	text[i++] = ADD;
	text[i++] = PUSH;
	text[i++] = EXIT;
	pc = text;
	
	program();
	return eval();
}