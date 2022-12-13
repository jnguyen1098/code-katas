# Competitive Programming Notes
* **Imports**: `collections`, `heapq`, `itertools`, `functools`, `copy`, `math`, `random`, `re`, `sys`, `typing`
* **Parsing**
  * `strsep(line[, sep])` - parse `sep`arator-delimited `str` as `list[str]` (`foo bar baz` -> `["foo", "bar", "baz"]`)
  * `intsep(line[, sep])` - parse `sep`arator-delimited `int` as `list[int]` (`1 23 3` -> `[1, 23, 3]`)
  * `intgrid(line)` - parse adjacent `int` as `list[int]` (`12345` -> `[1, 2, 3, 4, 5]`)
  * `parse(pattern, line)` - create `group` from regex as `list[str]` (`3 to 6` -> `["3", "6"]` using `r"(\d+) to (\d+)"`)
* **Logging** - `log(message, newline=False)` or `log(defer(f"Expensive {resource}"))`
* **`DIR`ection**:
  * Kernels - `DIR.{DIAG,HORZ,VERT,SURR,ADJA}`
  * Bearings - `DIR.{N,S,E,W,NW,NE,SW,SE}`
* **Reverse a dictionary** `revdict(source_dict)`
* **Pointers and Variables** Use `Context` for this
* **Chinese Remainder Theorem** - `crt(residues, moduli)`
* **Documentation**
  * [Documentation for `collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)
  * [Documentation for `collections.defaultdict`](https://docs.python.org/3/library/collections.html#collections.defaultdict)
  * [Documentation for `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque)
  * [Documentation for `heapq`](https://docs.python.org/3/library/heapq.html)
  * [Documentation for `itertools`](https://docs.python.org/3/library/itertools.html)
  * [Documentation for `functools`](https://docs.python.org/3/library/functools.html)
* **Point**
  * **Create** `Point(1, 2)` or `Point([1, 2])` or `Point((1, 2))`
  * **Normal Add/Sub** `point1 += (1, 2)`  
  * **Boundary Add/Sub** `point.get_point((1, 1), 1, 2, 3, 4)`
    * `point.get_point((1, 1), x_min=1, x_max=2, y_min=3, y_max=4)`
  * **Kernel Reach** `point.adja`, `point.surr`, `point.diag`, `point.horz`, `point.vert`
  * **Custom Kernel Reach** `point.reaches(some_other_point, kernel=((1, 1), (1, 0)))`
  * **Convert** `point.to_list()` or `.to_tuple()`
  * **Copy** `point.copy()`
  * **1D <-> 2D** `Point.from_id(displacement, col_size)` and `point.to_1d(col_size)`
  * **Equality** `point1 = Point(1, 2)` and `point2 = Point([1, 2])` => `point1 == point2`
  * **Tuple Fallback** `get_point(old_tuple, new_tuple, rows, cols)`
* [Documentation for `itertools`](https://docs.python.org/3/library/itertools.html)
  * **Clone Iterator** `tee(my_iterator, 3)` -> `copy1, copy2, copy3`
  * **Flatten/Unpack** `chain("ABC", "DEF", "G")` -> `A, B, C, D, E, F, G`
    * `chain.from_iterable(["ABC", "DEF", "G"])` -> `A, B, C, D, E, F, G`
  * **Subset Bitmask Select** `compress("ABCDEF", [1, 0, 1, 0, 1, 1])` -> `A, C, E, F`
  * **Infinite Cycle** `cycle([1, 2, 3])` -> `1, 2, 3, 1, 2, 3, ...,`
  * **Absement Sum** `accumulate([1, 2, 3])` -> `1, 3, 6`
* [Documentation for `functools`](https://docs.python.org/3/library/functools.html)
  * **Make Class Comparable** Implement `==`, then one of: `<` `<=` `>` `>=`, then use `@total_ordering`