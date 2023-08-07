import matplotlib
from matplotlib.backends.backend_qt5agg import(
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavTool,
    )
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width,height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        
class MplCanvas3d(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width,height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        super().__init__(fig)