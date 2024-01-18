# Functions to use with netcdfs
# based on https://docs.esmvaltool.org/projects/ESMValCore/en/latest/api/esmvalcore.preprocessor.html#esmvalcore.preprocessor.anomalies

import numpy as np
import logging
import re
import warnings
from collections.abc import Callable
from typing import Any, Optional



import datetime
import isodate
import iris
from iris.cube import Cube
from iris.time import PartialDateTime
import iris.analysis
from iris.coords import DimCoord

from typing import Iterable, Optional
from scipy.stats import mstats

import dask.array as da

logger = logging.getLogger(__name__)

def _parse_start_date(date):
    """Parse start of the input `timerange` tag given in ISO 8601 format.

    Returns a datetime.datetime object.
    """
    if date.startswith('P'):
        start_date = isodate.parse_duration(date)
    else:
        try:
            start_date = isodate.parse_datetime(date)
        except isodate.isoerror.ISO8601Error:
            start_date = isodate.parse_date(date)
            start_date = datetime.datetime.combine(
                start_date, datetime.time.min)
    return start_date


def _parse_end_date(date):
    """Parse end of the input `timerange` given in ISO 8601 format.

    Returns a datetime.datetime object.
    """
    if date.startswith('P'):
        end_date = isodate.parse_duration(date)
    else:
        if len(date) == 4:
            end_date = datetime.datetime(int(date) + 1, 1, 1, 0, 0, 0)
        elif len(date) == 6:
            month, year = get_next_month(int(date[4:]), int(date[0:4]))
            end_date = datetime.datetime(year, month, 1, 0, 0, 0)
        else:
            try:
                end_date = isodate.parse_datetime(date)
            except isodate.ISO8601Error:
                end_date = isodate.parse_date(date)
                end_date = datetime.datetime.combine(end_date,
                                                     datetime.time.min)
            end_date += datetime.timedelta(seconds=1)
    return end_date

def _duration_to_date(duration, reference, sign):
    """Add or subtract a duration period to a reference datetime."""
    date = reference + sign * duration
    return date

def _select_timeslice(cube: Cube, select: np.ndarray) -> Cube: # | None:
    """Slice a cube along its time axis."""
    if select.any():
        coord = cube.coord('time')
        time_dims = cube.coord_dims(coord)
        if time_dims:
            time_dim = time_dims[0]
            slices = tuple(select if i == time_dim else slice(None)
                           for i in range(cube.ndim))
            cube_slice = cube[slices]
        else:
            cube_slice = cube
    else:
        cube_slice = None
    return cube_slice

def _extract_datetime(
    cube: Cube,
    start_datetime: PartialDateTime,
    end_datetime: PartialDateTime,
) -> Cube:
    """Extract a time range from a cube.

    Given a time range passed in as a datetime.datetime object, it
    returns a time-extracted cube with data only within the specified
    time range with a resolution up to seconds..

    Parameters
    ----------
    cube:
        Input cube.
    start_datetime:
        Start datetime
    end_datetime:
        End datetime

    Returns
    -------
    iris.cube.Cube
        Sliced cube.

    Raises
    ------
    ValueError
        if time ranges are outside the cube time limits
    """
    time_coord = cube.coord('time')
    time_units = time_coord.units
    if time_units.calendar == '360_day':
        if isinstance(start_datetime.day, int) and start_datetime.day > 30:
            start_datetime.day = 30
        if isinstance(end_datetime.day, int) and end_datetime.day > 30:
            end_datetime.day = 30

    if not cube.coord_dims(time_coord):
        constraint = iris.Constraint(
            time=lambda t: start_datetime <= t.point < end_datetime)
        cube_slice = cube.extract(constraint)
    else:
        # Convert all time points to dates at once, this is much faster
        # than using a constraint.
        dates = time_coord.units.num2date(time_coord.points)
        select = (dates >= start_datetime) & (dates < end_datetime)
        cube_slice = _select_timeslice(cube, select)

    if cube_slice is None:

        def dt2str(time: PartialDateTime) -> str:
            txt = f"{time.year}-{time.month:02d}-{time.day:02d}"
            if any([time.hour, time.minute, time.second]):
                txt += f" {time.hour:02d}:{time.minute:02d}:{time.second:02d}"
            return txt
        raise ValueError(
            f"Time slice {dt2str(start_datetime)} "
            f"to {dt2str(end_datetime)} is outside "
            f"cube time bounds {time_coord.cell(0).point} to "
            f"{time_coord.cell(-1).point}.")

    return cube_slice

