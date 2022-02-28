# Implements various click models
import bisect
import pandas as pd
import numpy as np

def binary_func(x):
    if x > 0:
        return 1
    return 0

class Steps(object):
    '''
    Contains information on a built-in stepped function, and provides
    access to that function.
    '''

    def step(self, x):
        '''
        Returns the value of a stepped function evaluated at x.
        '''
        ind = bisect.bisect_right(self._xList, x)
        if (ind < len(self._steps)):
            return self._steps[ind][1]
        return self._finalY
    # End of step().

    _steps = tuple(sorted((
        (0.05, 0   ),
        (0.1 , 0.5 ),
        (0.3,  0.75),
    )))
    '''
    A sorted list of (x, y) pairs:
      (x0, y0),
      (x1, y1),
      ...
      (xN, yN)
    The function evalutes as:
      if (x < x0):
        return y0
      elif (x < x1):
        return y1
      ...
      elif (x < xN):
        return yN
      return _finalY
    Using a sorted list allows for faster lookup than linearly iterating.
    '''

    _finalY = 1
    '''
    See description for _steps.
    '''

    _xList = tuple(x for (x, y) in _steps)
    '''
    Just the x values from _steps.
    '''
# End of Steps class.
def step(x):
    return Steps().step(x)
# End of step().


# Given a click model type, transform the "grade" into an appropriate value between 0 and 1, inclusive
# This operates on the data frame and adds a "grade" column
#
def apply_click_model(data_frame, click_model_type="binary", downsample=True):
    if click_model_type == "binary":
        print("Binary click model") # if we have at least one click, count it as relevant
        data_frame["grade"] = data_frame["clicks"].apply(lambda x: binary_func(x))
        if downsample:
            data_frame = down_sample_buckets(data_frame)
    elif click_model_type == "ctr":
        data_frame["grade"] = (data_frame["clicks"]/data_frame["num_impressions"]).fillna(0)
        if downsample:
            data_frame = down_sample_continuous(data_frame)
    elif click_model_type == "heuristic":
        data_frame["grade"] = (data_frame["clicks"]/data_frame["num_impressions"]).fillna(0).apply(lambda x: step(x))
        if downsample:
            data_frame = down_sample_buckets(data_frame)
    return data_frame

# https://stackoverflow.com/questions/55119651/downsampling-for-more-than-2-classes
def down_sample_buckets(data_frame):
    g = data_frame.groupby('grade', group_keys=False)
    return pd.DataFrame(g.apply(lambda x: x.sample(g.size().min()))).reset_index(drop=True)


# Generate the probabilities for our grades and then use that to sample from
# from: https://stackoverflow.com/questions/63738389/pandas-sampling-from-a-dataframe-according-to-a-target-distribution
# If you want to learn more about this, see http://www.seas.ucla.edu/~vandenbe/236C/lectures/smoothing.pdf
def down_sample_continuous(data_frame):
    x = np.sort(data_frame['grade'])
    f_x = np.gradient(x)*np.exp(-x**2/2)
    sample_probs = f_x/np.sum(f_x)
    try: # if we have too many zeros, we can get value errors, so first try w/o replacement, then with
        sample = data_frame.sort_values('grade').sample(frac=0.8, weights=sample_probs, replace=False)
    except Exception as e:
        print("Unable to downsample, keeping original:\n%s" % e)
        sample = data_frame #data_frame.sort_values('grade').sample(frac=0.8, weights=sample_probs, replace=True)
    return sample

