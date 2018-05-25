#include<bits/stdc++.h>
using namespace std;

#define MAX 100000

int arr[MAX];
int top=-1;

bool isEmpty()
{
	if(top==-1)
		return true;
	else
		return false;
}
bool isFull()
{
	if(top==MAX)
		return true;
	else 
		return false;
}
int display()
{
	if(isEmpty())
	{
		cout<<"Stack empty!"<<endl;
	}
	else
	{
		cout<<"array elements are:"<<endl;
		for(int i=top;i>=0;i--)
		{
			cout<<arr[i]<<endl;
		}
	}
}
void push()
{
	if(isFull())
		cout<<"stack overflow"<<endl;
	else
		{
			cout<<"enter element to be pushed:";
			int a; cin>>a;
			cout<<endl;
			top=top+1;
			arr[top]=a;	
		}	
}
void pop()
{
	if(isEmpty())
		cout<<"stack underflow"<<endl;
	else
		top--;
}


int main()
{
	//run the functions 
	cout<<"1.Push\n2.Pop\n3.Display\nEnter your choice:";
	int choice;
	cin>>choice;
	while(1)
	{
		switch(choice)
		{
			case 1:
				{
					push();
					break;
				}
			case 2:
				{
					pop();
					break;
				}
			case 3:
				{
					display();
					break;
				}
			default:
				{
					cout<<"Invalid choice!"<<endl;
				}
		}
		cout<<"Press Y to continue, N to exit";
		char ch; cin>>ch;
		if(ch=='y' || ch=='Y')
		{
			cout<<"enter choice:";
			cin>>choice;
			cout<<endl;
		}
		else
		{
			exit(0);
		}
	}
	return 0;	
}
