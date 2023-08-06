#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : mixing.py
# License: GNU v3.0
# Author : Andrei Leonard Nicusan <a.l.nicusan@bham.ac.uk>
# Date   : 24.08.2022


import  os
import  textwrap
from    numbers             import  Number


import  numpy               as      np
import  scipy
from    scipy.interpolate   import  interp1d

from    tqdm                import  tqdm
from    joblib              import  Parallel, delayed

from    pept                import  PointData, Voxels
from    pept.base           import  Reducer
from    pept                import  plots

from    plotly.subplots     import  make_subplots
import  plotly.graph_objs   as      go




def enlarge(lim):
    '''Correctly enlarge two limits, e.g. [xmin, xmax]
    '''
    eps = np.finfo(float).resolution
    lim = lim.copy()

    if lim[0] < 0:
        lim[0] = lim[0] * 1.0001 - eps
    else:
        lim[0] = lim[0] * 0.9999 - eps

    if lim[1] < 0:
        lim[1] = lim[1] * 0.9999 + eps
    else:
        lim[1] = lim[1] * 1.0001 + eps

    return lim




def _check_point3d(**kwargs):
    # Extract first argument
    for name, point in kwargs.items():
        break

    if point.ndim != 1 or len(point) != 3:
        raise ValueError(textwrap.fill((
            f"The input point `{name}` should be a vector-like with exactly 3 "
            f"elements. Received `{point}`."
        )))




def _parallel(f, samples, executor, max_workers, desc = "", verbose = True):
    if executor == "sequential":
        if verbose:
            samples = tqdm(samples, desc = desc)

        return [f(s) for s in samples]

    elif executor == "joblib":
        if verbose:
            samples = tqdm(samples, desc = desc)

        # Joblib's `max_workers` behaviour is different than for Executors.
        # The latter simply sets the maximum number of threads available,
        # while the former uses a max_worker=1. Make behaviour consistent.
        if max_workers is None:
            max_workers = os.cpu_count()

        return Parallel(n_jobs = max_workers)(delayed(f)(s) for s in samples)

    else:
        # Otherwise assume `executor` is a `concurrent.futures.Executor`
        # subclass (e.g. ProcessPoolExecutor, MPIPoolExecutor).
        with executor(max_workers = max_workers) as exe:
            futures = [exe.submit(f, s) for s in samples]

            if verbose:
                futures = tqdm(futures, desc = desc)

            return [fut.result() for fut in futures]




