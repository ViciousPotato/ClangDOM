test:
	LD_LIBRARY_PATH=`llvm-config --libdir` python tests/test.py