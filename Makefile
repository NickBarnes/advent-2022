.PHONY: all
all: $(foreach dir,$(sort $(wildcard [012]*)),day-$(dir))

.PHONY: day-%
day-%: %/go.py %/test*.txt %/input.txt
	for f in $(wildcard $*/test*.txt); do time python3 $*/go.py $$f; done
	time python3 $*/go.py $*/input.txt

.PHONY: clean
clean:
	rm -rf *~ */*~ */__pycache__


