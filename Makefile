run:
	docker compose run networkx
view:
	open out.png

clean:
	rm -f out.png
	rm -f test.dot
	rm -f test.gml
