

# Overview of the 5 SOLID design principles

SOLID is an acronym for 5 design principles, which are

- **Single Responsibility Principle**: A class/module/package should have only one reason to change, focusing on a single functionality.
- **Open/Closed Principle**: Entities should be open for extension but closed for direct modification, allowing for adding new features without altering existing code.
- **Liskov Substitution Principle**: Subclasses should be replaceable with their base classes without affecting the program's functionality.
- **Interface Segregation Principle**: Use multiple specific interfaces rather than a single, general-purpose interface to avoid forcing clients to depend on things they don't use.
- **Dependency Inversion Principle**: Depend on abstractions, not concrete implementations, to reduce dependencies and increase modularity.

These principles guide the creation of code that is
* easy to maintain
* easy to extend the system with new functionality without breaking something
* easy to read and understand

Instead of reading code for hours, good software design will enable you to easily navigate understand a codebase. So you can read less and do more.

The principles were first introduced in Robert Martins paper [Design Principles and Design Patterns](https://web.archive.org/web/20150906155800/http://www.objectmentor.com/resources/articles/Principles_and_Patterns.pdf) and named by Michael Feathers.


## Single Responsibility Principle

The Single Responsibility Principle, representing the 'S' in SOLID, advocates for a focused approach in class and module design. Each class, method, function, module, or package should have a singular purpose. For instance, a class dedicated to retrieving user data from a database should not be involved in presenting this data. Separating these distinct responsibilities enhances clarity and maintainability.

### Example

Write narrowly focused classes rather than broad, all-encompassing ones. As an example, do not aggregate various functions in a single `Employee` class, rather break down the functionalities into specialized classes like `EmployeeTimeLog`, `EmployeeTimeOff`, `EmployeeSalary`, `EmployeeDetails`, and so on. This organizes your code more intuitively, makes it easy to understand, and simplifies future modifications.


### Metaphor

This makes the code look like a clean and organized kitchen and a clean and organized bathroom. Here you cook there you ... take showers. If you have your shower and toilet in the kitchen it might be practical because you only need one room with water. But for several other reasons like e.g. hygiene its not good.

There’s a place for everything in your apartment and one room is there for one purpose. Your code should be the same.


## Open / Closed Principle

The essence of the Open/Closed Principle is that modules and objects should be designed to accommodate expansion (extension) without altering existing code (modification). This approach allows for the introduction of new functionalities by adding new code, rather than modifying current code, thereby preserving the integrity and reliability of the existing, tested code.

When a subclass changes inherited behavior or internal state from a superclass, it essentially 'modifies' the existing functionality of the superclass. This violates the Open/Closed principle, as it leads to a system where extending functionality often requires altering existing code, which can introduce new bugs and reduce the system's overall stability.

### Example

Consider the development of an e-commerce module that needs to support various payment methods. One approach might be to create a `Pay` class with different payment methods as its methods. However, this would necessitate modifying the `Pay` class each time a new payment method is added or changed, which is not ideal.

A more efficient approach would involve creating an `PayableInterface`. This interface would define the necessary structure for payment methods. Subsequently, each payment method would be implemented as a separate class adhering to this interface. This design means the core system remains unchanged (closed for modification) when new payment methods are added (open for extension), as these are implemented through adding new classes, not altering the existing system.

### Example for inheritance

Imagine a class `Vehicle` with a method `calculateFuelEfficiency()` and some basic implementation for it. We have two subclasses: `PetrolVehicle` and `GasolineVehicle`, both inheriting from `Vehicle`. To account for differences in fuel types, both subclasses use override the  `calculateFuelEfficiency()` method from `Vehicle` by first calling it, then multiplying the resulting number with a factor specific to petrol or gas.

This design violates the Open/Closed Principle. By overriding `calculateFuelEfficiency()`, `PetrolVehicle` and `GasolineVehicle` modify behavior. If the `Vehicle` class undergoes changes in its fuel efficiency calculation, it could inadvertently impact these subclasses, potentially leading to incorrect calculations. This setup creates a codebase that is brittle and prone to errors whenever the superclass is modified.

#### Better Approach

A more robust approach would involve abstracting the fuel efficiency calculation. The `Vehicle` is becomes an interface definition (without implementations). `PetrolVehicle` and `GasolineVehicle` each implement their own version of the fuel efficiency calculation. To ensure code reuse, they might use a `DistanceTracker` and a `FuelTracker`, and base their calculations on those.
This ensures stability, as changes in one implementation will almost never negatively effect the behavior dependant classes, allowing for independent evolution and maintenance of each subclass.

### Metaphor

Applying the Open/Closed Principle is akin to operating a grocery store that uses a delivery service. The delivery service is open for transporting your groceries, but as the store owner, you shouldn’t interfere with their delivery methods. Imagine if you secretly swapped their vans for race cars to speed up delivery, only to find out the next day that the high speed resulted in broken eggs and damaged produce.


## Liskov Substitution Principle


You should be able to substitute a parent class with any of its child classes, without breaking the system. In other words, implementations of the same interface should never give a different result.

Consider you're developing an app and initially use the file system for data storage. You create code that interacts with the file system, processing files and returning data in an array format. When development progresses, you extend the code to also work with a database. However, despite implementing the same methods, the new database-oriented code returns objects instead of arrays, breaking the code.

### Example

Imagine a digital library system, where `Book` is a base class representing all kinds of reading material. There are subclasses like `FictionBook`, `NonFictionBook`, and `ReferenceBook`. According to the Liskov Substitution Principle, any object of a subclass (like `FictionBook`) should be substitutable for an object of the base class (`Book`) without altering the desirable properties of the program. 

This means if there's a function `DisplayBookDetails(Book book)`, it should work seamlessly whether we pass an object of `Book`, `FictionBook`, or any other subclass. If we introduce a new subclass, say `EBook`, it should also integrate smoothly with existing functions expecting a `Book`. This principle ensures that extending the library system with new types of books won't require rewriting functions that operate on the base `Book` class.


Using types in interface methods can help mitigate the issue of inconsistencies across different implementations. But there are other sources for errors. For instance, throwing an exception where it's not anticipated also constitutes a violation of the Liskov Substitution Principle. Being vigilant about maintaining consistency and predictability in method behaviors across different implementations of an interface is key here.

### Metaphor

The Liskov Substitution Principle is like using different brands of light bulbs in your home. Suppose you have a variety of lamps, each designed for a standard size light bulb. The principle is akin to the idea that you should be able to replace any old light bulb with a new one from any brand, as long as it fits the standard size. Whether it's an LED, an energy-saver, or a classic incandescent bulb, each should work perfectly in your lamp without needing to change the lamp itself. Just like in programming, where objects of a subclass should be able to replace objects of a superclass without disrupting the application, different light bulbs can be substituted in the lamp without affecting its ability to illuminate.


## Interface Segregation Principle

The Interface Segregation Principle states that you should never force the client code to depend on methods it doesn’t use. This is related to the Single Responsibility Principle. 

### Example

Consider a scenario where you have an `Employee` class encompassing all functionalities for employee management in your system. Additionally, there are various classes dedicated to a specific aspect of employee management (like `EmployeeTimeLogController`, `EmployeeTimeOffController`, etc.). These classes all depend on the singular `Employee` class, which poses a risk: any modification in `Employee` could potentially disrupt all these controllers due to their reliance on it.

A more effective approach, as before, is to deconstruct the `Employee` class into smaller, more focused classes, each with its own specific interface. Then each controller to depends only on the interfaces relevant to its functionality. Future changes will then impact smaller parts of the system enhancing robustness and maintainability.

### Metaphor

Your kitchen has a variety of appliances: a microwave, an oven, a refrigerator, and a dishwasher. Each appliance has its own specific control panel, designed for its unique functions. The microwave panel has buttons for heating and defrosting, the refrigerator for temperature control, and the dishwasher for wash cycles.

This is similar to the Interface Segregation Principle, which suggests that it's better to have specific, separate interfaces (like control panels), rather than one general-purpose interface for all of your appliances – which is confusing and makes every dishwasher user adapt, even if changes in the interface are necessary only because of the oven.


## Dependency Inversion Principle

The dependency inversion principle states that high-level modules should not depend on low-level modules - both should depend on abstractions/interfaces.


### Example

Consider two classes: `EmailNotifier` and `OrderProcessor`. The `OrderProcessor` class is responsible for handling orders, and it needs to notify customers when their order is processed. Initially, it's directly dependent on the `EmailNotifier` class for sending these notifications.
If we decide to add another notification method, like `SMSNotifier`, you could be tempted to make `OrderProcessor` work with both an `EmailNotifier` or a `SMSNotifier` as specific classes.

However, to adhere to the Dependency Inversion Principle, we invert the dependency and make all classes depend on a new interface called `INotifier`. This interface declares a method like `SendNotification()`. All notifiers implement this interface (thus depending on it). We also change the `OrderProcessor` class to depend on the `INotifier` interface.

### Metaphor

You’re using electricity for your laptop, your phone, washing mashine, etc. Imagine if you had to wire the power supply into each gadget in a particular way, thus creating a depency on how the specific gadget needs this done.
Instead, you could introduce a new dependency for both power supply and gadget: a standard for power plugs. Instead of power supply and gadget depending on each other, you make both depend on the power plug standard. This is an interface in software design terms (sometimes called a protocol).


## Conclusion

SOLID design principles serve as a roadmap for crafting robust, maintainable, and easily understandable software. When applied effectively, these principles enable teams to focus less on deciphering existing code and more on developing innovative features. Ultimately, these principles are about streamlining the software development process, making it a more efficient and enjoyable experience for developers.