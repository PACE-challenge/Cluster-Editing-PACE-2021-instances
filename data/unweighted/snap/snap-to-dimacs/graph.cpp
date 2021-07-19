#include "graph.hpp"

namespace akt {
void adjacenylist::add(neighbor *v) {
	if (first) {
		_last->next = v;
		v->prev = _last;
	} else {
		first = v;
	}
	_last = v;
}
list_iterator<neighbor> adjacenylist::begin() { return list_iterator<neighbor>(first); }
list_iterator<neighbor> adjacenylist::end() { return list_iterator<neighbor>(); }
const list_iterator<neighbor> adjacenylist::begin() const { return list_iterator<neighbor>(first); }
const list_iterator<neighbor> adjacenylist::end() const { return list_iterator<neighbor>(); }

void adjacenylist::remove(neighbor &n) {
	if (n.prev == nullptr) {
		first = n.next;
	} else {
		n.prev->next = n.next;
	}

	if (n.next == nullptr) {
		_last = n.prev;
	} else {
		n.next->prev = n.prev;
	}
}

neighbor* neighbor::complement() {
		if(e->x.id == id) {
			return &e->y;
		} else {
			return &e->x;
		}
	}

} /* namespace akt */
