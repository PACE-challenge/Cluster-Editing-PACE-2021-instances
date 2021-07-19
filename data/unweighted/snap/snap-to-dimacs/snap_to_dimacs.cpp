#include "graph.hpp"

int main(int ac, char *av[]) {

	akt::graph g = akt::parse_snap(std::cin);
	akt::to_dimacs(std::cout, g);

	return 0;
}

