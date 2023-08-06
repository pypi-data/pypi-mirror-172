# IQM-VIS
Image Quality Metric Visualision

Extendable user interface for the assessment of transformations on image metrics.

## Minimal Example of API
Define image path and name:
```python
image_path = {'X': 'images/image2.jpg'}
```
Define metric function to use:
```python
metric = {'MAE': lambda im1, im2: np.abs(im1 - im2).mean()}
```
Define a metric image function:
```python
metric_im = {'MAE': lambda im1, im2: np.abs(im1 - im2)}
```
Define a transformation and its parameter value range:
```python
trans = {'brightness': {'min':-1, 'max':1, 'init_value':0, 'function':lambda im, val: np.clip(im + val, 0, 1)}}
```
Use the API to create the UI:
```python
import api
api.make_UI(image_path, metric, metric_im, trans)
```
![Alt text](images/ui-simple.png?raw=true "Simple UI")

## Additional items
Add more entries to the dictionaries to include extra items examples found [here](examples/multiple.py)

![Alt text](images/ui-multi.png?raw=true "Multi UI")


## Installation (todo: `setup.py` and pypi)
Currently under development so install from GitHub. First create a new python venv, eg. using conda
```
$ conda create -n iqm_vis python=3.9
```
Activate env:
```
$ conda activate iqm_vis
```
Clone repo
```
$ git clone git@github.com:mattclifford1/IQA_GUI.git
$ cd IQA_GUI
```
Install requirements
```
$ pip install -r requirements.txt
```
Run MWE
```
$ python examples/simple.py
```

## To do - datasets
Need to 'scroll' through dataset:
  - directory of images?
  - image paths in list?
  - image paths in csv file?
