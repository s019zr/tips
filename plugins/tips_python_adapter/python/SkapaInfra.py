#! /usr/bin/env python
# coding:iso-8859-15 
# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228

from __future__ import generators
import sys

class priorityDictionary(dict):
	def __init__(self):
		'''Initialize priorityDictionary by creating binary heap of pairs (value,key).
Note that changing or removing a dict entry will not remove the old pair from the heap
until it is found by smallest() or until the heap is rebuilt.'''
		self.__heap = []
		dict.__init__(self)

	def smallest(self):
		'''Find smallest item after removing deleted items from front of heap.'''
		if len(self) == 0:
			raise IndexError, "smallest of empty priorityDictionary"
		heap = self.__heap
		while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
			lastItem = heap.pop()
			insertionPoint = 0
			while 1:
				smallChild = 2*insertionPoint+1
				if smallChild+1 < len(heap) and heap[smallChild] > heap[smallChild+1] :
					smallChild += 1
				if smallChild >= len(heap) or lastItem <= heap[smallChild]:
					heap[insertionPoint] = lastItem
					break
				heap[insertionPoint] = heap[smallChild]
				insertionPoint = smallChild
		return heap[0][1]
	
	def __iter__(self):
		'''Create destructive sorted iterator of priorityDictionary.'''
		def iterfn():
			while len(self) > 0:
				x = self.smallest()
				yield x
				del self[x]
		return iterfn()
	
	def __setitem__(self,key,val):
		'''Change value stored in dictionary and add corresponding pair to heap.
Rebuilds the heap if the number of deleted items gets large, to avoid memory leakage.'''
		dict.__setitem__(self,key,val)
		heap = self.__heap
		if len(heap) > 2 * len(self):
			self.__heap = [(v,k) for k,v in self.iteritems()]
			self.__heap.sort()  # builtin sort probably faster than O(n)-time heapify
		else:
			newPair = (val,key)
			insertionPoint = len(heap)
			heap.append(None)
			while insertionPoint > 0 and newPair < heap[(insertionPoint-1)//2]:
				heap[insertionPoint] = heap[(insertionPoint-1)//2]
				insertionPoint = (insertionPoint-1)//2
			heap[insertionPoint] = newPair
	
	def setdefault(self,key,val):
		'''Reimplement setdefault to pass through our customized __setitem__.'''
		if key not in self:
			self[key] = val


def Dijkstra(G,start,end=None):
	"""
	Find shortest paths from the  start vertex to all vertices nearer than or equal to the end.
	The input graph G is assumed to have the following representation:
	A vertex can be any object that can be used as an index into a dictionary.
	G is a dictionary, indexed by vertices.  For any vertex v, G[v] is itself a dictionary,
	indexed by the neighbors of v.  For any edge v->w, G[v][w] is the length of the edge.
	This is related to the representation in <http://www.python.org/doc/essays/graphs.html>
	where Guido van Rossum suggests representing graphs as dictionaries mapping vertices
	to lists of outgoing edges, however dictionaries of edges have many advantages over lists:
	they can store extra information (here, the lengths), they support fast existence tests,
	and they allow easy modification of the graph structure by edge insertion and removal.
	Such modifications are not needed here but are important in many other graph algorithms.
	Since dictionaries obey iterator protocol, a graph represented as described here could
	be handed without modification to an algorithm expecting Guido's graph representation.
	Of course, G and G[v] need not be actual Python dict objects, they can be any other
	type of object that obeys dict protocol, for instance one could use a wrapper in which vertices
	are URLs of web pages and a call to G[v] loads the web page and finds its outgoing links.
	
	The output is a pair (D,P) where D[v] is the distance from start to v and P[v] is the
	predecessor of v along the shortest path from s to v.
	
	Dijkstra's algorithm is only guaranteed to work correctly when all edge lengths are positive.
	This code does not verify this property for all edges (only the edges examined until the end
	vertex is reached), but will correctly compute shortest paths even for some graphs with negative
	edges, and will raise an exception if it discovers that a negative edge has caused it to make a mistake.
	"""

	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()	# estimated distances of non-final vertices
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					raise ValueError, "Dijkstra: found better path to already-final vertex"
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	
	return (D,P)
			
def shortestPath(G,start,end):
	"""
	Find a single shortest path from the given start vertex to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along the shortest path.
	"""

	D,P = Dijkstra(G,start,end)
	Dist = D[end]
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return (Dist,Path)

def distint(text):
  if text.isdigit():
    return text
  else:
    ik = 0
    for i in range(len(text)):
      if text[i].isdigit():
        ik = ik + 1
      else:
        break
    if ik > 0:
      return text[0:ik]
  return '0'

def komma_int(tal_str):
  if tal_str.find(',') > -1:
    tal = tal_str[0:tal_str.find(',')]
  elif tal_str.find('.') > -1:
    tal = tal_str[0:tal_str.find('.')]
  else:
    tal = tal_str
  if len(tal) == 0:
    tal = '0'
  return int(float(tal)+.5)

if __name__ == '__main__':
  Loc_dic = {}
  Rtl_dic = {}
  Sign_lista = []
  input = open(sys.argv[1],'r')
  lines = input.readlines()
  for linetemp in lines:
    line = linetemp.strip()
    if line[0:3] == 'LOC':
      line_list = line.split(chr(9))
      land = line_list[23]
      i = line_list[2].find('.')
      if i > 0:
        sign = line_list[2][i + 1:]
        land = line_list[2][0:i]
      else:
        sign = line_list[2]
      namn = line_list[3]
      RTo = line_list[6]
      RTn = line_list[7]
      typ = line_list[9]
      aegare = line_list[10]
      Sign_lista.append((sign,land))
      Loc_dic[(sign,land)] = (namn,RTo,RTn,typ,aegare,[])
    if line[0:3] == 'RTL':
      line_list = line.split(chr(9))
      temp = line_list[2]
      i = temp.find('.')
      if i > 0:
        land1 = temp[0:i]
        sign1 = temp[i + 1:]
      else:
        land1 = 'SE'
        sign1 = temp
      temp = line_list[3]
      i = temp.find('.')
      if i > 0:
        land2 = temp[0:i]
        sign2 = temp[i + 1:]
      else:
        land2 = 'SE'
        sign2 = temp
      fran = (sign1,land1)
      till = (sign2,land2)
      dist = line_list[6]
      Rtl_dic[(fran,till)] = int(dist)
      if till in Loc_dic[fran][5]:
        pass
      else:
        Loc_dic[fran][5].append(till)
      if fran in Loc_dic[till][5]:
        pass
      else:
        Loc_dic[till][5].append(fran)
#  for stn in Loc_dic.keys():
#    print stn,Loc_dic[stn]
#  for rtl in Rtl_dic.keys():
#    print rtl,Rtl_dic[rtl]

G = {}
for key in Loc_dic.keys():
  temp = {}
  for nyk in Loc_dic[key][5]:
    dist = Rtl_dic[(key,nyk)]    
    temp[nyk] = dist
  if temp.keys() > 0:
    G[key] = temp
#print '*********************************************'
#print G
kalle =  Dijkstra(G,("CST","SE"))
slut = ("CST","SE")
#print '*********************************************'
#print kalle
#print '*********************************************'
    
print kalle[0][('G','SE')]
print '*********************************************'
start = ('G','SE')
print start[0],start[1],kalle[0][start]
while start in kalle[1].keys():
  start = kalle[1][start]
  if start == slut:
    print slut[0],slut[1],0
  else:
    print kalle[1][start][0],kalle[1][start][1],kalle[0][start]