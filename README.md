Solution for the  `find_shortest_distance()` task.

Usage:

* Just run the file `distance.py` without arguments with a Python3.6
  interpreter and the test suite will be run
* Alternatively, you can run it with 3 arguments: file, word1, word2

Example Usage:
```
$ python3.6 distance.py test.txt Roads I
Distance between `Roads` and `I` is 5 words
```

The module contains two implementations of the search with different
complexities. I created the more complex one first and then thought about how
decrease computational complexity and came up with the linear solution.

The test suite checks both implementations.
