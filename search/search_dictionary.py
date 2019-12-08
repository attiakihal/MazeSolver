from search.a_star_euclidean import a_star_euclidean
from search.a_star_manhattan import a_star_manhattan
from search.bidirectional_bfs import bidirectional_bfs
from search.bfs import bfs
from search.dfs import dfs

search_dictionary = {
    "a_star_euclidean": a_star_euclidean,
    "a_star_manhattan": a_star_manhattan,
    "dfs": dfs,
    "bfs": bfs,
    "bidirectional_bfs": bidirectional_bfs
}
