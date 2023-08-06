# **R**otation of **3**-dimensional **F**rames

## Conversions

This library includes three sets of functions: general array checks,
attitude-representation conversions, and reference-frame conversions.  The
following table shows all the attitude-representation conversions provided,
where 'Vector' is short for 'rotation vector,' 'RPY is short for 'roll, pitch,
and yaw,' and 'DCM' is short for 'direction cosine matrix':

| To \ From  | Vector | Axis-angle | RPY    | DCM    | Quaternion |
| ---------- | :----: | :--------: | :----: | :----: | :--------: |
| Vector     |   -    |     x      |        |        |            |
| Axis-angle |   x    |     -      |   x    |   x    |     x      |
| RPY        |        |     x      |   -    |   x    |     x      |
| DCM        |        |     x      |   x    |   -    |     x      |
| Quaternion |        |     x      |   x    |   x    |     -      |

Because the conversion from rotation vector to axis-angle is so trivial, none of
the other attitude representations have conversions to rotation vectors.

In addition to the conversion from the z, y, x sequence of Euler angles to a
DCM, the function `rot` is also provided for creating a DCM from a generic set
of Euler angles in any desired sequence of axes.

This library also includes various conversions among Earth-specific and
navigation frames:

| To \\ From      |  e  |  d  |  t  |  c  |
| --------------- | --- | --- | --- | --- |
| e (ECEF)        |  -  |  x  |  x  |     |
| d (geodetic)    |  x  |  -  |     |  x  |
| t (tangent)     |  x  |     |  -  |     |
| c (curvilinear) |     |  x  |     |  -  |

## Passive Rotations

All rotations are interpreted as passive.  This means they represent rotations
of reference frames, not of vectors.

## Vectorization

When possible, the functions are vectorized in order to handle processing
batches of values.  A set of scalars is a 1D array.  A set of vectors is a 2D
array, with each vector in a column.  So, a (3, 7) array is a set of seven
vectors, each with 3 elements.  A set of matrices is a 3D array with each matrix
in a stack.  The first index is the stack number.  So, a (2, 5, 5) array is a
stack of two 5x5 matrices.  Roll, pitch, and yaw are not treated as a vector but
as three separate quantities.  The same is true for latitude, longitude, and
height above ellipsoid.  A quaternion is passed around as an array.

## Robustness

In general, the functions in this library check that the inputs are of the
correct type and shape.  They do not generally handle converting inputs which do
not conform to the ideal type and shape.

## Provided Functions

The following functions are provided:

**Attitude-representation Conversions**

| Returns | Name                  | Parameters            |
| ------- | --------------------- | --------------------- |
| vec     | axis_angle_to_vector  | ax, ang, degs=False   |
| ax, ang | vector_to_axis_angle  | vec, degs=False       |
| ax, ang | rpy_to_axis_angle     | r, p, y, degs=False   |
| r, p, y | axis_angle_to_rpy     | ax, ang, degs=False   |
| ax, ang | dcm_to_axis_angle     | C, degs=False         |
| C       | axis_angle_to_dcm     | ax, ang, degs=False   |
| ax, ang | quat_to_axis_angle    | q, degs=False         |
| q       | axis_angle_to_quat    | ax, ang, degs=False   |
| r, p, y | dcm_to_rpy            | C, degs=False         |
| C       | rpy_to_dcm            | r, p, y, degs=False   |
| C       | rot                   | ang, ax=2, degs=False |
| r, p, y | quat_to_rpy           | q, degs=False         |
| q       | rpy_to_quat           | r, p, y, degs=False   |
| C       | quat_to_dcm           | q                     |
| q       | dcm_to_quat           | C                     |

**Reference-frame Conversions**

| Returns         | Name                  | Parameters                             |
| --------------- | --------------------- | -------------------------------------- |
| xe, ye, ze      | geodetic_to_ecef      | lat, lon, hae, degs=False              |
| lat, lon, hae   | ecef_to_geodetic      | xe, ye, ze, degs=False                 |
| xt, yt, zt      | ecef_to_tangent       | xe, ye, ze, xe0, ye0, ze0, ned=True    |
| xe, ye, ze      | tangent_to_ecef       | xt, yt, zt, xe0, ye0, ze0, ned=True    |
| xc, yc, zc      | geodetic_to_curlin    | lat, lon, hae, lat0, lon0, hae0,       |
|                 |                       | ned=True, degs=False                   |
| lat, lon, hae   | curlin_to_geodetic    | xc, yc, zc, lat0, lon0, hae0,          |
|                 |                       | ned=True, degs=False                   |