def _get_period_coord(cube, period, seasons):
    """Get periods."""
    if period in ['hourly', 'hour', 'hr']:
        if not cube.coords('hour'):
            iris.coord_categorisation.add_hour(cube, 'time')
        return cube.coord('hour')
    if period in ['daily', 'day']:
        if not cube.coords('day_of_year'):
            iris.coord_categorisation.add_day_of_year(cube, 'time')
        return cube.coord('day_of_year')
    if period in ['monthly', 'month', 'mon']:
        if not cube.coords('month_number'):
            iris.coord_categorisation.add_month_number(cube, 'time')
        return cube.coord('month_number')
    if period in ['seasonal', 'season']:
        if not cube.coords('season_number'):
            iris.coord_categorisation.add_season_number(cube,
                                                        'time',
                                                        seasons=seasons)
        return cube.coord('season_number')
    raise ValueError(f"Period '{period}' not supported")

def _aggregate_time_fx(result_cube, source_cube):
    time_dim = set(source_cube.coord_dims(source_cube.coord('time')))
    if source_cube.cell_measures():
        for measure in source_cube.cell_measures():
            measure_dims = set(source_cube.cell_measure_dims(measure))
            if time_dim.intersection(measure_dims):
                logger.debug('Averaging time dimension in measure %s.',
                             measure.var_name)
                result_measure = da.mean(measure.core_data(),
                                         axis=tuple(time_dim))
                measure = measure.copy(result_measure)
                measure_dims = tuple(measure_dims - time_dim)
                result_cube.add_cell_measure(measure, measure_dims)

    if source_cube.ancillary_variables():
        for ancillary_var in source_cube.ancillary_variables():
            ancillary_dims = set(
                source_cube.ancillary_variable_dims(ancillary_var))
            if time_dim.intersection(ancillary_dims):
                logger.debug(
                    'Averaging time dimension in ancillary variable %s.',
                    ancillary_var.var_name)
                result_ancillary_var = da.mean(ancillary_var.core_data(),
                                               axis=tuple(time_dim))
                ancillary_var = ancillary_var.copy(result_ancillary_var)
                ancillary_dims = tuple(ancillary_dims - time_dim)
                result_cube.add_ancillary_variable(ancillary_var,
                                                   ancillary_dims)

def aggregator_accept_weights(aggregator: iris.analysis.Aggregator) -> bool:
    """Check if aggregator support weights.

    Parameters
    ----------
    aggregator:
        Aggregator to check.

    Returns
    -------
    bool
        ``True`` if aggregator support weights, ``False`` otherwise.

    """
    weighted_aggregators_cls = (
        iris.analysis.WeightedAggregator,
        iris.analysis.WeightedPercentileAggregator,
    )
    return isinstance(aggregator, weighted_aggregators_cls)

