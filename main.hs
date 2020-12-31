import Control.Monad
import System.IO

import Data.List

import Data.List.Split
import Data.Graph.Types
import Data.Graph.DGraph
import Data.Graph.Visualize

data Relation = Synonym | Antonym deriving(Show)

createNode :: [String] -> (String, [(String, Relation)])
createNode (w:ws) = (w, zip ws (repeat Synonym))


createGraph :: [[String]] -> DGraph String Relation
createGraph wordlists = fromList (map createNode wordlists)

read' :: IO String
read' =
    putStr "query> "
    >> hFlush stdout
    >> getLine

print' :: String -> IO()
print' = putStrLn

eval' :: DGraph String Relation -> String -> Int -> [String]
eval' graph word depth = limitedDFS (depth+1) graph [word]
    where
        limitedDFS depth graph words =
            if depth == 1 then
                words
            else
                limitedDFS (depth-1) graph (nub ((concat (map (reachableAdjacentVertices graph) words))++words))

repl graph = do
    command <- fmap words read'
    if length command /= 2 then
        print' "Error: syntax is <word> <depth>"
    else
        print' (show (eval' graph (head command) ((read (last command) :: Int))))
        >> repl graph

main = do
    lines <- fmap lines $ readFile "small-thesaurus.csv"
    let wordlists = map (splitOn ",") lines
    let wordgraph = createGraph wordlists

    repl wordgraph
    return ()