class LaceyColors(Reducer):
    '''Compute Lacey-like mixing image, with streamlines passing through plane
    1 being split into Red and Blue tracers, then evaluated into RGB pixels at
    a later point in plane 2.

    Intuitively, red and blue pixels will contain unmixed streamlines, while
    purple pixels will indicate mixing.

    Reducer signature:

    ::

               PointData -> LaceyColors.fit -> (height, width, 3) pept.Voxels
         list[PointData] -> LaceyColors.fit -> (height, width, 3) pept.Voxels
        list[np.ndarray] -> LaceyColors.fit -> (height, width, 3) pept.Voxels

    **Each sample in the input `PointData` is treated as a separate streamline
    / tracer pass. You can group passes using `Segregate + GroupBy("label")`**.

    The first plane where tracers are split into Red and Blue streamlines is
    defined by a point `p1` and direction axis `ax1`. **The point `p1` should
    be the middle of the pipe**.

    The second plane where mixing is evaluated is similarly defined by `p2` and
    `ax2`. **The point `p2` should be the middle of the volume / pipe**.

    If the direction vectors `ax1` and `ax2` are undefined (`None`), the
    tracers are assumed to follow a straight line between `p1` and `p2`.

    The `max_distance` parameter defines the maximum distance allowed between
    a point and a plane to be considered part of it. The `resolution` defines
    the number of pixels in the height and width of the resulting image.

    *New in pept-0.5.1*

    Examples
    --------
    Consider a pipe-flow experiment, with tracers moving from side to side in
    multiple passes / streamlines. First locate the tracers, then split their
    trajectories into each individual pass:

    >>> import pept
    >>> from pept.tracking import *
    >>>
    >>> split_pipe = pept.Pipeline([
    >>>     Segregate(window = 10, max_distance = 20),  # Appends label column
    >>>     GroupBy("label"),                           # Splits into samples
    >>>     Reorient(),                                 # Align with X axis
    >>>     Center(),                                   # Center points at 0
    >>>     Stack(),
    >>> ])
    >>> streamlines = split_pipe.fit(trajectories)

    Now each sample in `streamlines` corresponds to a single tracer pass, e.g.
    `streamlines[0]` is the first pass, `streamlines[1]` is the second. The
    passes were reoriented and centred such that the pipe is aligned with the
    X axis.

    Now the `LaceyColors` reducer can be used to create an image of the mixing
    between the pipe entrance and exit:

    >>> from pept.processing import LaceyColors
    >>> entrance = [-100, 0, 0]     # Pipe data was aligned with X and centred
    >>> exit = [100, 0, 0]
    >>> lacey_image = LaceyColors(entrance, exit).fit(streamlines)
    >>> print(lacey_image.voxels)    # RGB channels of image
    (8, 8, 3)

    Now the image can be visualised e.g. with Plotly:

    >>> from pept.plots import PlotlyGrapher2D
    >>> PlotlyGrapher2D().add_image(lacey_image).show()
    '''

    def __init__(
        self,
        p1,
        p2,
        ax1 = None,
        ax2 = None,
        basis1 = None,
        basis2 = None,
        xlim = None,
        ylim = None,
        max_distance = 10,
        resolution = (8, 8),
    ):
        self.p1 = np.asarray(p1, dtype = float)
        _check_point3d(p1 = self.p1)

        if ax1 is not None:
            ax1 = np.asarray(ax1, dtype = float)
            ax1 = ax1 / np.linalg.norm(ax1)
            _check_point3d(ax1 = ax1)
        self.ax1 = ax1

        self.p2 = np.asarray(p2, dtype = float)
        _check_point3d(p2 = self.p2)

        if ax2 is not None:
            ax2 = np.asarray(ax2, dtype = float)
            ax2 = ax2 / np.linalg.norm(ax2)
            _check_point3d(ax2 = ax2)
        self.ax2 = ax2

        if basis1 is not None:
            basis1 = np.asarray(basis1, dtype = float)
            if basis1.ndim != 2 or len(basis1) != 3 or basis1.shape[1] != 2:
                raise ValueError(textwrap.fill((
                    "The input `basis1`, if defined, should be two column "
                    "vectors - i.e. a (3, 2) matrix. Received "
                    f"`basis1.shape={basis1.shape}`."
                )))
        self.basis1 = basis1

        if basis2 is not None:
            basis2 = np.asarray(basis2, dtype = float)
            if basis2.ndim != 2 or len(basis2) != 3 or basis2.shape[1] != 2:
                raise ValueError(textwrap.fill((
                    "The input `basis2`, if defined, should be two column "
                    "vectors - i.e. a (3, 2) matrix. Received "
                    f"`basis2.shape={basis2.shape}`."
                )))
        self.basis2 = basis2

        if xlim is not None:
            xlim = np.asarray(xlim, dtype = float)
            if xlim.ndim != 1 or len(xlim) != 2:
                raise ValueError(textwrap.fill((
                    "The input `xlim`, if given, should be a vector-like with "
                    f"two values [xmin, xmax]. Received `{xlim}`."
                )))
        self.xlim = xlim

        if ylim is not None:
            ylim = np.asarray(ylim, dtype = float)
            if ylim.ndim != 1 or len(ylim) != 2:
                raise ValueError(textwrap.fill((
                    "The input `ylim`, if given, should be a vector-like with "
                    f"two values [ymin, ymax]. Received `{ylim}`."
                )))
        self.ylim = ylim

        self.max_distance = float(max_distance)
        self.resolution = tuple(resolution)


    def fit(
        self,
        trajectories,
        executor = "joblib",
        max_workers = None,
        verbose = True,
    ):

        if not isinstance(trajectories, PointData):
            try:
                trajectories = PointData(trajectories)
            except (ValueError, TypeError):
                raise TypeError(textwrap.fill((
                    "The input `trajectories` must be pept.PointData-like. "
                    f"Received `{type(trajectories)}`."
                )))

        if self.ax1 is None:
            self.ax1 = self.p2 - self.p1

        if self.ax2 is None:
            self.ax2 = self.p2 - self.p1

        self.ax1 = self.ax1 / np.linalg.norm(self.ax1)
        self.ax2 = self.ax2 / np.linalg.norm(self.ax2)

        # Aliases
        p1 = self.p1
        ax1 = self.ax1
        p2 = self.p2
        ax2 = self.ax2

        max_distance = self.max_distance
        resolution = self.resolution

        # For each pass, find the closest point to the start and end planes
        points_start = []
        points_end = []

        for traj in trajectories:
            xyz = traj.points[:, 1:4]
            xyz = xyz[np.isfinite(xyz).all(axis = 1)]

            dists_start = np.abs(np.dot(xyz - p1, ax1))
            dists_end = np.abs(np.dot(xyz - p2, ax2))

            min_dist_start = np.min(dists_start)
            min_dist_end = np.min(dists_end)

            if min_dist_start < max_distance and min_dist_end < max_distance:
                points_start.append(xyz[np.argmin(dists_start)])
                points_end.append(xyz[np.argmin(dists_end)])

        points_start = np.array(points_start)
        points_end = np.array(points_end)

        # Split starting points into two species - Red and Blue - along the PCA
        points_start_centred = points_start - p1

        if self.basis1 is None:
            cov = np.cov(points_start_centred.T)
            evals, evecs = np.linalg.eig(cov)

            evals_argsorted = evals.argsort()[::-1]
            evals = evals[evals_argsorted]
            self.basis1 = evecs[:, evals_argsorted][:, :2]

        points_start2d = points_start_centred @ self.basis1

        # Project ending points onto 2D plane by the Principal Components
        points_end_centred = points_end - p2

        if self.basis2 is None:
            cov = np.cov(points_end_centred.T)
            evals, evecs = np.linalg.eig(cov)

            evals_argsorted = evals.argsort()[::-1]
            evals = evals[evals_argsorted]
            self.basis2 = evecs[:, evals_argsorted][:, :2]

        points_end2d = points_end_centred @ self.basis2

        # Create RGB image with the R and B channels == the number of passes
        ired = points_start2d[:, 0] < 0
        iblu = points_start2d[:, 0] >= 0

        # Compute image physical limits
        limits = np.c_[points_end2d.min(axis = 0), points_end2d.max(axis = 0)]

        if self.xlim is None:
            self.xlim = enlarge(limits[0, :])

        if self.ylim is None:
            self.ylim = enlarge(limits[1, :])

        xlim = self.xlim
        ylim = self.ylim

        xsize = (xlim[1] - xlim[0]) / resolution[0]
        ysize = (ylim[1] - ylim[0]) / resolution[1]

        red_mix = np.zeros(resolution)
        blu_mix = np.zeros(resolution)

        # Find indices within pixels
        red_ix = ((points_end2d[ired, 0] - xlim[0]) / xsize).astype(int)
        red_iy = ((points_end2d[ired, 1] - ylim[0]) / ysize).astype(int)

        # Ensure all red pixel indices are within bounds
        mask = (
            (red_ix >= 0) & (red_ix < resolution[0]) &
            (red_iy >= 0) & (red_iy < resolution[1])
        )

        red_ix = red_ix[mask]
        red_iy = red_iy[mask]

        for i in range(len(red_ix)):
            red_mix[red_ix[i], red_iy[i]] += 1

        blu_ix = ((points_end2d[iblu, 0] - xlim[0]) / xsize).astype(int)
        blu_iy = ((points_end2d[iblu, 1] - ylim[0]) / ysize).astype(int)

        # Ensure all blue pixel indices are within bounds
        mask = (
            (blu_ix >= 0) & (blu_ix < resolution[0]) &
            (blu_iy >= 0) & (blu_iy < resolution[1])
        )

        blu_ix = blu_ix[mask]
        blu_iy = blu_iy[mask]

        for i in range(len(blu_ix)):
            blu_mix[blu_ix[i], blu_iy[i]] += 1

        # Stack RGB channels
        red_mix *= 255 / red_mix.max()
        blu_mix *= 255 / blu_mix.max()

        mix_img = np.zeros((resolution[0], resolution[1], 3), dtype = int)
        mix_img[:, :, 0] = red_mix.astype(int)
        mix_img[:, :, 2] = blu_mix.astype(int)

        return Voxels(
            mix_img,
            xlim = xlim,
            ylim = ylim,
            zlim = [0, 2],
        )




