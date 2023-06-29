# WikipediaGraph
A small project to represent wikipedia in a graph.


## Summary
Wikipedia contains links in itself. I wanted to create a graph where each wikipedia page's links are atached as nodes and a recursive search keeps retrieving the links of each link etc... For this, I've used BeautifulSoup and NetworkX for the task.


## Why?
This was just to improve my graph skills in a cool and graphic way. I don't really care if it has been already done before.


## Results
I've only retrieved the first 10 links from every page and a search depth of 5. This should search in the space of 100.000 wikipedia pages. If a page has been already visited, it's not processed. The starting page is **"Philosophy"** for a meme reason.


### The Graph
Some cool visualization.
![]("./Untitled (2).png")


### The Connections
Using Graphi, we can visualize and plot the graph in a cool way!
![](./dasdasdasd.png)


### Walking the Graph
Walking the graph means to retrieve the shortest path between two pages. Similar to the wiki game.
For example, given "Philosophy" and "Evolution", the shortest path is: Philosophy -> Plato -> Parmenides -> Ontology -> Ontogeny -> Evolution

Interesting stuff in my opinion.
