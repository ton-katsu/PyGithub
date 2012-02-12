Documentation
=============
 - tutorial
 - classes for Github objects
   - how to get instances of them
   - properties
   - methods (and arguments)
 - api and how it is wrapped
 - rationale:
   - lazyness for objects returned by API, not for objects requested by user
   - naming: get_xxx() to avoid clashes with attribute xxx (User.followers for example), and to explicit api calls. One get_ <=> one api call. No get_ <=> no api call, most often, and one from time to time to complete an object.
   - lazy completion, but no caching
   - explicit edit instead of writeable attributes
   - data model (cf Design.md)

Functional improvements
=======================
 - implement the full API
 - add a full example creating your github graph (listing followers, following, co-contributors, watched repositories, organization co-members, etc.)

Technical improvements
======================
 - Anything.edit shall read the response data and update the object's attributes
 - improve rawRequest
   - pagination
   - http status
 - privatize private methods/hide them behind facade/do something