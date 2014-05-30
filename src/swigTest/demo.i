%module demo

%begin %{
#pragma warning(disable:4127 4100 4211 4706)
%}

%{
#define __FUNCSIG__ __FUNCTION__
#include <iostream>
void Foo(int size, int data[]) { std::cout << __FUNCSIG__ << std::endl; }
void Foo(double d)             { std::cout << __FUNCSIG__ << std::endl; }
void Foo(int a,int b)          { std::cout << __FUNCSIG__ << std::endl; }
void Foo(int a)                { std::cout << __FUNCSIG__ << std::endl; }
%}

%typemap(in) (int szData,int Data[])
{
  int i; 
  if (!PyTuple_Check($input))
  {
      PyErr_SetString(PyExc_TypeError,"Expecting a tuple for this parameter");
      $1 = 0;
  }
  else
    $1 = (int)PyTuple_Size($input);
  $2 = (int *) malloc(($1+1)*sizeof(int));
  for (i =0; i < $1; i++)
  {
      PyObject *o = PyTuple_GetItem($input,i);
      if (!PyInt_Check(o))
      {
         free ($2);
         PyErr_SetString(PyExc_ValueError,"Expecting a tuple of integers");
         return NULL;
      }
      $2[i] = PyInt_AsLong(o);
  }
  $2[i] = 0;
}

void Foo(int a, int b);
void Foo(double d);
void Foo(int a);
%rename Foo Foot;
void Foo(int szData,int Data[]);