class LaceyColorsLinear(Reducer):
    '''Apply the `LaceyColors` mixing algorithm at `num_divisions` equidistant
    points between `p1` and `p2`, saving images at each step in `directory`.

    Reducer signature:

    ::

               PointData -> LaceyColors.fit -> (height, width, 3) np.ndarray
         list[PointData] -> LaceyColors.fit -> (height, width, 3) np.ndarray
        list[np.ndarray] -> LaceyColors.fit -> (height, width, 3) np.ndarray

    For details about the mixing algorithm itself, check the `LaceyColors`
    documentation.

    The generated images (saved in `directory` with `height` x `width` pixels)
    can be stitched into a video using `pept.plots.make_video`.

    *New in pept-0.5.1*

    Examples
    --------
    Consider a pipe-flow experiment, with tracers moving from side to side in
    multiple passes / streamlines. First locate the tracers, then split their
    trajectories into each individual pass:

    >>> import pept
    >>> from pept.tracking import *
    >>>
    >>> split_pipe = pept.Pipeline([
    >>>     Segregate(window = 10, max_distance = 20),  # Appends label column
    >>>     GroupBy("label"),                           # Splits into samples
    >>>     Reorient(),                                 # Align with X axis
    >>>     Center(),                                   # Center points at 0
    >>>     Stack(),
    >>> ])
    >>> streamlines = split_pipe.fit(trajectories)

    Now each sample in `streamlines` corresponds to a single tracer pass, e.g.
    `streamlines[0]` is the first pass, `streamlines[1]` is the second. The
    passes were reoriented and centred such that the pipe is aligned with the
    X axis.

    Now the `LaceyColorsLinear` reducer can be used to create images of the
    mixing between the pipe entrance and exit:

    >>> from pept.processing import LaceyColorsLinear
    >>> entrance = [-100, 0, 0]     # Pipe data was aligned with X and centred
    >>> exit = [100, 0, 0]
    >>> LaceyColorsLinear(
    >>>     directory = "lacey",    # Creates directory and saves images there
    >>>     p1 = entrance,
    >>>     p2 = exit,
    >>> ).fit(streamlines)

    Now the directory "lacey" was created inside your current working folder,
    and all Lacey images saved there as "frame0000.png", "frame0001.png", etc.
    You can stitch all images together into a video using
    `pept.plots.make_video`:

    >>> import pept
    >>> pept.plots.make_video("lacey/frame*.png", output = "lacey/video.avi")
    '''

    def __init__(
        self,
        directory,
        p1, p2,
        xlim = None,
        ylim = None,
        num_divisions = 50,
        max_distance = 10,
        resolution = (8, 8),
        height = 1000,
        width = 1000,
        prefix = "frame",
    ):
        self.directory = directory
        self.num_divisions = int(num_divisions)
        if self.num_divisions <= 1:
            raise ValueError(textwrap.fill((
                "The input `num_divisions` should be an integer >= 2. "
                f"Received `{self.num_divisions}`."
            )))

        self.p1 = np.asarray(p1, dtype = float)
        self.p2 = np.asarray(p2, dtype = float)

        self.xlim = xlim
        self.ylim = ylim

        self.max_distance = float(max_distance)
        self.resolution = tuple(resolution)

        self.height = int(height)
        self.width = int(width)
        self.prefix = prefix


    def fit(
        self,
        trajectories,
        executor = "joblib",
        max_workers = None,
        verbose = True,
    ):

        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

        divisions = np.c_[
            np.linspace(self.p1[0], self.p2[0], self.num_divisions),
            np.linspace(self.p1[1], self.p2[1], self.num_divisions),
            np.linspace(self.p1[2], self.p2[2], self.num_divisions),
        ]

        axis = self.p2 - self.p1

        # Compute basis vectors for splitting flow
        lacey = LaceyColors(
            p1 = divisions[0],
            p2 = divisions[1],
            ax1 = axis,
            ax2 = axis,
            max_distance = self.max_distance,
            resolution = self.resolution,
        )
        lacey.fit(trajectories)

        basis1 = lacey.basis1
        basis2 = lacey.basis2

        if self.xlim is None:
            self.xlim = lacey.xlim

        if self.ylim is None:
            self.ylim = lacey.ylim

        def compute_save_lacey(idiv):
            image = LaceyColors(
                p1 = self.p1,
                p2 = divisions[idiv],
                ax1 = axis,
                ax2 = axis,
                basis1 = basis1,
                basis2 = basis2,
                xlim = self.xlim,
                ylim = self.ylim,
                max_distance = self.max_distance,
                resolution = self.resolution,
            ).fit(trajectories)

            travelled = np.linalg.norm(divisions[idiv] - self.p1)
            grapher = plots.PlotlyGrapher2D(subplot_titles = [
                f"Travelled {travelled} mm"
            ])
            grapher.add_image(image)
            grapher.fig.write_image(
                f"{self.directory}/{self.prefix}{idiv:0>4}.png",
                height = self.height,
                width = self.width,
            )

        _parallel(
            compute_save_lacey,
            range(1, self.num_divisions),
            executor = executor,
            max_workers = max_workers,
            desc = "LaceyColorsLinear :",
            verbose = verbose,
        )




