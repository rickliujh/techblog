---
title: Rollup of primegen's interview with uncle bob
tags:
- programming
- interview
- cleancode
---

Notes for interview of uncle bob conducted by primegen

- dev double every 5 years
- the propose of the design pattern is to have a name of structure for communicate more clearly between dev when talking or reading the code
- let code force the abstraction upon you by doing the design first before coding
- abstraction come with a cost and it will not pay back if there is a reason to make abstraction 
- agile is a small idea to help small team to deal with small project [25:00]
- agile is a simple idea about:
	- do thing in the really short segments
	- measure how that get done
	- project that out with the end day and tell everybody
- agile is a idea about extreme programming
- breaking code to readable chunk doesn't means you will have nest of leaping around, it's small of bad code if that happened [39:36]
- order the code of how they being called
- be polite to next person coming to the code, don't write rude code -- hard understand, jumping around, not clear, etc.
- there are accidental and essential complexity, the goal of clean code is to reduce accidental complexity to as close to zero, but there always has the case that name of function can't convey the context of the code so you have to read it through
- the TDD is a double entry bookkeeping way to write the code
- back and forth to change the test code when using TDD is the pain especially when you realize that the direction is wrong and have to totally rewrite. but it's a self discipline of way of coding that build the confidence of your code and being able to fearlessly refactoring it at any time
- to have tests suite that is beneficial for refactoring the tests need to against contract/interface of the code [51:47]
	- in TDD, the tests don't couple to the implementation
- any time you touch a system in one place, and it breaks many, it's a design problem
	- you apply exact same principles that any code you ever written to tests code
	- in practice of TDD, every line of code were tested indirectly in many case, no necessary to have to test every line directly, **only test the code that could possibly have the problem directly**
	- technically speaking, only one module affected when requirement changed [53:04] -- book "clean architecture"
		- which means every module only has one dependency 
		- both a problem if a module has many incoming or outgoing dependency
		- can't control all of the module's dependencies but the discipline to minimum the dependency will help
		- a abstraction layer the man in the middle will help to control the dependencies
		- the abstraction introduced to control the dependencies of the module could be not strictly necessary to the behavior of the system but vastly increase the ability to modify it
		- we will get bit by a requirement change that cause many change in code from time to time, but we can mitigate it by observing some small change in the beginning and introducing a protection an abstract layer before a big change ever arrive, because the most likely thing to change is the things being change already
- not all code is worse testing directly [56:40]
	- only test the thing that can possibly break
	- test should be general enough to against a family of function than to each specific function
	- unit test was written in a slightly higher level but below the level of integration test
- integration testing should not be test business rule, unit test should does that [1:01:42]
	- it should test choreography and the flow of data through the units as opposed to individual business rules which is a waste
	- the goal in the integration test is not to make sure all the business rules work
		- it might needs to test all the business rules to make sure the date flow works
		- but won't test every business rules that use the same data flow if there is a guarantee that data flow works
		- including process started properly, data flow channels got open properly, that the right data went across them
		- it can be done by putting a special little widget on it, or sticking in some extra fixture code that will look at the flow of data
		- it is very technical thing
		- golden standards are least effective way of keeping a system under control




### Resources
[I Interviewed Uncle Bob (youtube.com)](https://www.youtube.com/watch?v=UBXXw2JSloo)
