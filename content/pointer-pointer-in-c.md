---
title: Advance Pointer - Pointer Pointer
id: 202502070000
publish: true
tags:
  - techblog
  - c
---

Double pointer, or pointer-pointer is considered somewhat advance technique in C programming language.

In this article I will explain to grandma level about these concepts and common myths about pointer and double pointer.

## Pointer

Pointer is variable that store the memory address of another variable.

Here is what memory layout looks like in the real computer.

slot | address | value 
---|---|---
0 | 0x80200000 | 123 
1 | 0x80200008 | 0
2 | 0x80200011 | 124
3 | 0x80200019 | 0x80200000

As you might notice, the slot 3 is actually a pointer value points to an address that stores the value of 123.

Think of pointer is a **chain of command** in the military, Colonel don't directly command individual soldiers they commands Major and Captain who in turn commands soldiers for the target.

![[chain-of-command-20250207185258.png]]

Everytime you use a `*` to create a pointer, you create a node in the chain of command that could be used later for manipulating something indirectly.

Why is pointer necessary?

Good question, just like you ask why hierarchy or echelon is necessary, they existed are fundamentally because communication bandwidth can't possibly be hold within large group to the certain extend.

Similarly, in the [[stack]] where the memory space is limited is not able to uphold large, long live, or dynamic growing dataset.

So we need a commander to hold all those large, long live, or dynamic growing bits. And that, my friends, is why we need a Pointer.

Technically speaking, Pointer is very efficient, since it only store the address, as least in terms of memory. Depends on CPU's architecture, an address only needs few bits, for any x86 CPU, it can have 2^32 [[registers]], if we address/identify those register by number, then we need 32bit memory in order to cover all the possibly address of registers.

And 32bit memory can hold any size of data from 1 bit to 1gb in the memory indirectly, so later we need to use that large data, we can access it by [[dereferencing]] the Pointer. Very efficient, doesn't it?

## Pointer Pointer

Now, we will get a bit advance but also a little bit exciting, "Giggity Giggity Goo!".

Double pointer, or Pointer pointer, is just a Pointer points to another pointer that in turn points to the real data.

slot | address | value 
---|---|---
0 | 0x80200000 | 0x80200011
1 | 0x80200008 | 0
2 | 0x80200011 | 124
3 | 0x80200019 | 0x80200000

As you can see the memory table above, the slot 3 store an address of slot 1, where slot 1 store an address of slot 2, and the slot 2 store the real value: 124.

Why we even need that shit? Is this some sort of European bureaucracy's representation in the computer science in order to waste your time and make your lovely life miserable?

Hold on, hold on, before we go nuke, those double pointer or triple pointer, or some quadruple pointer, actually have its use cases. Let me explain.

To understand Double pointer, we have to understand what it represents underlaying, it just likes this sentence, without the first half (underlaying) you have no idea what I'm talking about.

Double pointer use case is usually break down to two scenarios.

### Case 1: nature hierarchy of the data structure

We all know that in C we don't have native string, but string is made of characters, so a string is a array of char, and array's representation in C is a Pointer points at the beginning of the array.

If we want to have a array of strings, it naturally comes to Pointer pointer.

```c
char *str1 = "this is a sentence.";
char *str2 = "this is another sentence.";

char **str_arr = (char **)malloc(2 * sizeof(char *));
str_arr[0] = str1;
str_arr[1] = str2;

free(str_arr);
```

If you generalize this use case it will apply to any case that needs a two dimensional array -- because array is represented at a Pointer points to the beginning of the array, the two dimensional array is an array that stores Pointers that points to an array.

```c
// in the stack
int _2D_arr[2][2] = {{1, 2}, {1, 2}};
// in the heap
int len_2darr = 2;
int **_2d_arr_heap = malloc(sizeof(size_t) * len_2darr);
for (int i = 0; i < len_2darr; i++) {
    _2d_arr_heap[i] = calloc(len_2darr, sizeof(int));
}
for (int i = 0; i < len_2darr; i++) {
    for (int j = 0; j < len_2darr; j++) {
	_2d_arr_heap[i][j] = j + 1;
    }
}
// print
for (int i = 0; i < len_2darr; i++) {
    for (int j = 0; j < len_2darr; j++) {
	printf("%d ", _2d_arr_heap[i][j]);
    }
    printf("\n");
}

// free memory
for (int i = 0; i < len_2darr; i++) {
    free(_2d_arr_heap[i]);
}
free(_2d_arr_heap);

// ...
```

*Hey, let me remind you that you have a friend call ChatGPT if you carious why I don't explain the code.*

### Case 2: changing the value but preserve current variable

If you understand the first case, you might confused when you first time saw this coming.

```c
void allocate(void **p, size_t size) {
    *p = malloc(size);
}

int main(void) {
    int **ptr;
    allocate((void *)ptr, sizeof(int) * 2);
    // this is equivalent to:
    // int *ptr
    // allocate((void *)&ptr, sizeof(int) * 2);
    
    int *arr = *ptr;
    arr[0] = 1;
    arr[1] = 2;
    
    printf("first: %d, second: %d", arr[0], arr[1]);
    free(*ptr);

    // ...
}
```

The first parameter in the allocate function is not a two dimensional array, is a Pointer points to another pointer which its value should the beginning address of an array (array Pointer).

The allocate function allocates the memory of given size to the Pointer `*p` that `p` points to, which in turn has being used as an array.

The reason we need to do this is the parameters in a function call is a copy of the originates - each function call will be prepared with new stack space with all parameters copied in the top of the stack.

If we pass `int *p` instead of `int **p` in the call of allocate in the main function, the Pointer you pass in will have the same value but new address (it's a copy), so the memory is allocated to a Pointer we can't use in the main function, which defeat the propose of the allocate function - allocating memory to given parameter.

Let's take a close look:

![[stack-dump-1-20250207174834.png]]

We have `* p` in the `main` declared, its address is 0x80200000, now calling `allocate`, SP, short for stack pointer, jump to location 0x8020501F and make a copy of address of the Pointer in the `main` located at 0x80200000, which is `NULL`. After the allocation, only value in address 0x8020501F is changed, the actual Pointer with address 0x80200000 in the `main` remains untouched.

What will happen if we use double Pointer?

![[stack-dump-2-20250207181054.png]]

Same thing happen when we call `allocate`, but this time is double Pointer, the address in our original Pointer in `main` is copied, but because this time it refers to another Pointer that also declared in `main`, the beginning address of allocated memory will be assigned to Pointer `*p` that is in `main`. So when we dereference Pointer `**p` we got a Pointer that points to the address that just allocated by our `allocate` function, as you saw in the code I shared above!

It's fundamentally the same idea when you want a int type variable (copied during function call) to be changed out side of current function scope and also reflect in your current scope, you will pass the address of the int to function you called, and that function, inevitably, receives a Pointer to int, so it can change the value in the address that you hold in your scope instead of value you passed in.

To warp it up, let's go back to the chain of command example. As a Colonel, you can tell Major to swap out one of his squad, but you can't tell a squad to swap out itself. That's the power of indirect control! That's why when you're being laidoff you always heard that somebody in high position wants to cut the budget but your manager really wants you to stay. 

With that, we concluded this article. 

Phew, that's a hell out of the shit, isn't it? But you just understood something pretty deep and pretty advance you know it? Many so call 10 years programmer might still don't understand how it work. You will beat the hell out of them if you subscribe my blog. BTW, If you grandma didn't understand, tell her I said "remember to read it again!"

I hope you have a wonderful day!
