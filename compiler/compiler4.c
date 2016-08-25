#include <stdio.h>
#include <stdlib.h>

int token;
int token_val;
char *src  = NULL;
char *line = NULL;
enum {Num};

void next()
{
	while(*src == ' ' || *src == '\t'){src++;}
	token = *src++;
	if(token >= '0' && token <= '9')
	{
		token_val = token - '0';
		token = Num;
		while(*src >= '0' && *src <= '9')
		{
			token_val = token_val * 10 + *src - '0';
			src++;
		}
		return;
	}
}

void match(int tk)
{
	if(token != tk)
	{
		printf("expected token: %d(%c), got: %d(%c)\n", tk, tk, token, token);
		exit(-1);
	}
	next();
}

int expr()
{
	int lvalue = term();
	return expr_tail(lvalue);
}

int expr_tail(int lvalue)
{
	if(token == '+')
	{
		match('+');
		int value = lvalue + term();
		return expr_tail(value);
	}
	else if(token == '-')
	{
		match('-');
		int value = lvalue - term();
		return expr_tail(value);
	}
	else{return lvalue;}
}

int term()
{
	int lvalue = factor();
	return term_tail(lvalue);
}

int term_tail(int lvalue)
{
	if(token == '*')
	{
		match('*');
		int value = lvalue * factor();
		return term_tail(value);
	}
	else if(token == '/')
	{
		match('/');
		int value = lvalue / factor();
		return term_tail(value);
	}
	else{return lvalue;}
}

int factor()
{
	if(token == '(')
	{
		match('(');
		int value = expr();
		match(')');
		return value;
	}
	else
	{
		match(Num);
		int value = token_val;
		return value;
	}
}

void main()
{
	src = "1+( ( 12 * 3)  / 2  -5 )*  3";
	next();
	printf("%d\n", expr());
}