"""Stage 9's test of spectral sampling: the coarse grid and its sampled cross-sections."""
import numpy as np
import pytest

from atmosphere.waterworlds import radiating as rd, sampling as sa, steam, steam_optics as so
from atmosphere.waterworlds.body import Waterworld


class _Grey:
    """A grey column: the same cross-section at every wavenumber, so that any grid gives the same heights."""
    def layer_cross_sections(self, col, band):
        nu = band.grid.nu
        return nu, np.full((len(col['layer_p_pa']), nu.size), 1e-24)


def test_the_coarse_grid_runs_from_1_cm_to_five_wien_peaks_in_5000_points():
    nu = sa.coarse_grid(400.0)
    assert nu.size == 5000 and nu[0] == 1.0 and nu[-1] == pytest.approx(5 * 1.960998 * 400.0, rel=1e-6)


def test_a_grey_column_emits_from_the_same_height_on_either_grid():
    col = steam.column(Waterworld(0.12), 400.0, steam.Levels(top_pa=1e-2, per_decade=5), optical_gravity='surface')
    sampled = sa.Sampled(_Grey(), sa.coarse_grid(400.0))
    nu, sigma = sampled.layer_cross_sections(col)
    assert nu.size == 5000 and np.all(sigma == 1e-24)
    coarse = rd.surfaces(col, rd.column_spectra(col, sampled, (None,)))
    full = rd.surfaces(col, rd.column_spectra(col, _Grey(), so.BANDS))
    assert coarse['z_lw'] == pytest.approx(full['z_lw'], rel=1e-9)
    with pytest.raises(ValueError):
        sa.Sampled(_Grey(), np.array([30000.0])).layer_cross_sections(col)