class RelativeDeviations(Reducer):
    '''Compute a Lagrangian mixing measure - the changes in tracer distances
    to a point P1 as they pass through an "inlet" plane and another point P2
    when reaching an "outlet" plane.

    A deviation is computed for each tracer trajectory, yielding a range of
    deviations that can e.g be histogrammed (default). Intuitively, mixing is
    stronger if this distribution of deviations is wider.

    Reducer signature:

    ::

        If ``histogram = True`` (default)
               PointData -> LaceyColors.fit -> plotly.graph_objs.Figure
         list[PointData] -> LaceyColors.fit -> plotly.graph_objs.Figure
        list[np.ndarray] -> LaceyColors.fit -> plotly.graph_objs.Figure

        If ``histogram = False`` (return deviations)
               PointData -> LaceyColors.fit -> (N,) np.ndarray
         list[PointData] -> LaceyColors.fit -> (N,) np.ndarray
        list[np.ndarray] -> LaceyColors.fit -> (N,) np.ndarray


    **Each sample in the input `PointData` is treated as a separate streamline
    / tracer pass. You can group passes using `Segregate + GroupBy("label")`**.

    The first plane where the distances from tracers to a point `p1` is defined
    by the point `p1` and direction axis `ax1`. **The point `p1` should be the
    middle of the pipe**.

    The second plane where relative distances are evaluated is similarly
    defined by `p2` and `ax2`. **The point `p2` should be the middle of the
    volume / pipe**.

    If the direction vectors `ax1` and `ax2` are undefined (`None`), the
    tracers are assumed to follow a straight line between `p1` and `p2`.

    The `max_distance` parameter defines the maximum distance allowed between
    a point and a plane to be considered part of it. The `resolution` defines
    the number of pixels in the height and width of the resulting image.

    The following attributes are always set. A Plotly figure is only generated
    and returned if `histogram = True` (default).

    The extra keyword arguments ``**kwargs`` are passed to the histogram
    creation routine `pept.plots.histogram`. You can e.g. set the YAxis limits
    by adding `ylim = [0, 20]`.

    *New in pept-0.5.1*

    Attributes
    ----------
    points1 : pept.PointData
        The tracer points selected at the inlet around `p1`.

    points2 : pept.PointData
        The tracer points selected at the outlet around `p2`.

    deviations : (N,) np.ndarray
        The vector of tracer deviations for each tracer pass in `points1` and
        `points2`.

    Examples
    --------
    Consider a pipe-flow experiment, with tracers moving from side to side in
    multiple passes / streamlines. First locate the tracers, then split their
    trajectories into each individual pass:

    >>> import pept
    >>> from pept.tracking import *
    >>>
    >>> split_pipe = pept.Pipeline([
    >>>     Segregate(window = 10, max_distance = 20),  # Appends label column
    >>>     GroupBy("label"),                           # Splits into samples
    >>>     Reorient(),                                 # Align with X axis
    >>>     Center(),                                   # Center points at 0
    >>>     Stack(),
    >>> ])
    >>> streamlines = split_pipe.fit(trajectories)

    Now each sample in `streamlines` corresponds to a single tracer pass, e.g.
    `streamlines[0]` is the first pass, `streamlines[1]` is the second. The
    passes were reoriented and centred such that the pipe is aligned with the
    X axis.

    Now the `RelativeDeviations` reducer can be used to create a histogram of
    tracer deviations due to mixing:

    >>> from pept.processing import RelativeDeviations
    >>> entrance = [-100, 0, 0]     # Pipe data was aligned with X and centred
    >>> exit = [100, 0, 0]
    >>> fig = RelativeDeviations(entrance, exit).fit(streamlines)
    >>> fig.show()

    The deviations themselves can be extracted directly for further processing:

    >>> mixing_algorithm = RelativeDeviations(entrance, exit, histogram=False)
    >>> mixing_algorithm.fit(streamlines)

    >>> deviations = mixing_algorithm.deviations
    >>> inlet_points = mixing_algorithm.points1
    >>> outlet_points = mixing_algorithm.points2
    '''

    def __init__(
        self,
        p1,
        p2,
        ax1 = None,
        ax2 = None,
        max_distance = 10,
        histogram = True,
        **kwargs,
    ):
        self.p1 = np.asarray(p1, dtype = float)
        _check_point3d(p1 = self.p1)

        if ax1 is not None:
            ax1 = np.asarray(ax1, dtype = float)
            self.ax1 = ax1 / np.linalg.norm(ax1)
            _check_point3d(ax1 = self.ax1)

        self.p2 = np.asarray(p2, dtype = float)
        _check_point3d(p2 = self.p2)

        if ax2 is not None:
            ax2 = np.asarray(ax2, dtype = float)
            self.ax2 = ax2 / np.linalg.norm(ax2)
            _check_point3d(ax2 = self.ax2)

        self.max_distance = float(max_distance)
        self.histogram = bool(histogram)

        self.kwargs = kwargs

        # Will be set in `fit`
        self.points1 = None
        self.points2 = None
        self.deviations = None


    def fit(
        self,
        trajectories,
        executor = "joblib",
        max_workers = None,
        verbose = True,
    ):

        if not isinstance(trajectories, PointData):
            try:
                trajectories = PointData(trajectories)
            except (ValueError, TypeError):
                raise TypeError(textwrap.fill((
                    "The input `trajectories` must be pept.PointData-like. "
                    f"Received `{type(trajectories)}`."
                )))

        if self.ax1 is None:
            self.ax1 = self.p2 - self.p1

        if self.ax2 is None:
            self.ax2 = self.p2 - self.p1

        self.ax1 = self.ax1 / np.linalg.norm(self.ax1)
        self.ax2 = self.ax2 / np.linalg.norm(self.ax2)

        # Aliases
        p1 = self.p1
        ax1 = self.ax1
        p2 = self.p2
        ax2 = self.ax2

        max_distance = self.max_distance

        # For each pass, find the closest point to the start and end planes
        points_start = []
        points_end = []

        for traj in trajectories:
            xyz = traj.points[:, 1:4]
            xyz = xyz[np.isfinite(xyz).all(axis = 1)]

            dists_start = np.abs(np.dot(xyz - p1, ax1))
            dists_end = np.abs(np.dot(xyz - p2, ax2))

            min_dist_start = np.min(dists_start)
            min_dist_end = np.min(dists_end)

            if min_dist_start < max_distance and min_dist_end < max_distance:
                points_start.append(traj.points[np.argmin(dists_start)])
                points_end.append(traj.points[np.argmin(dists_end)])
            else:
                points_start.append(np.full(traj.points.shape[1], np.nan))
                points_end.append(np.full(traj.points.shape[1], np.nan))

        # TODO: check empty trajectories
        self.points1 = trajectories.copy(data = points_start)
        self.points2 = trajectories.copy(data = points_end)

        # Distances to P1 and P2 and relative deviations
        d1 = np.linalg.norm(self.points1.points[:, 1:4] - self.p1, axis = 1)
        d2 = np.linalg.norm(self.points2.points[:, 1:4] - self.p2, axis = 1)

        self.deviations = np.abs(d2 - d1)

        # Return histogram of deviations
        if self.histogram:
            return plots.histogram(
                self.deviations,
                xaxis_title = "Relative Deviation (mm)",
                yaxis_title = "Probability (%)",
                **self.kwargs,
            )
        else:
            return self.deviations




