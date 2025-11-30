all:
	@mkdir -p bench/build
	@cd bench/build && cmake .. && make -j$(nproc)
	@echo "Build OK"
	@echo "Bin: cpp/bench/build/benchmark"

run:
	@./bench/build/benchmark

clean:
	@rm -rf bench/build
	@echo "Clean OK"
