# Why did I come up with this idea?

Future archaeologists may puzzle over why this repo exists; I also write this as a reminder to myself.

1. I release a Python package.  It shall help users explore and manipulate data through a mostly conversational interface.
2. It promotes DuckDB usage. DuckDB benefits users due to its performant query processing engine, its role as a universal access connector to several data stores, and its light footprint.
3. It shall guide & help users get comfortable with DuckDB concepts and syntax.
4. It shall make users more productive due to its generative capabilities, its function as a wrapper and, in future, its ability to serve as a store of readymade, contextual queries which need not be generated again.

## Approach

Enough of the motivations.  In the spirit of starting small, let's start with these items, translate them to requirements and see how we can solve them.

|Sl No| Motivation | Requirement |  Approach |
|-----|------------|-------------|-----------|
|1|I release a Python package.  It shall help users explore and manipulate data through a mostly conversational interface.| Users want to explore data using natural language.| Provide a Python class which uses generative AI for DuckDB SQL, wraps a DuckDB connection for execution, and provides methods to access output|
|2|It promotes DuckDB usage. DuckDB benefits users due to its performant query processing engine, its role as a universal access connector to several data stores, and its light footprint.|Users want to execute DuckDB SQL including code that they generate using AI. |Provide access to a DuckDB connection within the class and use it to execute input queries.|
|3|It shall guide & help users get comfortable with DuckDB concepts and syntax.| Users want to understand how to call DuckDB instead of relying on a generative component all throughout.| Provide explanation, summary and comment capabilities in addition to pure code generation capabilities.|
|4| It shall make users more productive due to its generative capabilities, its function as a wrapper and, in future, its ability to serve as a store of readymade, contextual queries which need not be generated again.| Users want to run DuckDB in a cost-effective manner.| Capture query history and make available locally for first level of reference for users.|



