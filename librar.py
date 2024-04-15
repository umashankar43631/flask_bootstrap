from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import os
import shutil
import plotly.graph_objects as go
import plotly.express as px