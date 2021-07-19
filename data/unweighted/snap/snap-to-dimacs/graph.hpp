#pragma once
#include <iostream>
#include <set>
#include <random>
#include <unordered_map>

namespace akt {
struct neighbor;
template<class T>
struct list_iterator {

	list_iterator() {}
	list_iterator(T* e) :e(e) {}

	list_iterator& operator++() {
		e = e->next;	
		return *this;
	}

	T& operator*() {
		return *e;	
	}
	const T& operator*() const {
		return *e;	
	}
	T* operator->() {
		return e;	
	}
	const T* operator->() const {
		return e;	
	}
	bool operator==(const list_iterator<T>& rhs) const  { return e == rhs.e; } 
	bool operator!=(const list_iterator<T>& rhs) const { return !(e == rhs.e); }
	private:
		T* e = nullptr;

};
struct adjacenylist {

	void add(neighbor* v);
	list_iterator<neighbor> begin();
	list_iterator<neighbor> end();
	void remove(neighbor& n);
		
	const list_iterator<neighbor> begin() const;
	const list_iterator<neighbor> end() const;
	neighbor* last() { return _last; }
	const neighbor* last() const { return _last; }
	private:
	neighbor* first = nullptr;
	neighbor* _last = nullptr;
};

struct vertex {
	unsigned int id;
	unsigned int degree = 0;
	adjacenylist neighbors;
};

struct edge;
struct neighbor {
	unsigned int id;
	edge *e;
	neighbor* prev = nullptr;
	neighbor* next = nullptr;

	neighbor* complement(); 

};


struct edge {
	neighbor x, y;
	edge *prev = nullptr;
	edge *next = nullptr;
};

struct edgelist {

	edgelist(size_t M) : list(M) {}

	void add(unsigned int source, unsigned int target) {

		if(counter == list.size()) throw "added too many edges";

		list[counter].x.id = source;
		list[counter].x.e = &list[counter];
		list[counter].y.id = target;
		list[counter].y.e = &list[counter];

		if(first) {
			list[counter].prev = _last;
			_last->next = &list[counter];
		} else {
			first = &list[counter];
		}

		_last = &list[counter];
		counter++;
		num_of_edges++;

	}

	void remove(edge& e) {
		if(e.prev == nullptr) {
			first = e.next;
		} else {
			e.prev->next = e.next;
		}

		if(e.next == nullptr) {
			_last = e.prev;
		} else {
			e.next->prev = e.prev;
		}
		num_of_edges--;
	}

	list_iterator<edge> begin() {
		return list_iterator<edge>(first);

	}
	list_iterator<edge> end() {
		return list_iterator<edge>();
	}

	const list_iterator<edge> begin() const {
		return list_iterator<edge>(first);

	}
	const list_iterator<edge> end() const {
		return list_iterator<edge>();
	}

	size_t M() const { return num_of_edges; }

	edge* last() { return _last; }

      private:
		size_t num_of_edges = 0;
	      std::vector<edge> list;
	      unsigned int counter = 0;
	      edge* first = nullptr;
	      edge* _last = nullptr;
};



struct graph {

	graph(unsigned int N, unsigned int M) :edges(M), vertices(N) {
		//set the ids
		for(size_t i = 0 ; i < N ; i++) {
			vertices[i].id = i;
		}
	}


	void add_edge(unsigned int source, unsigned int target) {
		edges.add(source, target);
		vertices[source].neighbors.add(&edges.last()->y);
		vertices[source].degree++;
		vertices[target].neighbors.add(&edges.last()->x);
		vertices[target].degree++;
	}

	void remove_edge(edge& e) {
		edges.remove(e);
		vertices[e.x.id].neighbors.remove(e.y);
		vertices[e.y.id].neighbors.remove(e.x);
		vertices[e.x.id].degree--;
		vertices[e.y.id].degree--;
	}

	vertex& get_vertex(unsigned int id) {
		return vertices[id];
	}
	const vertex& get_vertex(unsigned int id) const{
		return vertices[id];
	}
	

	const vertex& operator[](unsigned int id) const {
		return get_vertex(id);
	}
	vertex& operator[](unsigned int id) {
		return get_vertex(id);
	}

	const edgelist& edgeset() const { return edges; }
	unsigned int N() const { return vertices.size(); }

	std::vector<vertex>::iterator begin() { return vertices.begin(); }
	std::vector<vertex>::iterator end() { return vertices.end(); }

	void isolate_vertex(unsigned int id) {
		for(auto& v : vertices[id].neighbors) {
			remove_edge(*v.e);
		}
	}
	private:

	edgelist edges;
	std::vector<vertex> vertices;

};

template<class IStream>
graph parse_snap(IStream&in) {

	std::string first, second;
	std::unordered_map<size_t, size_t> names;
	size_t counter = 0;

	std::vector<std::set<size_t>> edges;


	while (std::getline(in, first) && first.size() > 0 && first[0] == '#')
		; // read comments
	auto i = first.find_first_of(" \t");
	second = first.substr(i + 1);
	first = first.substr(0, i);
	do {
		size_t v = std::atoi(first.c_str());
		size_t w = std::atoi(second.c_str());
		auto iter = names.find(v);
		if (iter != names.end())
			v = iter->second;
		else {

			names[v] = counter;
			v = counter;
			counter++;
			edges.push_back(std::set<size_t>());
		}
		iter = names.find(w);
		if (iter != names.end())
			w = iter->second;
		else {

			names[w] = counter;
			w = counter;
			counter++;
			edges.push_back(std::set<size_t>());
		}
		if(v > w) {
			std::swap(v,w);
		}

		if(v != w) {
			edges[v].insert(w);
		}
	} while (in >> first >> second);

	size_t m = 0;
	for(auto& i : edges) {
		m += i.size();
	}
	graph g(counter, m);
	for(int v = 0; v < edges.size(); v++) {
		for(auto w : edges[v]) {
			g.add_edge(v, w);
		}
	}
	return g;
}

template<class OStream>
OStream& to_dimacs(OStream& os, const graph& g) {
	os << "p " << g.N() << ' ' << g.edgeset().M() << std::endl;
	for(auto& e : g.edgeset()) {
		os << "e " << std::min(e.x.id, e.y.id)+1 << ' ' << std::max(e.x.id, e.y.id)+1 << std::endl;
	}
	return os;
}

}
