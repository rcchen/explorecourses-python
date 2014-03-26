explorecourses-python
=====================

Python Wrapper for XML-based ExploreCourses API

### Sample code

```
from explorecourses import ExploreCourses
ec = ExploreCourses()
result = ec.getCourse('cs140')
print result.fullCode
>>> CS140
print result.title
>>> Operating Systems and Systems Programming
```