def update_weights_kwargs(
    aggregator: iris.analysis.Aggregator,
    kwargs: dict,
    weights: Any,
    cube: Optional[Cube] = None,
    callback: Optional[Callable] = None,
    **callback_kwargs,
) -> dict:
    """Update weights keyword argument.

    Parameters
    ----------
    aggregator:
        Iris aggregator.
    kwargs:
        Keyword arguments to update.
    weights:
        Object which will be used as weights if supported and desired.
    cube:
        Cube which can be updated through the callback (if not None) if weights
        are used.
    callback:
        Optional callback function with signature `f(cube: iris.cube.Cube,
        **kwargs) -> None`. Should update the cube given to this function
        in-place. Is called only when weights are used and cube is not None.
    **callback_kwargs:
        Optional keyword arguments passed to `callback`.

    Returns
    -------
    dict
        Updated keyword arguments.

    """
    kwargs = dict(kwargs)
    if aggregator_accept_weights(aggregator) and kwargs.get('weights', True):
        kwargs['weights'] = weights
        if cube is not None and callback is not None:
            callback(cube, **callback_kwargs)
    else:
        kwargs.pop('weights', None)
    return kwargs

def get_iris_aggregator(
    operator: str,
    **operator_kwargs,
) -> tuple[iris.analysis.Aggregator, dict]:
    """Get :class:`iris.analysis.Aggregator` and keyword arguments.

    Supports all available aggregators in :mod:`iris.analysis`.

    Parameters
    ----------
    operator:
        A named operator that is used to search for aggregators. Will be
        capitalized before searching for aggregators, i.e., `MEAN` **and**
        `mean` will find :const:`iris.analysis.MEAN`.
    **operator_kwargs:
        Optional keyword arguments for the aggregator.

    Returns
    -------
    tuple[iris.analysis.Aggregator, dict]
        Object that can be used within :meth:`iris.cube.Cube.collapsed`,
        :meth:`iris.cube.Cube.aggregated_by`, or
        :meth:`iris.cube.Cube.rolling_window` and the corresponding keyword
        arguments.

    Raises
    ------
    ValueError
        An invalid `operator` is specified, i.e., it is not found in
        :mod:`iris.analysis` or the returned object is not an
        :class:`iris.analysis.Aggregator`.

    """
    cap_operator = operator.upper()
    aggregator_kwargs = dict(operator_kwargs)

    # Deprecations
    if cap_operator == 'STD':
        msg = (
            f"The operator '{operator}' for computing the standard deviation "
            f"has been deprecated in ESMValCore version 2.10.0 and is "
            f"scheduled for removal in version 2.12.0. Please use 'std_dev' "
            f"instead. This is an exact replacement."
        )
        warnings.warn(msg, ESMValCoreDeprecationWarning)
        operator = 'std_dev'
        cap_operator = 'STD_DEV'
    elif re.match(r"^(P\d{1,2})(\.\d*)?$", cap_operator):
        msg = (
            f"Specifying percentile operators with the syntax 'pXX.YY' (here: "
            f"'{operator}') has been deprecated in ESMValCore version 2.10.0 "
            f"and is scheduled for removal in version 2.12.0. Please use "
            f"`operator='percentile'` with the keyword argument "
            f"`percent=XX.YY` instead. Example: `percent=95.0` for 'p95.0'. "
            f"This is an exact replacement."
        )
        warnings.warn(msg, ESMValCoreDeprecationWarning)
        aggregator_kwargs['percent'] = float(operator[1:])
        operator = 'percentile'
        cap_operator = 'PERCENTILE'

    # Check if valid aggregator is found
    if not hasattr(iris.analysis, cap_operator):
        raise ValueError(
            f"Aggregator '{operator}' not found in iris.analysis module"
        )
    aggregator = getattr(iris.analysis, cap_operator)
    if not hasattr(aggregator, 'aggregate'):
        raise ValueError(
            f"Aggregator {aggregator} found by '{operator}' is not a valid "
            f"iris.analysis.Aggregator"
        )

    # Use dummy cube to check if aggregator_kwargs are valid
    x_coord = DimCoord([1.0], bounds=[0.0, 2.0], var_name='x')
    cube = Cube([0.0], dim_coords_and_dims=[(x_coord, 0)])
    test_kwargs = update_weights_kwargs(
        aggregator, aggregator_kwargs, np.array([1.0])
    )
    try:
        cube.collapsed('x', aggregator, **test_kwargs)
    except (ValueError, TypeError) as exc:
        raise ValueError(
            f"Invalid kwargs for operator '{operator}': {str(exc)}"
        )

    return (aggregator, aggregator_kwargs)

