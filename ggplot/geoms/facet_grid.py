from copy import deepcopy
import math

class facet_grid(object):
    def __init__(self, x=None, y=None, ncol=None, nrow=None, scales=None):
        self.x = x
        self.y = y
        self.ncol = ncol
        self.nrow = nrow
        self.scales = scales

    def __radd__(self, gg):

        x = gg.data.get(self.x)
        y = gg.data.get(self.y)
        if x is None:
            n_dim_x = 1
        else:
            n_dim_x = x.nunique()
        if y is None:
            n_dim_y = 1
        else:
            n_dim_y = y.nunique()
        
        n_dim = n_dim_x * n_dim_y
        if self.ncol is None and self.nrow is None:
            n_wide = n_dim_x
            n_high = n_dim_y
        elif self.nrow is None:
            n_wide = self.ncol
            n_high = math.ceil(float(n_dim) / n_wide)
        elif self.ncol is None:
            n_high = self.nrow
            n_wide = math.ceil(float(n_dim) / n_high)
        else:
            n_wide = self.ncol
            n_high = self.nrow

        gg.n_wide, gg.n_high = int(n_wide), int(n_high)

        facets = []
        if self.x:
            facets.append(self.x)
        if self.y:
            facets.append(self.y)
        gg.facets = facets
        gg.facet_type = "grid"
        gg.facet_scales = self.scales

        combos = []
        for x_i in sorted(x.unique()):
            for y_i in sorted(y.unique()):
                combos.append((x_i, y_i))
        gg.facet_pairs = combos

        return deepcopy(gg)
