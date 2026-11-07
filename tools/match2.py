import json,sys,numpy as np
from PIL import Image
sys.path.insert(0,'tools')
from grid import grid
import match as M   # reuses norm + font (re-renders templates; skip by loading T)