def clip_timerange(cube: Cube, timerange: str) -> Cube:
    """Extract time range with a resolution up to seconds.

    Parameters
    ----------
    cube:
        Input cube.
    timerange: str
        Time range in ISO 8601 format.

    Returns
    -------
    iris.cube.Cube
        Sliced cube.

    Raises
    ------
    ValueError
        Time ranges are outside the cube's time limits.

    """
    start_date = _parse_start_date(timerange.split('/')[0])
    end_date = _parse_end_date(timerange.split('/')[1])

    if isinstance(start_date, isodate.duration.Duration):
        start_date = _duration_to_date(start_date, end_date, sign=-1)
    elif isinstance(start_date, datetime.timedelta):
        start_date = _duration_to_date(start_date, end_date, sign=-1)
        start_date -= datetime.timedelta(seconds=1)

    if isinstance(end_date, isodate.duration.Duration):
        end_date = _duration_to_date(end_date, start_date, sign=1)
    elif isinstance(end_date, datetime.timedelta):
        end_date = _duration_to_date(end_date, start_date, sign=1)
        end_date += datetime.timedelta(seconds=1)

    t_1 = PartialDateTime(
        year=start_date.year,
        month=start_date.month,
        day=start_date.day,
        hour=start_date.hour,
        minute=start_date.minute,
        second=start_date.second,
    )

    t_2 = PartialDateTime(
        year=end_date.year,
        month=end_date.month,
        day=end_date.day,
        hour=end_date.hour,
        minute=end_date.minute,
        second=end_date.second,
    )

    return _extract_datetime(cube, t_1, t_2)

def extract_time(
    cube: Cube,
    start_year: int,
    start_month: int,
    start_day: int,
    end_year: int,
    end_month: int,
    end_day: int,
) -> Cube:
    """Extract a time range from a cube.

    Given a time range passed in as a series of years, months and days, it
    returns a time-extracted cube with data only within the specified
    time range.

    Parameters
    ----------
    cube:
        Input cube.
    start_year:
        Start year.
    start_month:
        Start month.
    start_day:
        Start day.
    end_year:
        End year.
    end_month:
        End month.
    end_day:
        End day.

    Returns
    -------
    iris.cube.Cube
        Sliced cube.

    Raises
    ------
    ValueError
        Time ranges are outside the cube time limits.

    """
    t_1 = PartialDateTime(year=int(start_year),
                          month=int(start_month),
                          day=int(start_day))
    t_2 = PartialDateTime(year=int(end_year),
                          month=int(end_month),
                          day=int(end_day))

    return _extract_datetime(cube, t_1, t_2)

def theil_sen_estimator(x, y):
    n = len(x)
    slopes = []

    for i in range(n-1):
        for j in range(i+1, n):
            slopes.append((y[j] - y[i]) / (x[j] - x[i]))

    median_slope = np.median(slopes)
    median_intercept = np.median(y - median_slope * x)

    return median_slope, median_intercept