class RelativeDeviationsLinear(Reducer):
    '''Apply the `RelativeDeviations` mixing algorithm at `num_divisions`
    equidistant points between `p1` and `p2`, saving histogram images at each
    step in `directory`.

    Reducer signature:

    ::

               PointData -> LaceyColors.fit -> plotly.graph_objs.Figure
         list[PointData] -> LaceyColors.fit -> plotly.graph_objs.Figure
        list[np.ndarray] -> LaceyColors.fit -> plotly.graph_objs.Figure

    For details about the mixing algorithm itself, check the
    `RelativeDeviations` documentation.

    This algorithm saves a rich set of data:

    - Individual histograms for each point along P1-P2 are saved in the given
      `directory`.
    - A Plotly figure of computed statistics is returned, including the
      deviations' mean, standard deviation, skewness and kurtosis.
    - The raw data is saved as object attributes (see below).

    The generated images (saved in `directory` with `height` x `width` pixels)
    can be stitched into a video using `pept.plots.make_video`.

    The extra keyword arguments ``**kwargs`` are passed to the histogram
    creation routine `pept.plots.histogram`. You can e.g. set the YAxis limits
    by adding `ylim = [0, 20]`.

    *New in pept-0.5.1*

    Attributes
    ----------
    deviations : list[(N,) np.ndarray]
        A list of deviations computed by `RelativeDeviations` at each point
        between P1 and P2.

    mean : (N,) np.ndarray
        A vector of mean tracer deviations at each point between P1 and P2.

    std : (N,) np.ndarray
        A vector of the tracer deviations' standard deviation at each point
        between P1 and P2.

    skew : (N,) np.ndarray
        A vector of the tracer deviations' adjusted skewness at each point
        between P1 and P2. A normal distribution has a value of 0; positive
        values indicate a longer right distribution tail; negative values
        indicate a heavier left tail.

    kurtosis : (N,) np.ndarray
        A vector of the tracer deviations' Fisher kurtosis at each point
        between P1 and P2. A normal distribution has a value of 0; positive
        values indicate a "thin" distribution; negative values indicate a
        heavy, wide distribution.

    Examples
    --------
    Consider a pipe-flow experiment, with tracers moving from side to side in
    multiple passes / streamlines. First locate the tracers, then split their
    trajectories into each individual pass:

    >>> import pept
    >>> from pept.tracking import *
    >>>
    >>> split_pipe = pept.Pipeline([
    >>>     Segregate(window = 10, max_distance = 20),  # Appends label column
    >>>     GroupBy("label"),                           # Splits into samples
    >>>     Reorient(),                                 # Align with X axis
    >>>     Center(),                                   # Center points at 0
    >>>     Stack(),
    >>> ])
    >>> streamlines = split_pipe.fit(trajectories)

    Now each sample in `streamlines` corresponds to a single tracer pass, e.g.
    `streamlines[0]` is the first pass, `streamlines[1]` is the second. The
    passes were reoriented and centred such that the pipe is aligned with the
    X axis.

    Now the `RelativeDeviationsLinear` reducer can be used to create images of
    the mixing between the pipe entrance and exit:

    >>> from pept.processing import RelativeDeviationsLinear
    >>> entrance = [-100, 0, 0]     # Pipe data was aligned with X and centred
    >>> exit = [100, 0, 0]
    >>> summary_fig = RelativeDeviationsLinear(
    >>>     directory = "deviations",   # Creates directory to save images
    >>>     p1 = entrance,
    >>>     p2 = exit,
    >>> ).fit(streamlines)
    >>> summary_fig.show()              # Summary statistics: mean, std, etc.

    Now the directory "deviations" was created inside your current working
    folder, and all relative deviation histograms were saved there as
    "frame0000.png", "frame0001.png", etc.
    You can stitch all images together into a video using
    `pept.plots.make_video`:

    >>> import pept
    >>> pept.plots.make_video(
    >>>     "deviations/frame*.png",
    >>>     output = "deviations/video.avi"
    >>> )

    The raw deviations and statistics can also be extracted directly:

    >>> mixing_algorithm = RelativeDeviationsLinear(
    >>>     directory = "deviations",   # Creates directory to save images
    >>>     p1 = entrance,
    >>>     p2 = exit,
    >>> )
    >>> fig = mixing_algorithm.fit(streamlines)
    >>> fig.show()

    >>> deviations = mixing_algorithm.deviations
    >>> mean = mixing_algorithm.mean
    >>> std = mixing_algorithm.std
    >>> skew = mixing_algorithm.skew
    >>> kurtosis = mixing_algorithm.kurtosis
    '''

    def __init__(
        self,
        directory,
        p1, p2,
        num_divisions = 50,
        max_distance = 10,
        height = 1000,
        width = 2000,
        prefix = "frame",
        **kwargs,
    ):
        self.directory = directory
        self.num_divisions = int(num_divisions)

        self.p1 = np.asarray(p1, dtype = float)
        self.p2 = np.asarray(p2, dtype = float)

        self.max_distance = float(max_distance)

        self.height = int(height)
        self.width = int(width)
        self.prefix = prefix
        self.kwargs = kwargs

        # Will be set in `fit`
        self.deviations = None
        self.mean = None
        self.std = None
        self.skew = None
        self.kurtosis = None


    def fit(
        self,
        trajectories,
        executor = "joblib",
        max_workers = None,
        verbose = True,
    ):

        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

        divisions = np.c_[
            np.linspace(self.p1[0], self.p2[0], self.num_divisions),
            np.linspace(self.p1[1], self.p2[1], self.num_divisions),
            np.linspace(self.p1[2], self.p2[2], self.num_divisions),
        ]

        axis = self.p2 - self.p1

        # Save vectors of deviations so that we can set the XAxis range
        def compute_deviations(division):
            return RelativeDeviations(
                p1 = self.p1,
                p2 = division,
                ax1 = axis,
                ax2 = axis,
                max_distance = self.max_distance,
                histogram = False,
            ).fit(trajectories)

        self.deviations = _parallel(
            compute_deviations,
            divisions,
            executor = executor,
            max_workers = max_workers,
            desc = "RelativeDeviationsLinear 1 / 3 :",
            verbose = verbose,
        )

        # Save histograms to disk
        xlim = [0, np.nanmax([np.nanmax(d) for d in self.deviations])]

        def save_histograms(idiv):
            fig = plots.histogram(
                self.deviations[idiv],
                xlim = xlim,
                **self.kwargs,
            )

            travelled = np.linalg.norm(divisions[idiv] - self.p1)
            fig.update_layout(
                title = f"Travelled {travelled:4.4f} mm",
                xaxis_title = "Deviation (mm)",
                yaxis_title = "Probability (%)",
            )

            fig.write_image(
                f"{self.directory}/{self.prefix}{idiv:0>4}.png",
                height = self.height,
                width = self.width,
            )

        _parallel(
            save_histograms,
            range(self.num_divisions),
            executor = executor,
            max_workers = max_workers,
            desc = "RelativeDeviationsLinear 2 / 3 :",
            verbose = verbose,
        )

        # Compute summarised statistics about distributions
        def compute_stats(idiv):
            dev = self.deviations[idiv]
            dev = dev[np.isfinite(dev)]
            return [
                np.mean(dev),
                np.std(dev),
                scipy.stats.skew(dev),
                scipy.stats.kurtosis(dev),
            ]

        stats = _parallel(
            compute_stats,
            range(self.num_divisions),
            executor = executor,
            max_workers = max_workers,
            desc = "RelativeDeviationsLinear 3 / 3 :",
            verbose = verbose,
        )
        stats = np.array(stats, order = "F")

        self.mean = stats[:, 0]
        self.std = stats[:, 1]
        self.skew = stats[:, 2]
        self.kurtosis = stats[:, 3]

        # Plot summarised statistics
        distance = np.linspace(
            0,
            np.linalg.norm(self.p2 - self.p1),
            self.num_divisions,
        )

        fig = make_subplots(rows = 2, cols = 1, subplot_titles = [
            "Mean Tracer Deviation Along P1-P2 Axis",
            "Distribution Skewness & Kurtosis (How Many Outliers?)",
        ])

        fig.add_trace(
            go.Scatter(
                x = distance,
                y = self.mean,
                mode = "lines",
                name = "Mean Deviation",
            ),
            row = 1, col = 1,
        )

        fig.add_trace(
            go.Scatter(
                x = distance,
                y = self.mean - self.std,
                mode = 'lines',
                marker_color = "#444",
                line_width = 0,
                showlegend = False,
            ),
            row = 1, col = 1,
        )

        fig.add_trace(
            go.Scatter(
                x = distance,
                y = self.mean + self.std,
                mode = 'lines',
                marker_color = "#444",
                line_width = 0,
                fillcolor = 'rgba(68, 68, 68, 0.3)',
                fill = 'tonexty',
                name = "Standard Deviation",
            ),
            row = 1, col = 1,
        )

        # Plot skewness and kurtosis
        fig.add_trace(
            go.Scatter(
                x = distance,
                y = self.skew,
                name = "Skewness",
            ),
            row = 2, col = 1,
        )

        fig.add_trace(
            go.Scatter(
                x = distance,
                y = self.kurtosis,
                name = "Kurtosis",
            ),
            row = 2, col = 1,
        )

        plots.format_fig(fig)
        fig.update_xaxes(title = "Length Along P1-P2 Axis (mm)")
        fig.update_layout(yaxis_title = "Deviation (mm)")

        return fig




