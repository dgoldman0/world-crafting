#!/usr/bin/env bash
# Apply every patch series to a pristine copy of its pinned upstream source and compare the result with
# the recorded hashes (the sources Terluna compiled). Nothing is compiled.
#
#   models/check_patches.sh [UPSTREAM_DIR]      # default: ./upstream (ignored by Git)
#
# UPSTREAM_DIR holds the files named in models/pins.sha256: the ExoPlaSim, CM1, SWAN and SWASH archives
# and WRF-ELEC's three files under wrf4-elec/. A missing file is reported as BLOCKED, never skipped silently.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
UP="$(cd "${1:-$HERE/../upstream}" 2>/dev/null && pwd)" || { echo "BLOCKED: no upstream folder"; exit 2; }
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
status=0
fail() { echo "FAIL: $*"; status=1; }

echo "== pins"
missing=0
while read -r sum name; do
    if [ ! -e "$UP/$name" ]; then echo "BLOCKED: $name missing"; missing=1; continue; fi
    [ "$(sha256sum "$UP/$name" | cut -d' ' -f1)" = "$sum" ] && echo "ok  $name" || fail "$name differs from its pin"
done < "$HERE/pins.sha256"

apply_series() {   # apply_series <patch-dir-root> <series-file>...
    local root=$1; shift
    for s in "$@"; do
        while read -r p; do
            [ -z "$p" ] && continue
            patch -p1 --quiet --no-backup-if-mismatch < "$root/$p" || { fail "$p does not apply"; return 1; }
        done < "$s"
    done
}

echo "== ExoPlaSim 3.4.2"
if [ -e "$UP/exoplasim-3.4.2.tar.gz" ]; then
    mkdir -p "$TMP/exo" && tar -xzf "$UP/exoplasim-3.4.2.tar.gz" -C "$TMP/exo" \
        exoplasim-3.4.2/exoplasim/plasim/src/radmod.f90 exoplasim-3.4.2/exoplasim/plasim/src/rainmod.f90
    ( cd "$TMP/exo/exoplasim-3.4.2/exoplasim" && sed 's|^|patches/|' "$HERE/exoplasim/patches/series" > "$TMP/exo.series" \
      && apply_series "$HERE/exoplasim" "$TMP/exo.series" && sha256sum -c --quiet "$HERE/exoplasim/expected.sha256" ) \
      && echo "ok  10 patches; radmod.f90 and rainmod.f90 match the deployed copy" || fail "ExoPlaSim series"
fi

echo "== CM1 r22.0"
if [ -e "$UP/cm1r22.0.tar.gz" ]; then
    tar -xzf "$UP/cm1r22.0.tar.gz" -C "$TMP" cm1r22.0/src
    C="$HERE/cm1"
    while read -r want label; do
        R="$TMP/cm1-$label"; cp -r "$TMP/cm1r22.0" "$R"
        (
            cd "$R" || exit 1
            case $label in moon|earth_g) mk=makefile-gnu-mpi.patch ;; *) mk=makefile-gnu-omp.patch ;; esac
            patch -p1 --quiet < "$C/patches/$mk" || exit 1
            extra=()
            case $label in
                *terrain_sea_twilight) extra=(series-terrain series-sea series-twilight) ;;
                *terrain_sea) extra=(series-terrain series-sea) ;;
                *terrain) extra=(series-terrain) ;;
                *twilight) extra=(series-twilight) ;;
                *earth_fall) extra=(series-earth-fall) ;;
                *elec)
                    [ -e "$UP/wrf4-elec/module_mp_nssl_2mom_elec.F" ] || { echo "BLOCKED: WRF-ELEC files"; exit 3; }
                    cp "$UP/wrf4-elec/module_mp_nssl_2mom_elec.F" src/module_mp_nssl_2mom.F
                    cp "$UP/wrf4-elec/module_discharge_msz.F" src/
                    cp "$C/fortran/"*.F src/
                    extra=(series-elec) ;;
            esac
            apply_series "$C" "$C/series-core" "${extra[@]/#/$C/}" || exit 1
            case $label in moon|earth_g) ;; *) patch -p1 --quiet < "$C/patches/makefile-omp-O3-march-native.patch" || exit 1 ;; esac
            got=$( (cd src && sha256sum *.F Makefile | sort -k2) | sha256sum | cut -d' ' -f1)
            [ "$got" = "$want" ]
        ) && echo "ok  $label" || fail "CM1 $label"
    done < "$C/expected.sha256"
fi

echo "== SWAN 41.51"
if [ -e "$UP/swan4151.tar.gz" ] && [ -f "$HERE/swan/patches/series" ]; then
    mkdir -p "$TMP/swan" && tar -xzf "$UP/swan4151.tar.gz" -C "$TMP/swan"
    src=$(dirname "$(find "$TMP/swan" -name swancom3.ftn | head -1)")
    ( cd "$src" && sed 's|^|patches/|' "$HERE/swan/patches/series" > "$TMP/swan.series" \
      && apply_series "$HERE/swan" "$TMP/swan.series" \
      && { [ ! -f "$HERE/swan/expected.sha256" ] || sha256sum -c --quiet "$HERE/swan/expected.sha256"; } ) \
      && echo "ok  SWAN patches" || fail "SWAN series"
fi

[ $missing -eq 1 ] && [ $status -eq 0 ] && exit 2
exit $status