def detrend_theil_sen(data, axis=0, type='linear', bp=0, overwrite_data=False):
    """
    Remove linear trend along axis from data using Theil-Sen slopes.

    Parameters
    ----------
    data : array_like
        The input data.
    axis : int, optional
        The axis along which to detrend the data. By default, this is the
        first axis (0).
    type : {'linear', 'constant'}, optional
        The type of detrending. If ``type == 'linear'`` (default),
        the result of a Theil-Sen fit to `data` is subtracted from `data`.
        If ``type == 'constant'``, only the mean of `data` is subtracted.
    bp : array_like of ints, optional
        A sequence of break points. If given, an individual Theil-Sen fit is
        performed for each part of `data` between two break points.
        Break points are specified as indices into `data`. This parameter
        only has an effect when ``type == 'linear'``.
    overwrite_data : bool, optional
        If True, perform in place detrending and avoid a copy. Default is False

    Returns
    -------
    ret : ndarray
        The detrended input data.

    Based on:

    https://docs.esmvaltool.org/projects/ESMValCore/en/latest/api/esmvalcore.preprocessor.html#esmvalcore.preprocessor.detrend
    https://docs.esmvaltool.org/projects/ESMValCore/en/latest/_modules/esmvalcore/preprocessor/_detrend.html#detrend
    https://github.com/scipy/scipy/blob/906e6cd9bb022e78a07b34636bee64813ce56afa/scipy/signal/_signaltools.py#L3521

    """
    if type not in ['linear', 'l', 'constant', 'c']:
        raise ValueError("Trend type must be 'linear' or 'constant'.")
    data = np.asarray(data)
    dtype = data.dtype.char
    if dtype not in 'dfDF':
        dtype = 'd'
    if type in ['constant', 'c']: #delete mean
        ret = data - np.mean(data, axis, keepdims=True)
        return ret
    else: #delete trend
        dshape = data.shape
        N = dshape[axis]
        bp = np.sort(np.unique(np.concatenate(np.atleast_1d(0, bp, N))))
        if np.any(bp > N):
            raise ValueError("Breakpoints must be less than the length "
                             "of data along the given axis.")

        # Restructure data so that the axis is along the first dimension
        # and all other dimensions are collapsed into the second dimension
        rnk = len(dshape)
        if axis < 0:
            axis = axis + rnk
        newdata = np.moveaxis(data, axis, 0)
        newdata_shape = newdata.shape
        newdata = newdata.reshape(N, -1)

        if not overwrite_data:
            newdata = newdata.copy()  # make sure we have a copy
        if newdata.dtype.char not in 'dfDF':
            newdata = newdata.astype(dtype)

        # Find Theil-Sen fit and remove it for each piece
        for m in range(len(bp) - 1):
            sl = range(bp[m], bp[m + 1])  # Convert slice to range
            #x = np.arange(1, len(sl) + 1, dtype=dtype)
            y = newdata[sl]
            
            # Calculate Theil-Sen fit across all data points
            
            #dif_y = np.diff(y.flatten())
            #dif_x = np.diff(x)
            #slopes = dif_y/dif_x
            #slopes = np.array(slopes)
            y = np.array(y).flatten()
            x = np.arange(len(y), dtype=float)
            # Compute sorted slopes only when deltax > 0
            deltax = x[:, np.newaxis] - x
            deltay = y[:, np.newaxis] - y
            slopes = deltay[deltax > 0] / deltax[deltax > 0]
            slopes.sort()

            median_slope = np.median(slopes)
            intercept = np.median(y) - median_slope * np.median(x)
            y = newdata[sl]

            # Calculate trend
            trend = median_slope * x + intercept
            trend = trend.reshape(N, -1)
            # Remove trend from data
            newdata[sl] = y - trend

        # Put data back in the original shape.
        newdata = newdata.reshape(newdata_shape)
        ret = np.moveaxis(newdata, 0, axis)
        return ret
    