class AutoCorrelation(Reducer):
    r'''Compute autocorrelation of multiple measures (eg YZ velocities) as a
    function of a lagging variable (eg time).

    Reducer signature:

    ::

               PointData -> AutoCorrelation.fit -> PlotlyGrapher2D
         list[PointData] -> AutoCorrelation.fit -> PlotlyGrapher2D
        list[np.ndarray] -> AutoCorrelation.fit -> PlotlyGrapher2D

    **Each sample in the input `PointData` is treated as a separate streamline
    / tracer pass. You can group passes using `Segregate + GroupBy("label")`**.

    Autocorrelation and autocovariance each refer to about 3 different things
    in each field. The formula used here, inspired by the VACF in molecular
    dynamics and generalised for arbitrary measures, is:

    .. math::

       C(L_i) = \frac{ \sum_{N} V(L_0) \cdot V(L_i) }{N}

    i.e. the autocorrelation C at a lag of Li is the average of the dot
    products of quantities V for all N tracers. For example, the velocity
    autocorrelation function with respect to time would be the average of
    `vx(0) vx(t) + vy(0) vy(t) + vz(0) vz(t)` at a given time `t`.

    The input `lag` defines the column used as a lagging variable; it can be
    given as a named column string (e.g. `"t"`) or index (e.g. `0`).

    The input `signals` define the quantities for which the autocorrelation is
    computed, given as a list of column names (e.g. `["vy", "vz"]`) or indices
    (e.g. `[5, 6]`).

    The input `span`, if defined, is the minimum and maximum values for the
    `lag` (e.g. start and end times) for which the autocorrelation will be
    computed. By default it is automatically computed as the range of values.

    The input `num_divisions` is the number of lag points between `span[0]` and
    `span[1]` for which the autocorrelation will be computed.

    The `max_distance` parameter defines the maximum distance allowed between
    a lag value and the closest trajectory value for it to be considered.

    If `normalize` is True, then the formula used becomes:

    .. math::

       C(L_i) = \frac{ \sum_{N} V(L_0) \cdot V(L_i) / V(L_0) \cdot V(L_0)}{N}


    If `preprocess` is True, then the times of each tracer pass is taken
    relative to its start; only relevant if using time as the lagging variable.

    The extra keyword arguments ``**kwargs`` are passed to
    `PlotlyGrapher2D.add_points`. You can e.g. set the YAxis limits by adding
    `ylim = [0, 20]`.

    The extra keyword arguments ``**kwargs`` are passed to
    `plotly.graph_objs.Scatter`. You can e.g. set a different colorscheme with
    "marker_colorscheme = 'Viridis'".

    *New in pept-0.5.1*

    Examples
    --------
    Consider a pipe-flow experiment, with tracers moving from side to side in
    multiple passes / streamlines. First locate the tracers, then split their
    trajectories into each individual pass:

    >>> import pept
    >>> from pept.tracking import *
    >>>
    >>> split_pipe = pept.Pipeline([
    >>>     Segregate(window = 10, max_distance = 20),  # Appends label column
    >>>     GroupBy("label"),                           # Splits into samples
    >>>     Reorient(),                                 # Align with X axis
    >>>     Center(),                                   # Center points at 0
    >>>     Velocity(7),                                # Compute vx, vy, vz
    >>>     Stack(),
    >>> ])
    >>> streamlines = split_pipe.fit(trajectories)

    Now each sample in `streamlines` corresponds to a single tracer pass, e.g.
    `streamlines[0]` is the first pass, `streamlines[1]` is the second. The
    passes were reoriented and centred such that the pipe is aligned with the
    X axis.

    Now the `AutoCorrelation` algorithm can be used to compute the VACF:

    >>> from pept.processing import AutoCorrelation
    >>> fig = AutoCorrelation("t", ["vx", "vy", "vz"]).fit(streamlines)
    >>> fig.show()

    The radial velocity autocorrelation can be computed as a function of the
    pipe length (X axis as it was reoriented):

    >>> entrance = -100
    >>> exit = 100
    >>> ac = AutoCorrelation("x", ["vy", "vz"], span = [entrance, exit])
    >>> ac.fit(streamlines).show()

    The raw lags and autocorrelations plotted can be accessed directly:

    >>> ac.lags
    >>> ac.correlation

    The radial location can be autocorrelated with time, then normalised to
    show periodic movements (e.g. due to a mixer):

    >>> ac = AutoCorrelation("t", ["y", "z"], normalize = True)
    >>> ac.fit(streamlines).show()
    '''

    def __init__(
        self,
        lag = "t",
        signals = ["vx", "vy", "vz"],
        span = None,
        num_divisions = 500,
        max_distance = 10,
        normalize = False,
        preprocess = True,
        **kwargs,
    ):

        self.lag = lag
        if isinstance(signals, str) or isinstance(signals, Number):
            signals = [signals]
        self.signals = signals

        if span is not None:
            span = tuple(span)
            if len(span) != 2:
                raise ValueError(textwrap.fill((
                    "The input `span`, if defined, must contain two "
                    f"values [lag_start, lag_end]. Received `{span}`."
                )))

        self.span = span
        self.num_divisions = int(num_divisions)
        self.max_distance = float(max_distance)

        self.normalize = bool(normalize)
        self.preprocess = bool(preprocess)

        self.kwargs = kwargs

        # Will be set in `fit`
        self.lags = None
        self.correlation = None


    def fit(
        self,
        trajectories,
        executor = "joblib",
        max_workers = None,
        verbose = True,
    ):

        if not isinstance(trajectories, PointData):
            try:
                trajectories = PointData(trajectories)
            except (ValueError, TypeError):
                raise TypeError(textwrap.fill((
                    "The input `trajectories` must be pept.PointData-like. "
                    f"Received `{type(trajectories)}`."
                )))

        # Extract relevant columns' indices
        if isinstance(self.lag, str):
            ilag = trajectories.columns.index(self.lag)
        else:
            ilag = int(self.lag)

        isignals = []
        for sig in self.signals:
            if isinstance(sig, str):
                isignals.append(trajectories.columns.index(sig))
            else:
                isignals.append(int(sig))

        # If preprocessing is enabled, make times relative to the start of each
        # trajectory pass
        if self.preprocess and ilag == 0:
            trajectories = trajectories.copy()
            for traj in trajectories:
                traj.points[:, 0] -= traj.points[0, 0]

        # Set span if undefined
        if self.span is None:
            self.span = (
                np.min(trajectories.points[:, ilag]),
                np.max(trajectories.points[:, ilag]),
            )

        # For each tracer pass, find closest value to the lag in `divisions`
        divisions = np.linspace(self.span[0], self.span[1], self.num_divisions)
        correlation = np.zeros(self.num_divisions)

        # Save correlations as class attributes
        self.lags = divisions
        self.correlation = correlation

        def closest_signal(traj, lag):
            lag_values = traj.points[:, ilag]

            # Find closest lag value
            lag_distances = np.abs(lag_values - lag)
            ilag_closest = np.argmin(lag_distances)

            # If not lag was close enough, return NaNs
            if lag_distances[ilag_closest] > self.max_distance:
                return np.full(len(isignals), np.nan)
            else:
                return traj.points[ilag_closest, isignals]

        # Compute signals at lag=0
        signals0 = [
            closest_signal(traj, divisions[0])
            for traj in trajectories
        ]

        def compute_correlation(lag):
            # Find signal values close to this lag value
            signal_values = [
                closest_signal(traj, lag)
                for traj in trajectories
            ]

            # Compute correlation as dot product with signals at lag=0
            if self.normalize:
                corr = [
                    np.dot(signals0[i], signal_values[i]) /
                    np.dot(signals0[i], signals0[i])
                    for i in range(len(signal_values))
                ]
            else:
                corr = [
                    np.dot(signals0[i], signal_values[i])
                    for i in range(len(signal_values))
                ]

            # Return ensemble average, ignoring NaNs (i.e. when no signal was
            # found close enough to the given lag value)
            finites = np.isfinite(corr)

            if not len(corr) or np.all(~finites):
                return np.nan, 0

            return np.nanmean(corr), finites.sum()

        # Compute correlation at each lag in `divisions`
        stats = _parallel(
            compute_correlation,
            divisions,
            executor = executor,
            max_workers = max_workers,
            desc = "AutoCorrelation :",
            verbose = verbose,
        )

        correlation[:] = [s[0] for s in stats]
        finites = np.array([s[1] for s in stats])

        # Make points denser for colorbars
        dense_lags = np.linspace(
            self.span[0],
            self.span[1],
            50 * self.num_divisions,
        )
        dense_correlation = interp1d(self.lags, self.correlation)(dense_lags)
        dense_finites = interp1d(self.lags, finites)(dense_lags)

        # Plot correlation as a function of lag
        if len(self.correlation):
            ylim = [np.nanmin(self.correlation), np.nanmax(self.correlation)]
        else:
            ylim = None

        if "marker_size" not in self.kwargs.keys():
            self.kwargs["marker_size"] = 5

        if "marker_colorscale" not in self.kwargs.keys():
            self.kwargs["marker_colorscale"] = "Magma_r"

        if "line_color" not in self.kwargs.keys():
            self.kwargs["line_color"] = "black"

        grapher = plots.PlotlyGrapher2D(ylim = ylim)
        grapher.add_trace(go.Scatter(
            x = dense_lags,
            y = dense_correlation,
            mode = "markers+lines",
            marker = dict(
                colorbar_title = "N",
                color = dense_finites,
            ),
            **self.kwargs,
        ))

        norm = "Normalised " if self.normalize else ""
        grapher.fig.update_layout(
            xaxis_title = f"Lag (column `{self.lag}`)",
            yaxis_title = f"{norm}AutoCorrelation (columns {self.signals})",
        )

        # Set scaleratios to be automatically determined
        for i in range(grapher._rows):
            for j in range(grapher._cols):
                index = i * grapher._cols + j + 1
                yaxis = f"yaxis{index}" if index != 1 else "yaxis"
                grapher._fig["layout"][yaxis].update(
                    scaleanchor = None,
                    scaleratio = None,
                )

        # If the span is inversed, reverse the X-axis
        if self.span[1] < self.span[0]:
            grapher.fig.update_layout(xaxis_autorange = "reversed")

        return grapher




