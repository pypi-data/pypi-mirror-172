This is a fork from [OC_SORT](https://github.com/noahcao/OC_SORT). Only the [main implementations](https://github.com/noahcao/OC_SORT/tree/master/trackers/ocsort_tracker) are used.

# Adjustments
- Map 1-1 each input detection result with a tracked result so a detection will receive either a valid value or `None`. Check `map_result` variable in `tracker.py` for detailed implementation.
- Only accept post-processed detections (e.g: boxes are scaled to original image size).
- Adjust stale tracklet removal logic by using 2 new arguments:
    - `hit_inertia_min`: minimum number of hits for a tracklet to be considered alive. `hits` will be initiated with `hit_inertia_min+1`. A tracklet will update `hits` depending on input detection. Check `KalmanBoxTracker.update` and `KalmanBoxTracker.is_alive` function in `tracker.py` for detailed implementation.
    - `hit_inertia_max`: hard cap of `hits`.

# Installation
```
pip install techainer-ocsort
```

# Example
- Prepare a video for face detection. Reconfig video name accordingly in `tests/test_ocsort.py`.
- Replace our face detection with yours in `tests/test_ocsort.py`. Make sure that tracker input format is `[[x1,y1,x2,y2,score],[x1,y1,x2,y2,score],...]`.
- Run `python tests/test_ocsort.py`. Output will be saved in your configed video name. 