def detrend_theil_sen_cube(cube, dimension='time', method='linear'):
    """
    Detrend data along a given dimension.

    Parameters
    ----------
    cube: iris.cube.Cube
        input cube.
    dimension: str
        Dimension to detrend
    method: str
        Method to detrend. Available: linear, constant. See documentation of
        'detrend_theil_sen' for details

    Returns
    -------
    iris.cube.Cube
        Detrended cube
    
    Based on:

    https://docs.esmvaltool.org/projects/ESMValCore/en/latest/api/esmvalcore.preprocessor.html#esmvalcore.preprocessor.detrend
    https://docs.esmvaltool.org/projects/ESMValCore/en/latest/_modules/esmvalcore/preprocessor/_detrend.html#detrend
    https://github.com/scipy/scipy/blob/906e6cd9bb022e78a07b34636bee64813ce56afa/scipy/signal/_signaltools.py#L3521

    """
    coord = cube.coord(dimension)
    axis = cube.coord_dims(coord)[0]
    detrended = da.apply_along_axis(
        detrend_theil_sen,
        axis=axis,
        arr=cube.lazy_data(),
        type=method,
        shape=(cube.shape[axis],)
    )
    return cube.copy(detrended)

def climate_statistics(
    cube: Cube,
    operator: str = 'mean',
    period: str = 'full',
    seasons: Iterable[str] = ('DJF', 'MAM', 'JJA', 'SON'),
    **operator_kwargs,
) -> Cube:
    """Compute climate statistics with the specified granularity.

    Computes statistics for the whole dataset. It is possible to get them for
    the full period or with the data grouped by hour, day, month or season.

    Note
    ----
    The `mean`, `sum` and `rms` operations over the `full` period are weighted
    by the time coordinate, i.e., the length of the time intervals. For `sum`,
    the units of the resulting cube will be multiplied by corresponding time
    units (e.g., days).

    Parameters
    ----------
    cube:
        Input cube.
    operator:
        The operation. Used to determine the :class:`iris.analysis.Aggregator`
        object used to calculate the statistics. Allowed options are given in
        :ref:`this table <supported_stat_operator>`.
    period:
        Period to compute the statistic over. Available periods: `full`,
        `season`, `seasonal`, `monthly`, `month`, `mon`, `daily`, `day`,
        `hourly`, `hour`, `hr`.
    seasons:
        Seasons to use if needed. Defaults to ('DJF', 'MAM', 'JJA', 'SON').
    **operator_kwargs:
        Optional keyword arguments for the :class:`iris.analysis.Aggregator`
        object defined by `operator`.

    Returns
    -------
    iris.cube.Cube
        Climate statistics cube.
    """
    original_dtype = cube.dtype
    period = period.lower()

    # Use Cube.collapsed when full period is requested
    if period in ('full', ):
        (agg, agg_kwargs) = get_iris_aggregator(operator, **operator_kwargs)
        agg_kwargs = update_weights_kwargs(
            agg, agg_kwargs, '_time_weights_', cube, _add_time_weights_coord
        )
        with warnings.catch_warnings():
            warnings.filterwarnings(
                'ignore',
                message=(
                    "Cannot check if coordinate is contiguous: Invalid "
                    "operation for '_time_weights_'"
                ),
                category=UserWarning,
                module='iris',
            )
            clim_cube = cube.collapsed('time', agg, **agg_kwargs)

        # Make sure input and output cubes do not have auxiliary coordinate
        if cube.coords('_time_weights_'):
            cube.remove_coord('_time_weights_')
        if clim_cube.coords('_time_weights_'):
            clim_cube.remove_coord('_time_weights_')

    # Use Cube.aggregated_by for other periods
    else:
        clim_coord = _get_period_coord(cube, period, seasons)
        (agg, agg_kwargs) = get_iris_aggregator(operator, **operator_kwargs)
        clim_cube = cube.aggregated_by(clim_coord, agg, **agg_kwargs)
        clim_cube.remove_coord('time')
        _aggregate_time_fx(clim_cube, cube)
        if clim_cube.coord(clim_coord.name()).is_monotonic():
            iris.util.promote_aux_coord_to_dim_coord(clim_cube,
                                                     clim_coord.name())
        else:
            clim_cube = CubeList(
                clim_cube.slices_over(clim_coord.name())).merge_cube()
        cube.remove_coord(clim_coord)

    # Make sure that original dtype is preserved
    new_dtype = clim_cube.dtype
    if original_dtype != new_dtype:
        logger.debug(
            "climate_statistics changed dtype from "
            "%s to %s, changing back", original_dtype, new_dtype)
        clim_cube.data = clim_cube.core_data().astype(original_dtype)

    return clim_cube