class SpatialProjections(Reducer):
    '''Project multiple tracer passes onto a moving 2D plane along a given
    `direction` between `start` and `end` coordinates, saving each frame in
    `directory`.

    Reducer signature:

    ::

               PointData -> SpatialProjections.fit -> None
         list[PointData] -> SpatialProjections.fit -> None
        list[np.ndarray] -> SpatialProjections.fit -> None

    **Each sample in the input `PointData` is treated as a separate streamline
    / tracer pass. You can group passes using `Segregate + GroupBy("label")`**.

    The generated images (saved in `directory` with `height` x `width` pixels)
    can be stitched into a video using `pept.plots.make_video`.

    The extra keyword arguments ``**kwargs`` are passed to the histogram
    creation routine `pept.plots.histogram`. You can e.g. set the YAxis limits
    by adding `ylim = [0, 20]`.

    *New in pept-0.5.1*

    Attributes
    ----------
    projections : list[(N, 5), np.ndarray]
        A list of frames for each division between `start` and `end`, with each
        frame saving 5 columns [t, x, y, z, colorbar_col].

    Examples
    --------
    Consider a pipe-flow experiment, with tracers moving from side to side in
    multiple passes / streamlines. First locate the tracers, then split their
    trajectories into each individual pass:

    >>> import pept
    >>> from pept.tracking import *
    >>>
    >>> split_pipe = pept.Pipeline([
    >>>     Segregate(window = 10, max_distance = 20),  # Appends label column
    >>>     GroupBy("label"),                           # Splits into samples
    >>>     Reorient(),                                 # Align with X axis
    >>>     Center(),                                   # Center points at 0
    >>>     Stack(),
    >>> ])
    >>> streamlines = split_pipe.fit(trajectories)

    Now each sample in `streamlines` corresponds to a single tracer pass, e.g.
    `streamlines[0]` is the first pass, `streamlines[1]` is the second. The
    passes were reoriented and centred such that the pipe is aligned with the
    X axis.

    Now the `RelativeDeviationsLinear` reducer can be used to create images of
    the mixing between the pipe entrance and exit:

    >>> from pept.processing import SpatialProjections
    >>> entrance_x = -100                   # Pipe data was aligned with X
    >>> exit_x = 100
    >>> SpatialProjections(
    >>>     directory = "projections",      # Creates directory to save images
    >>>     start = entrance_x,
    >>>     end = exit_x,
    >>> ).fit(streamlines)

    Now the directory "projections" was created inside your current working
    folder, and eachc projected frame was saved there as "frame0000.png",
    "frame0001.png", etc. You can stitch all images together into a video using
    `pept.plots.make_video`:

    >>> import pept
    >>> pept.plots.make_video(
    >>>     "projections/frame*.png",
    >>>     output = "projections/video.avi"
    >>> )

    The raw projections can also be extracted directly:

    >>> sp = SpatialProjections(
    >>>     directory = "projections",   # Creates directory to save images
    >>>     p1 = entrance_x,
    >>>     p2 = exit_x,
    >>> )
    >>> sp.fit(streamlines)
    >>> sp.projections
    '''

    def __init__(
        self,
        directory,
        start,
        end,
        dimension = "x",
        num_divisions = 500,
        max_distance = 10,
        colorbar_col = -1,
        height = 1000,
        width = 1000,
        prefix = "frame",
        **kwargs,
    ):

        self.directory = directory
        self.start = float(start)
        self.end = float(end)

        # Transform x -> 1, y -> 2, z -> 3 using ASCII integer `ord`er
        if isinstance(dimension, str):
            if dimension != "x" and dimension != "y" and dimension != "z":
                raise ValueError(textwrap.fill((
                    "The input `dimension` must be either 'x', 'y' or 'z'. "
                    f"Received `{dimension}`."
                )))

            self.dimension = ord(dimension) - ord('x') + 1
        else:
            self.dimension = int(dimension)
            if self.dimension < 1 or self.dimension > 3:
                raise ValueError(textwrap.fill((
                    "The input `dimension`, if given as an index, must be "
                    f"between 1 and 3 (inclusive). Received `{dimension}`."
                )))

        self.num_divisions = int(num_divisions)
        self.max_distance = float(max_distance)
        self.colorbar_col = colorbar_col

        self.height = int(height)
        self.width = int(width)
        self.prefix = prefix
        self.kwargs = kwargs

        # Will be set in `fit`
        self.projections = None


    def fit(
        self,
        trajectories,
        executor = "joblib",
        max_workers = None,
        verbose = True,
    ):

        if not isinstance(trajectories, PointData):
            try:
                trajectories = PointData(trajectories)
            except (ValueError, TypeError):
                raise TypeError(textwrap.fill((
                    "The input `trajectories` must be pept.PointData-like. "
                    f"Received `{type(trajectories)}`."
                )))

        # Find colorbar column's index
        if isinstance(self.colorbar_col, str):
            icolorbar_col = trajectories.columns.index(self.colorbar_col)
        else:
            icolorbar_col = int(self.colorbar_col)

        # Create directory for saving projection plots
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

        # Points at which to project the trajectories
        self.divisions = np.linspace(self.start, self.end, self.num_divisions)

        # For each point along the start-end axis, save the closest point's
        # coordinates and colorbar column
        def project_division(idiv):
            division = self.divisions[idiv]
            points = []

            for traj in trajectories:
                coords = traj.points[:, self.dimension]
                distances = np.abs(coords - division)

                imin_dist = np.argmin(distances)
                min_dist = distances[imin_dist]

                if min_dist < self.max_distance:
                    points.append(traj.points[
                        imin_dist,
                        [0, 1, 2, 3, icolorbar_col],
                    ])

            if not len(points):
                return np.empty((0, 5))
            return np.array(points)

        self.projections = _parallel(
            project_division,
            range(self.num_divisions),
            executor = executor,
            max_workers = max_workers,
            desc = "SpatialProjections 1 / 2 :",
            verbose = verbose,
        )

        # Other remaining dimensions
        other = list({1, 2, 3} - {self.dimension})
        ix = other[0]
        iy = other[1]

        # Find plot limits
        if "xlim" not in self.kwargs.keys():
            points = np.concatenate([p[:, ix] for p in self.projections])
            xlim = [points.min(), points.max()]
            extra = 0.05 * (xlim[1] - xlim[0])
            self.kwargs["xlim"] = [xlim[0] - extra, xlim[1] + extra]

        if "ylim" not in self.kwargs.keys():
            points = np.concatenate([p[:, iy] for p in self.projections])
            ylim = [points.min(), points.max()]
            extra = 0.05 * (ylim[1] - ylim[0])
            self.kwargs["ylim"] = [ylim[0] - extra, ylim[1] + extra]

        if "size" not in self.kwargs.keys():
            self.kwargs["size"] = 15

        colors = np.concatenate([p[:, -1] for p in self.projections])
        if "marker_cmin" not in self.kwargs.keys():
            self.kwargs["marker_cmin"] = colors.min()

        if "marker_cmax" not in self.kwargs.keys():
            self.kwargs["marker_cmax"] = colors.max()

        if "colorscale" not in self.kwargs.keys():
            self.kwargs["marker_colorscale"] = "Magma"

        if "colorbar_title" not in self.kwargs.keys():
            self.kwargs["marker_colorbar_title"] = \
                trajectories.columns[icolorbar_col]

        def plot_save_projections(idiv):
            # dim = '_XYZ'[self.dimension]
            # dist = self.divisions[idiv] - self.divisions[0]

            grapher = plots.PlotlyGrapher2D(
                # subplot_titles = [f"Length along {dim} = {dist:4.4f} mm"],
                xlim = self.kwargs["xlim"],
                ylim = self.kwargs["ylim"],
            )

            kwargs = self.kwargs.copy()
            del kwargs["xlim"]
            del kwargs["ylim"]

            grapher.add_points(
                self.projections[idiv][:, [0, ix, iy]],
                color = self.projections[idiv][:, -1],
                **kwargs,
            )

            # Set axis labels
            grapher.fig.update_layout(
                xaxis_title = f"{'_XYZ'[other[0]]} (mm)",
                yaxis_title = f"{'_XYZ'[other[1]]} (mm)",
            )

            grapher.fig.write_image(
                f"{self.directory}/{self.prefix}{idiv:0>4}.png",
                height = self.height,
                width = self.width,
            )

        self.projections = _parallel(
            plot_save_projections,
            range(self.num_divisions),
            executor = executor,
            max_workers = max_workers,
            desc = "SpatialProjections 2 / 2 :",
            verbose = verbose,
        )
