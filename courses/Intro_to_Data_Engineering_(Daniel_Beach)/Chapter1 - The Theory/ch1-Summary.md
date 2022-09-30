# Summary of Chapter 1 : The Theory  
The first chapter focuses on the basic ideas to keep in mind when designing a data pipeline:
1. movement
2. storage
3. access
4. repeatable
5. resilient
6. scalable

These have to be kept in mind throught the whole process of design and put extra emphasis in getting these right at the begining to reduce headache later.

## Highlights:

> Building a solid understaing of why we need data pipelines and what they should accomplish will end up driving every decision made along the way.  

> When data engineers think about the movement of data, one of the first thoughts should be ... "Is this data pipleline streaming, batch, or something in between?"  

> Data is of no use without reasonable accessibility and usability.

>Choosing storage and file types is one of the most important topics and with far-reaching consequences when designing data pipelines.

>a repeatable pipeline means:  
• Anyone must be able to run a data pipeline.  
• Anyone must be able to troubleshoot a pipeline.  
• Pipelines break, they will have to be re-run.  
• Pipelines should produce the same results (idempotent).  

> There should not be many instances of “hardcoded” values, like dates or numbers in the code. This inevitably means that an engineer will have to make a code change just to run a pipeline for some historic data. Is there no try: except: blocks? This probably means the author didn’t think about the pipeline in a resilient way.

> A data pipeline that isn’t scalable isn’t a pipeline at all,
it’s just a one-time script that is doomed from the beginning.

>  Scalability has to be one of the main tenants driving the creation of the pipeline from the beginning.
