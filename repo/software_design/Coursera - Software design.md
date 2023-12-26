# Software Architect and Design Roles in Industry 
These are questions asked to two senior software architects.

## Software architecture and software design ? What is the different ?
Important is you want to build a system which is the basis of many people work for many years.
If you get it wrong, the project would fail.
Understanding the requirement of the users and the ability to build a system that will deliver those requirements.

## Key challenges
- Tendency to have trade off between speed and quality
- Understanding the client's problem
	- they generally don't understand their problem
	- they might need guidance to define their issue


## What does the software architect do?
Responsible fo the overall integrity of the project - they are responsible for delivering the project within the budget that the customer has.
To be the interface between the product and the customer and the engineering team. 
- Customers come with requirements for their software
- Software architects needs to come up with the technical requirements for solving the problem
- Then they work with the engineering team to figure out how to implement those requirements

## Principle to follow in designing software?
**Simplicity** 
If it is simple: 
 - you have a good chance to get it right
 - you can explain it simply -> important for knowledge transfer

## Software architect skills
- empathic communication  - soft people skills
	- talking to clients
	- talking to engineers
- basic functional skills
- need to know about what solutions exist - and fit them into your understanding of the field - and how it could help you solve your problem in a better way

## Staying up to date
- reading about the general tech press
- checking what the big players are doing


# Object Oriented Modeling
[Object-Oriented-Design_Course-Notes](./coursera_material/_3cef0bd88cf5c57529dba8223c1d8890_Object-Oriented-Design_Course-Notes.pdf)

	When solving a problem, object-oriented modeling involves the practice of representing key concepts through objects in your software. Depending on the problem, many concepts, even instances of people, places or things become distinct objects in the software.

## Glossary
[Glossary](./coursera_material/_b14d4a2c530a055edc0682adba01da1d_C1-Glossary.pdf)
### Software Requirements, Conceptual and Technical Designs
Software development is an iterative process. \
<img src="./coursera_material/Pasted image 20231113120029.png">

- **Requirements** are essential in order to properly design a software
- **Eliciting requirements**: understanding what the problem is and figuring out we did not think about initially

**Conceptual mockups**
- define **components** and their relations
	- **responsibility** for each component
- do not go into the details which require understanding the full conceptional design

**Technical design**
 - Starts specifying the details of each components
	 - Defining sub components
	 - Technical diagrams

Sometimes need to go back and adapt to the conceptual design to answer issues raise during the technical designs. Then it is important to re-check that the conceptual design answers the initial issue.

## Expressing requirements with user stories
[User-Stories](./coursera_material/_dd374195fd4bdd2f8a95b9ebc8409246_User-Stories.pdf)
## Categories of Objects in Design
[Categories-of-Objects](./coursera_material/_12fa1381f24f1477da387de9693313da_Categories-of-Objects.pdf)
- **Entity Objects:** some real-world entity in the problem space
- **Boundary objects**: between systems
- **Control Objects**: responsible for coordination

### Competing qualities and trade-offs
**Performance - Convenience - Security**
- Architecture is about producing a quality product and you have to define what quality is.
- the most important, it's you're balancing quality versus time to market.
- You have to be able to establish what is good enough:
	- What are the non-negotiables? 
	- What must you do? 
	- And then, what can you negotiate on? 
	- Once you establish that as an architect, you've made a really good job of establishing those guardrails and then the team can execute from there. The business and the engineering team can execute from there.

The importance of **Context**
For example: small amount of data vs big data
Unintended consequences of a certain design

**Functional requirements**
The software design needs to align the solution to meet those requirements.

**Non-functional requirements**
- performance - resource usage - efficiency 
- how well can the code evolve - reusability - flexibility maintainability
	- reviews, test, feedbacks from end users

**Performance and maintainability trade-off:** high performance code may be less clear and less modular so more difficult to maintain.

**Security and performance trade-off**: The extra overhead for high security may reduce performance. Extra code for backward compatibility can worsen both performance and maintainability.

## Record, organize and refine components

During **conceptual design**, you looking how to satisfy your requirements and identify:
- Components
- Responsibilities
- Connections

Then during the technical design, you learn how the components and connections are further refined to give them technical details

How do we represent this information during design?

**CRS : Class Responsibility Collaborators**

They are used to 
	- record 
	- organise 
	- refine the design


<img src="./coursera_material/Pasted image 20231113141904.png">
<img src="./coursera_material/Pasted image 20231113142244.png">
Using CRC cards helps finding the different components necessary for your project
<img src="./coursera_material/Pasted image 20231113142418.png">
A CRS card itself might contain several different components, which seem small enough to be individual classes for programming.


# Object-Oriented Modeling
- Modeling problems and how programming languages evolve toward object orientation. 
- Explore four major design principles used in Object-Oriented Modeling, whichg are key to having a good design for your software.
- These principles help in problem solving and lead to software that is flexible, reusable and maintainable
- UML Class Diagrams and Java Code. 
-

Ready? Let's get started. If you wanted to make a house, you wouldn't start nailing without a design and just figure out the details later. Similarly, for a complex software problem, you don't dive right into solving it in code. There's a design step in between that iteratively deals with both the problem space and the solution space. You need conceptual design to break down the problem further and further into manageable pieces. You also need technical design to describe and refine the solution, so that it is clear enough for developers to implement as working software. Over the years, people have tried many approaches to make the design activity easier. For example, there are design strategies in programming languages suited for solving certain kinds of problems. If you had a data processing problem, you may have used Top Down Programming. This strategy map the processes in the problem to routines to be called. As you broke down the processing needs top down, you made a tree of routines for the eventual solution. These routines would be implemented in a programming language that supported subroutines. To make design easier, you don't want a big mental jump during design work between a concept in the problem space and how to deal with it in the solution space. If these concepts could be described in a design that made sense to both users and developers, that would be great. This would help ensure the two groups can discuss their understanding and common terms. For many kinds of complex problems, it makes sense to think about the concepts using objects. For example, any noun in a problem description could be an important object. The real world, where problems arise, is just full of objects. This has led to the popularity of Object-Oriented Programming with object-oriented languages. But even here, you still don't go straight from the problem to writing the code. There's a conceptual design involving object-oriented analysis to identify the key objects in the problem. There's also technical design involving object-oriented design to further refine the details of the objects, including their attributes and behaviors. The design activities happen iteratively and continuously. The goal during software design is to construct and refine models of all the objects. These models are useful throughout the design process. Initially, the focus will be on the entity objects from the problem space. As a solution in software arises, you introduced control objects that receive events and coordinate actions. You also introduce boundary objects that connect to services outside your system. The models are often expressed in a visual notation called Unified Modeling Language or UML. In Object-Oriented Modeling, you have different sorts of models or UML diagrams to focus on different software issues, like a structural model, to describe what the objects do and how they relate. It's like having a scale model of a building to understand the spatial relationships. To deal with complexity, you can apply design principles and guidelines to simplify objects. Break them down into smaller parts and look for commonalities that can be handled consistently. There's a continual need to critique and evaluate the models to ensure the design addresses the original problem and satisfies quality goals. Qualities are expected to be reusable, flexible and maintainable. The models also serve as design documentation for your software and can be easily mapped to skeletal source code, particularly for an object-oriented language like Java. That can give a good start for the developers implementing the software.