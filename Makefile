# Every check: `make check`. Each target also runs on its own.
PYTHON ?= python3
export OPENBLAS_NUM_THREADS ?= 1

.PHONY: check check-patches

check: check-patches

# Each patch series applied to its pinned upstream source reproduces the deployed sources (upstream/ is
# ignored by Git; see models/pins.sha256 for what it must hold).
check-patches:
	models/check_patches.sh