def anomalies(
    cube: Cube,
    period: str,
    reference: Optional[dict] = None,
    standardize: bool = False,
    seasons: Iterable[str] = ('DJF', 'MAM', 'JJA', 'SON'),
) -> Cube:
    """Compute anomalies using a mean with the specified granularity.

    Computes anomalies based on hourly, daily, monthly, seasonal or yearly
    means for the full available period.

    Parameters
    ----------
    cube:
        Input cube.
    period:
        Period to compute the statistic over. Available periods: `full`,
        `season`, `seasonal`, `monthly`, `month`, `mon`, `daily`, `day`,
        `hourly`, `hour`, `hr`.
    reference: optional
        Period of time to use a reference, as needed for the
        :func:`~esmvalcore.preprocessor.extract_time` preprocessor function.
        If ``None``, all available data is used as a reference.
    standardize: optional
        If ``True`` standardized anomalies are calculated.
    seasons: optional
        Seasons to use if needed. Defaults to ('DJF', 'MAM', 'JJA', 'SON').

    Returns
    -------
    iris.cube.Cube
        Anomalies cube.
    """
    if reference is None:
        reference_cube = cube
    else:
        reference_cube = extract_time(cube, **reference)
    reference = climate_statistics(reference_cube,
                                   period=period,
                                   seasons=seasons)
    if period in ['full']:
        metadata = copy.deepcopy(cube.metadata)
        cube = cube - reference
        cube.metadata = metadata
        if standardize:
            cube_stddev = climate_statistics(cube,
                                             operator='std_dev',
                                             period=period,
                                             seasons=seasons)
            cube = cube / cube_stddev
            cube.units = '1'
        return cube

    cube = _compute_anomalies(cube, reference, period, seasons)

    # standardize the results if requested
    if standardize:
        cube_stddev = climate_statistics(cube,
                                         operator='std_dev',
                                         period=period)
        tdim = cube.coord_dims('time')[0]
        reps = cube.shape[tdim] / cube_stddev.shape[tdim]
        if not reps % 1 == 0:
            raise ValueError(
                "Cannot safely apply preprocessor to this dataset, "
                "since the full time period of this dataset is not "
                f"a multiple of the period '{period}'")
        cube.data = cube.core_data() / da.concatenate(
            [cube_stddev.core_data() for _ in range(int(reps))], axis=tdim)
        cube.units = '1'
    return cube

def _compute_anomalies(
    cube: Cube,
    reference: Cube,
    period: str,
    seasons: Iterable[str],
):
    cube_coord = _get_period_coord(cube, period, seasons)
    ref_coord = _get_period_coord(reference, period, seasons)
    indices = np.empty_like(cube_coord.points, dtype=np.int32)
    for idx, point in enumerate(ref_coord.points):
        indices = np.where(cube_coord.points == point, idx, indices)
    ref_data = reference.core_data()
    axis, = cube.coord_dims(cube_coord)
    if cube.has_lazy_data() and reference.has_lazy_data():
        # Rechunk reference data because iris.cube.Cube.aggregate_by, used to
        # compute the reference, produces very small chunks.
        # https://github.com/SciTools/iris/issues/5455
        ref_chunks = tuple(
            -1 if i == axis else chunk
            for i, chunk in enumerate(cube.lazy_data().chunks)
        )
        ref_data = ref_data.rechunk(ref_chunks)
    with dask.config.set({"array.slicing.split_large_chunks": True}):
        ref_data_broadcast = da.take(ref_data, indices=indices, axis=axis)
    data = cube.core_data() - ref_data_broadcast
    cube = cube.copy(data)
    cube.remove_coord(cube_coord)
    return cube

