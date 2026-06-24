This is a Python implementation of QuickStats, a class that calculates
basic descriptive statistics from a stream of data with efficient dynamic
updating. Data can be added to a QuickStats object `qs` using
`qs.new_obs(datum)` or `qs.add_all(iterable_collection)`, both of which
can be chained, e.g. `qs.new_obs(1).new_obs(2)` or
`qs.add_all([1,2]).new_obs(3)`. Statistics for the current set of
data can be polled on demand: `qs.n`, `qs.avg`, `qs.s`, `qs.var`, etc.

