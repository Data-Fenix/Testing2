```
\ \ \ \ \ \           \     \     \ \ \ \ \ \ \  
\           \       \      \ \              \
\             \   \       \   \           \
\ \ \           \        \ \ \ \        \   
\             \   \     \       \     \           
\           \       \  \         \  \             
\ \ \ \ \ \           \           \ \ \ \ \ Y M E
```

Adapted | from GoogleDoc \
-> https://google.github.io/styleguide/pyguide.html <- 

## 3.8 Comments and Docstrings
Be sure to use the right style for module, function, method docstrings and inline comments.


### 3.8.1 Docstrings
Python uses docstrings to document code. A docstring is a string that is the first statement in a package, module, class or function. These strings can be extracted automatically through the __doc__ member of the object and are used by pydoc. (Try running pydoc on your module to see how it looks.) Always use the three-double-quote """ format for docstrings (per PEP 257). A docstring should be organized as a summary line (one physical line not exceeding 80 characters) terminated by a period, question mark, or exclamation point. When writing more (encouraged), this must be followed by a blank line, followed by the rest of the docstring starting at the same cursor position as the first quote of the first line. There are more formatting guidelines for docstrings below.

### 3.8.2 Modules
Every file should contain license boilerplate. Choose the appropriate boilerplate for the license used by the project (for example, Apache 2.0, BSD, LGPL, GPL).

Files should start with a docstring describing the contents and usage of the module.
```python
"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
```


#### 3.8.2.1 Test modules
Module-level docstrings for test files are not required. They should be included only when there is additional information that can be provided.

Examples include some specifics on how the test should be run, an explanation of an unusual setup pattern, dependency on the external environment, and so on.

```python
"""This blaze test uses golden files.

You can update those files by running
`blaze run //foo/bar:foo_test -- --update_golden_files` from the `google3`
directory.
"""
```

Docstrings that do not provide any new information should not be used.

```python
"""Tests for foo.bar."""
```

### 3.8.3 Functions and Methods
In this section, “function” means a method, function, generator, or property.

A docstring is mandatory for every function that has one or more of the following properties:
- being part of the public API
- nontrivial size
- non-obvious logic

A docstring should give enough information to write a call to the function without reading the function’s code. The docstring should describe the function’s calling syntax and its semantics, but generally not its implementation details, unless those details are relevant to how the function is to be used. For example, a function that mutates one of its arguments as a side effect should note that in its docstring. Otherwise, subtle but important details of a function’s implementation that are not relevant to the caller are better expressed as comments alongside the code than within the function’s docstring.

The docstring may be descriptive-style (`"""Fetches rows from a Bigtable."""`) or imperative-style (`"""Fetch rows from a Bigtable."""`), but the style should be consistent within a file. The docstring for a @property data descriptor should use the same style as the docstring for an attribute or a function argument (`"""The Bigtable path."""`, rather than `"""Returns the Bigtable path."""`).

A method that overrides a method from a base class may have a simple docstring sending the reader to its overridden method’s docstring, such as `"""See base class."""`. The rationale is that there is no need to repeat in many places documentation that is already present in the base method’s docstring. However, if the overriding method’s behavior is substantially different from the overridden method, or details need to be provided (e.g., documenting additional side effects), a docstring with at least those differences is required on the overriding method.

Certain aspects of a function should be documented in special sections, listed below. Each section begins with a heading line, which ends with a colon. All sections other than the heading should maintain a hanging indent of two or four spaces (be consistent within a file). These sections can be omitted in cases where the function’s name and signature are informative enough that it can be aptly described using a one-line docstring.

#### Args:
List each parameter by name. A description should follow the name, and be separated by a colon followed by either a space or newline. If the description is too long to fit on a single 80-character line, use a hanging indent of 2 or 4 spaces more than the parameter name (be consistent with the rest of the docstrings in the file). The description should include required type(s) if the code does not contain a corresponding type annotation. If a function accepts `*foo` (variable length argument lists) and/or `**bar` (arbitrary keyword arguments), they should be listed as `*foo` and `**bar`.

#### Returns: (or Yields: for generators)
Describe the semantics of the return value, including any type information that the type annotation does not provide. If the function only returns None, this section is not required. It may also be omitted if the docstring starts with Returns or Yields (e.g. `"""Returns row from Bigtable as a tuple of strings."""`) and the opening sentence is sufficient to describe the return value. Do not imitate older ‘NumPy style’ (example), which frequently documented a tuple return value as if it were multiple return values with individual names (never mentioning the tuple). Instead, describe such a return value as: `“Returns: A tuple (mat_a, mat_b), where mat_a is …, and …”`. The auxiliary names in the docstring need not necessarily correspond to any internal names used in the function body (as those are not part of the API).

#### Raises:
List all exceptions that are relevant to the interface followed by a description. Use a similar exception name + colon + space or newline and hanging indent style as described in Args:. You should not document exceptions that get raised if the API specified in the docstring is violated (because this would paradoxically make behavior under violation of the API part of the API).

#### No types in doctrings
The parameter type does not have to be reported in the docstrings as it should already be precised in the definition of the function. 


```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.
    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be
          returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the
        table (and require_all_keys must have been False).

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
```

Similarly, this variation on Args: with a line break is also allowed:

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
      table_handle:
        An open smalltable.Table instance.
      keys:
        A sequence of strings representing the key of each table row to
        fetch.  String keys will be UTF-8 encoded.
      require_all_keys:
        If True only rows with values set for all keys will be returned.

    Returns:
      A dict mapping keys to the corresponding table row data
      fetched. Each row is represented as a tuple of strings. For
      example:

      {b'Serak': ('Rigel VII', 'Preparer'),
       b'Zim': ('Irk', 'Invader'),
       b'Lrrr': ('Omicron Persei 8', 'Emperor')}

      Returned keys are always bytes.  If a key from the keys argument is
      missing from the dictionary, then that row was not found in the
      table (and require_all_keys must have been False).

    Raises:
      IOError: An error occurred accessing the smalltable.
    """
