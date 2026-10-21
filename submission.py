from typing import List, Tuple

from mapUtil import (
    CityMap,
    computeDistance,
    createStanfordMap,
    locationFromTag,
    makeTag,
)
from util import Heuristic, SearchProblem, State, UniformCostSearch


# *IMPORTANT* :: A key part of this assignment is figuring out how to model states
# effectively. We've defined a class `State` to help you think through this, with a
# field called `memory`.
#
# As you implement the different types of search problems below, think about what
# `memory` should contain to enable efficient search!
#   > Please read the docstring for `State` in `util.py` for more details and code.
#   > Please read the docstrings for in `mapUtil.py`, especially for the CityMap class

########################################################################################
# Problem 2a: Modeling the Shortest Path Problem.


class ShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path
    from `startLocation` to any location with the specified `endTag`.
    """

    def __init__(self, startLocation: str, endTag: str, cityMap: CityMap):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap

    def startState(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return State(location=self.startLocation)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def isEnd(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return self.endTag in self.cityMap.tags[state.location] # là 1 dict chứa các ds nhãn của từng vị trí
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def actionSuccessorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        """
        Note we want to return a list of *3-tuples* of the form:
            (actionToReachSuccessor: str, successorState: State, cost: float)
        Our action space is the set of all named locations, where a named location 
        string represents a transition from the current location to that new location.
        """
        # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        result = [] # List lưu kq
        cur = state.location
        for neighbor, distance in self.cityMap.distances[cur].items():
            action = neighbor
            successor_state = State(location=neighbor)
            result.append((action, successor_state, distance))
        return result
        raise Exception("Not implemented yet")
        # END_YOUR_CODE


########################################################################################
# Problem 2b: Custom -- Plan a Route through Stanford


def getStanfordShortestPathProblem() -> ShortestPathProblem:
    """
    Create your own search problem using the map of Stanford, specifying your own
    `startLocation`/`endTag`. 

    Run `python mapUtil.py > readableStanfordMap.txt` to dump a file with a list of
    locations and associated tags; you might find it useful to search for the following
    tag keys (amongst others):
        - `landmark=` - Hand-defined landmarks (from `data/stanford-landmarks.json`)
        - `amenity=`  - Various amenity types (e.g., "parking_entrance", "food")
        - `parking=`  - Assorted parking options (e.g., "underground")
    """
    cityMap = createStanfordMap()

    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    startLocation = "354733401"
    endTag = "amenity=food"
    # raise Exception("Not implemented yet")
    # END_YOUR_CODE
    return ShortestPathProblem(startLocation, endTag, cityMap)


########################################################################################
# Problem 3a: Modeling the Waypoints Shortest Path Problem.

class WaypointsShortestPathProblem(SearchProblem):

  def __init__(
      self,
      startLocation: str,
      waypointTags: List[str],
      endTag: str,
      cityMap: CityMap,
  ):
    self.startLocation = startLocation
    self.endTag = endTag
    self.cityMap = cityMap
    self.waypointTags = tuple(sorted(waypointTags))

  def startState(self) -> State:
    # BEGIN_YOUR_CODE
    start_tags = set(self.cityMap.tags.get(self.startLocation, []))
    remaining = set(self.waypointTags) - start_tags
    return State(location=self.startLocation, memory=frozenset(remaining))
    # END_YOUR_CODE

  def isEnd(self, state: State) -> bool:
    # BEGIN_YOUR_CODE
    has_end_tag = self.endTag in self.cityMap.tags.get(state.location, [])
    return len(state.memory) == 0 and has_end_tag
    # END_YOUR_CODE

  def actionSuccessorsAndCosts(
      self, state: State
  ) -> List[Tuple[str, State, float]]:
    # BEGIN_YOUR_CODE
    results = []
    for neighbor, cost in self.cityMap.distances.get(
        state.location, {}
    ).items():
      neighbor_tags = set(self.cityMap.tags.get(neighbor, []))
      new_remaining = state.memory - neighbor_tags
      new_state = State(location=neighbor, memory=frozenset(new_remaining))
      results.append((neighbor, new_state, cost))
    return results
    # END_YOUR_CODE

########################################################################################
# Problem 3c: Custom -- Plan a Route with Unordered Waypoints through Stanford
def getStanfordWaypointsShortestPathProblem() -> WaypointsShortestPathProblem:
  cityMap = createStanfordMap()
  # BEGIN_YOUR_CODE
  startLocation = "7113663356"
  endTag = "amenity=food"
  waypointTags = {
      "landmark=stanford_stadium",
      "landmark=hoover_tower",  
  }
  return WaypointsShortestPathProblem(
      startLocation, waypointTags, endTag, cityMap
  )
  # END_YOUR_CODE

########################################################################################
# Problem 4a: A* to UCS reduction

# Turn an existing SearchProblem (`problem`) you are trying to solve with a
# Heuristic (`heuristic`) into a new SearchProblem (`newSearchProblem`), such
# that running uniform cost search on `newSearchProblem` is equivalent to
# running A* on `problem` subject to `heuristic`.
#
# This process of translating a model of a problem + extra constraints into a
# new instance of the same problem is called a reduction; it's a powerful tool
# for writing down "new" models in a language we're already familiar with.
# See util.py for the class definitions and methods of Heuristic and SearchProblem.


def aStarReduction(problem: SearchProblem, heuristic: Heuristic) -> SearchProblem:
    class NewSearchProblem(SearchProblem):
        def startState(self) -> State:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)

            return State(location=problem.startState().location, memory=problem.startState().memory)
            # END_YOUR_CODE

        def isEnd(self, state: State) -> bool:
            # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
            return problem.isEnd(state)
            # END_YOUR_CODE

        def actionSuccessorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
            # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
            results = []
            # print(state)
            for neighbor, successor_state, cost in problem.actionSuccessorsAndCosts(state):
                heuristic_cost = heuristic.evaluate(successor_state)
                total_cost = cost + heuristic_cost -  heuristic.evaluate(state)
                results.append((neighbor, successor_state, total_cost))
            return results
            # END_YOUR_CODE

    return NewSearchProblem()


########################################################################################
# Problem 4b: "straight-line" heuristic for A*


class StraightLineHeuristic(Heuristic):
    """
    Estimate the cost between locations as the straight-line distance.
        > Hint: you might consider using `computeDistance` defined in `mapUtil.py`
    """
    def __init__(self, endTag: str, cityMap: CityMap):
        self.endTag = endTag
        self.cityMap = cityMap
        self.xy = []
        # Precompute
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        et = self.endTag.split('=')
        try:
            self.xy.append(self.cityMap.geoLocations[str(et[-1])])
        except:
            for lb, tg in self.cityMap.tags.items():
                if self.endTag in tg:
                    self.xy.append(self.cityMap.geoLocations[lb])
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        xy = self.cityMap.geoLocations[state.location]
        res = float(computeDistance(xy, self.xy[0]) )
        for i in range (1, len(self.xy)):
            if float(computeDistance(xy, self.xy[i]) < res ):
                res =  float(computeDistance(xy, self.xy[i]))
        return res
        # END_YOUR_CODE


########################################################################################
# Problem 4c: "no waypoints" heuristic for A*


class NoWaypointsHeuristic(Heuristic):
    """
    Returns the minimum distance from `startLocation` to any location with `endTag`,
    ignoring all waypoints.
    """
    def __init__(self, endTag: str, cityMap: CityMap):
        """
        Precompute cost of shortest path from each location to a location with the desired endTag
        """
        # Define a reversed shortest path problem from a special END state
        # (which connects via 0 cost to all end locations) to `startLocation`.
        # Solving this reversed shortest path problem will give us our heuristic,
        # as it estimates the minimal cost of reaching an end state from each state
        class ReverseShortestPathProblem(SearchProblem):
            def startState(self) -> State:
                """
                Return special "END" state
                """
                # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
                return State(location="dum")
                # END_YOUR_CODE

            def isEnd(self, state: State) -> bool:
                """
                Return False for each state.
                Because there is *not* a valid end state (`isEnd` always returns False), 
                UCS will exhaustively compute costs to *all* other states.
                """
                # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
                return False
                # END_YOUR_CODE

            def actionSuccessorsAndCosts(
                self, state: State
            ) -> List[Tuple[str, State, float]]:
                # If current location is the special "END" state, 
                # return all the locations with the desired endTag and cost 0 
                # (i.e, we connect the special location "END" with cost 0 to all locations with endTag)
                # Else, return all the successors of current location and their corresponding distances according to the cityMap
                # BEGIN_YOUR_CODE (our solution is 14 lines of code, but don't worry if you deviate from this)
                ls = []
                if state.location == "dum":
                    for i, u in cityMap.tags.items():
                        if endTag in u:
                            ls.append((i, State(location=i),0 ))
                else:
                    for neighbor, cost in cityMap.distances.get(
                                                state.location, {}
                                            ).items():
                        ls.append((neighbor, State(location=neighbor), cost))
                return ls
                    
                # END_YOUR_CODE

        # Call UCS.solve on our `ReverseShortestPathProblem` instance. Because there is
        # *not* a valid end state (`isEnd` always returns False), will exhaustively
        # compute costs to *all* other states.

        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        ucs =  UniformCostSearch()
        ucs.solve(problem=ReverseShortestPathProblem())
        # END_YOUR_CODE

        # Now that we've exhaustively computed costs from any valid "end" location
        # (any location with `endTag`), we can retrieve `ucs.pastCosts`; this stores
        # the minimum cost path to each state in our state space.
        #   > Note that we're making a critical assumption here: costs are symmetric!

        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        self.ucs = ucs.pastCosts
        # END_YOUR_CODE

    def evaluate(self, state: State) -> float:
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return self.ucs[state.location]
        raise Exception("Not implemented yet")
        # END_YOUR_CODE
