library(jsonlite)
library(plyr)
library(igraph)
library(visNetwork)

mountains <- fromJSON("/users/scottsfarley/documents/summitscraper/data/spmountains.json")


# graph <- as.list(mountains$parentURLs)
# names(graph) <- mountains$URL
# 


nodes <- character()
targets <- character()
nodeLabels <- character()
targetLabels <- character()


idx <- 1
for (i in 1:length(mountains$URL)){ ## each mountain
  node <- mountains$URL[i]
  edges <- mountains$parentURLs[[i]]
  if (length(edges) == 0){
    row = c(node, "")
    nodes[idx] <- node 
    nodeLabels[idx] <- mountains$title[i]
    targets[idx] <- ""
    targetLabels[idx] <- "" 
    idx = idx + 1
  }else{
    for (j in 1:length(edges)){
      edge <- mountains$parentURLs[[i]][[j]]
      print(edge)
      row = c(node, edge)
      nodes[idx] <- node
      targets[idx] <- edge
      nodeLabels[idx] <- mountains$title[i]
      targetLabels[idx] <- mountains$parents[[i]][[j]]
      idx = idx + 1
    }
  }
}


graph <- data.frame(nodes, targets)

graph <- graph[1:100, ]

g <- graph.data.frame(d = graph)