```


### 3.8.4 Classes
Classes are documented by adding a docstring to the class and the `__init__` method. \
The doctring in the `Class` should be quite general about the class, and the doctrings in `__init__` should focus on the class instantiation, and should specially describe the Args. \
Public attributes of a class always have to be defined using `@property` decorators for getters, which is where the attributes docstring should be defined. \
Property setters do not need to be documented.

```python
class SampleClass:

    """Summary of the class."""

    def __init__(self, likes_spam: bool = False):
        """Summary of the init function here.

        Args:
          likes_spam: Defines if instance exhibits this preference.
        """
        self._likes_spam = likes_spam
        self._eggs = 0

    @property
    def likes_spam(self):
        """getting like spam value"""
        return self._likes_spam

    @likes_spam.setter
    def likes_spam(self, value:bool):
        """setting like_spam value"""
        self._likes_spam = value

    def public_method(self):
        """Performs operation blah."""
```        
All class docstrings should start with a one-line summary that describes what the class instance represents. This implies that subclasses of Exception should also describe what the exception represents, and not the context in which it might occur. The class docstring should not repeat unnecessary information, such as that the class is a class.

```python
# Yes:
class CheeseShopAddress:
  """The address of a cheese shop.

  ...
  """

class OutOfCheeseError(Exception):
  """No more cheese is available."""
```

```python
# No:
class CheeseShopAddress:
  """Class that describes the address of a cheese shop.

  ...
  """

class OutOfCheeseError(Exception):
  """Raised when no more cheese is available."""
```

### 3.8.5 Note
The Note serves as a helpful annotation within a code documentation that provides additional information, explanations, or warnings to users and developers. It is often used to clarify specific aspects of the code, highlight important details, or suggest best practices, making it easier for others to understand and work with the code. This notation is a valuable tool for enhancing code readability and facilitating collaboration among developers.

```python
class Dog:
    """
    Represents a simple dog class."""

    def __init__(self, name, age):
        """
        Initializes a new instance of the Dog class.

        Args:
            name (str): The name of the dog.
            age (int): The age of the dog in years.

        Note:
            Ensure that the 'name' is a non-empty string, and 'age' is a positive integer to create a valid dog instance.
        """
        self.name = name
        self.age = age

    def bark(self):
        """
        Makes the dog bark.

        Note:
            This method simulates the dog's bark behavior and doesn't take any arguments.
        """
        print(f"{self.name} says Woof!")
