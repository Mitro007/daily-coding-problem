> 174. Describe and give an example of each of the following types of polymorphism:
>
> * Ad-hoc polymorphism
> * Parametric polymorphism
> * Subtype polymorphism

**Parametric polymorphism:** Say we have some list of items; this could be a list of integers, doubles, strings, 
whatever. Now consider a method `head()` that returns the first item from that list. This method doesn't care if the 
item is of type Int, String, Apple or Orange. Its return type is the one list is parameterized with and its 
implementation is the same for all types: "return first item".

Unlike parametric polymorphism, **Ad-hoc polymorphism** is bound to a type. Depending on the type, different 
implementations of the method are invoked. Method overloading is one example of ad-hoc polymorphism. For example, 
we can have two versions of method that appends two items - one that takes two integers and adds them, and one that 
takes two strings and concatenates them. You know, 2 plus 3 is 5, but "2" plus "3" is "23".

There's also a third kind of polymorphism, **Subtyping polymorphism**, in which subclasses provide different 
implementations of some superclass method. Unlike the ad-hoc polymorphism where the decision on which implementation 
is being invoked is made at compile time, in subtyping polymorphism it is made at run time (in case of parametric 
polymorphism there is just one implementation so no decision is being made there).

See [Ad-hoc polymorphism and type classes](https://medium.com/@sinisalouc/ad-hoc-polymorphism-and-type-classes-442ae22e5342).