```

### 3.8.6 Examples
We wish to have as many examples as possible in our scripts so our documentation contains use cases. \
These examples should be written so **doctest** module can run them. \
The doctest module searches for pieces of text that look like interactive Python sessions, and then executes those sessions to verify that they work exactly as shown.

```python
class Dog:
    """
    Represents a simple dog class.

    Example:
      >>> my_dog = Dog("Buddy", 3)
      >>> my_dog.bark()
      Buddy says Woof!
    ...
```
In this example, the code to run is predeeded by `>>>`. \
The next line without `>>>` states what is what is supposed to be returned. \
When tested by `doctest`, the `>>>` will be run what is returned will be compared to the return lines. \
The return line is only optional, if there is none, the example is still valid, doctest just run the example without checking what it returns. \ 

We want the doctests to run successfully, meaning that the example provided is correct and can be used as a reference.


### 3.8.7 Block and Inline Comments
The final place to have comments is in tricky parts of the code. If you’re going to have to explain it at the next code review, you should comment it now. Complicated operations get a few lines of comments before the operations commence. Non-obvious ones get comments at the end of the line.

```python 
# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.


if i & (i-1) == 0:  # True if i is 0 or a power of 2.
```

To improve legibility, these comments should start at least 2 spaces away from the code with the comment character #, followed by at least one space before the text of the comment itself.

On the other hand, never describe the code. Assume the person reading the code knows Python (though not what you’re trying to do) better than you do.

``` python
# BAD COMMENT: Now go through the b array and make sure whenever i occurs
# the next element is i+1
```

### 3.8.8 Punctuation, Spelling, and Grammar
Pay attention to punctuation, spelling, and grammar; it is easier to read well-written comments than badly written ones.

Comments should be as readable as narrative text, with proper capitalization and punctuation. In many cases, complete sentences are more readable than sentence fragments. Shorter comments, such as comments at the end of a line of code, can sometimes be less formal, but you should be consistent with your style.

Although it can be frustrating to have a code reviewer point out that you are using a comma when you should be using a semicolon, it is very important that source code maintain a high level of clarity and readability. Proper punctuation, spelling, and grammar help with that goal.

### 3.8.9 DataClasses

Check the following links for more on dataclasses:
- https://realpython.com/python-data-classes/
- https://florimond.dev/en/posts/2018/10/reconciling-dataclasses-and-properties-in-python/
- https://docs.python.org/3/library/dataclasses.html#post-init-processing 

Here is an example on how to write dataclasses 
```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class ProteinTag:
    """
    A immutable container representing a protein purification tag
    Args:
        name: The name of the tag.
        sequence: The sequence of the tag.
        origin:The origin of the tag, e.g. a protein this tag is derived from.
        method: The purification method used with this tag.
        reference: The pubmed link referencing this tag.
        length: The length of the tag.
        fusion: True if the tag is a fusion with another protein or protein domain.
        
    Example:
        >>> tag = ProteinTag(
        ...    name="Isopep-Tag", 
        ...    sequence="TDKDMTITFTNKKDAE", 
        ...    origin="Pilin-C covalent binding", 
        ...    method="Synthetic peptide", 
        ...    reference="https://pubmed.ncbi.nlm.nih.gov/20235501/"
        ...)
        >>> print(tag) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        ProteinTag(name='Isopep-Tag', sequence='TDKDMTITFTNKKDAE', 
        length=16, origin='Pilin-C covalent binding', method='Synthetic peptide', 
        reference='https://pubmed.ncbi.nlm.nih.gov/20235501/', fusion=False, leader=False, cleavage=False)
    """
    name: str = field(repr=True)
    sequence: str = field(repr=True)
    length: int = field(repr=True, default=False)
    origin: str = field(repr=True)
    method: str = field(repr=True)
    reference: str = field(repr=True)
    fusion: bool = field(repr=False, default=False)
    leader: bool = field(repr=False, default=False)
    cleavage: bool = field(repr=False, default=False)
    
    def __post_init__(self):
        """Post init method to set the length of the tag if not provided"""
        if self.le3ngth is False:
            object.__setattr__(self, 'length', len(self.sequence))
```

## 3.10 Strings
Use an **f-string**, the `%` operator, or the `format` method for formatting strings, even when the parameters are all strings. Use your best judgment to decide between string formatting options. A single join with `+` is okay but do not format with `+`.

```python
Yes: x = f'name: {name}; score: {n}'
     x = '%s, %s!' % (imperative, expletive)
     x = '{}, {}'.format(first, second)
     x = 'name: %s; score: %d' % (name, n)
     x = 'name: %(name)s; score: %(score)d' % {'name':name, 'score':n}
     x = 'name: {}; score: {}'.format(name, n)
     x = a + b
No: x = first + ', ' + second
    x = 'name: ' + name + '; score: ' + str(n)
```


Avoid using the + and += operators to accumulate a string within a loop. In some conditions, accumulating a string with addition can lead to quadratic rather than linear running time. Although common accumulations of this sort may be optimized on CPython, that is an implementation detail. The conditions under which an optimization applies are not easy to predict and may change. Instead, add each substring to a list and `''.join` the list after the loop terminates, or write each substring to an `io.StringIO` buffer. These techniques consistently have amortized-linear run-time complexity.

```python
Yes: items = ['<table>']
     for last_name, first_name in employee_list:
         items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
     items.append('</table>')
     employee_table = ''.join(items)
```
```python
No: employee_table = '<table>'
    for last_name, first_name in employee_list:
        employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
    employee_table += '</table>'
```

Be consistent with your choice of string quote character within a file. Pick `'` or `"` and stick with it. It is okay to use the other quote character on a string to avoid the need to backslash-escape quote characters within the string.
```python
Yes:
  Python('Why are you hiding your eyes?')
  Gollum("I'm scared of lint errors.")
  Narrator('"Good!" thought a happy Python reviewer.')
```
```python
No:
  Python("Why are you hiding your eyes?")
  Gollum('The lint. It burns. It burns us.')
  Gollum("Always the great lint. Watching. Watching.")
```
Prefer """ for multi-line strings rather than '''. Projects may choose to use ''' for all non-docstring multi-line strings if and only if they also use ' for regular strings. Docstrings must use """ regardless.

Multi-line strings do not flow with the indentation of the rest of the program. If you need to avoid embedding extra space in the string, use either concatenated single-line strings or a multi-line string with textwrap.dedent() to remove the initial space on each line:
```python
  No:
  long_string = """This is pretty ugly.
Don't do this.
"""
```
```python
  Yes:
  long_string = """This is fine if your use case can accept
      extraneous leading spaces."""
```
```python
  Yes:
  long_string = ("And this is fine if you cannot accept\n" +
                 "extraneous leading spaces.")
```
```python
  Yes:
  long_string = ("And this too is fine if you cannot accept\n"
                 "extraneous leading spaces.")
```
```python
  Yes:
  import textwrap

  long_string = textwrap.dedent("""\
      This is also fine, because textwrap.dedent()
      will collapse common leading spaces in each line.""")
```
Note that using a backslash here does not violate the prohibition against explicit line continuation; in this case, the backslash is escaping a newline in a string literal.



### 3.10.1 Logging
For logging functions that expect a pattern-string (with %-placeholders) as their first argument: Always call them with a string literal (not an f-string!) as their first argument with pattern-parameters as subsequent arguments. Some logging implementations collect the unexpanded pattern-string as a queryable field. It also prevents spending time rendering a message that no logger is configured to output.

```python
  Yes:
  import tensorflow as tf
  logger = tf.get_logger()
  logger.info('TensorFlow Version is: %s', tf.__version__)
```
```python
  Yes:
  import os
  from absl import logging

  logging.info('Current $PAGER is: %s', os.getenv('PAGER', default=''))

  homedir = os.getenv('HOME')
  if homedir is None or not os.access(homedir, os.W_OK):
    logging.error('Cannot write to home directory, $HOME=%r', homedir)
```
```python
  No:
  import os
  from absl import logging

  logging.info('Current $PAGER is:')
  logging.info(os.getenv('PAGER', default=''))

  homedir = os.getenv('HOME')
  if homedir is None or not os.access(homedir, os.W_OK):
    logging.error(f'Cannot write to home directory, $HOME={homedir!r}')
```

### 3.10.2 Error Messages
Error messages (such as: message strings on exceptions like `ValueError`, or messages shown to the user) should follow three guidelines:

- 1. The message needs to precisely match the actual error condition.
- 2. Interpolated pieces need to always be clearly identifiable as such.
- 3. They should allow simple automated processing (e.g. grepping).

```python
  Yes:
  if not 0 <= p <= 1:
    raise ValueError(f'Not a probability: {p!r}')

  try:
    os.rmdir(workdir)
  except OSError as error:
    logging.warning('Could not remove directory (reason: %r): %r',
                    error, workdir)
```
```python
  No:
  if p < 0 or p > 1:  # PROBLEM: also false for float('nan')!
    raise ValueError(f'Not a probability: {p!r}')

  try:
    os.rmdir(workdir)
  except OSError:
    # PROBLEM: Message makes an assumption that might not be true:
    # Deletion might have failed for some other reason, misleading
    # whoever has to debug this.
    logging.warning('Directory already was deleted: %s', workdir)

  try:
    os.rmdir(workdir)
  except OSError:
    # PROBLEM: The message is harder to grep for than necessary, and
    # not universally non-confusing for all possible values of `workdir`.
    # Imagine someone calling a library function with such code
    # using a name such as workdir = 'deleted'. The warning would read:
    # "The deleted directory could not be deleted."
    logging.warning('The %s directory could not be deleted.', workdir)
```



# Additional Ressources

## attrs
https://www.attrs.org/en/stable/examples.html
https://www.youtube.com/watch?v=1S2h11XronA 