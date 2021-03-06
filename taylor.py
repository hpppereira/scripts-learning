#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""
Taylor diagram (Taylor, 2001) test implementation.
 
http://www-pcmdi.llnl.gov/about/staff/Taylor/CV/Taylor_diagram_primer.htm
"""
 
__version__ = "Time-stamp: <2012-02-17 20:59:35 ycopin>"
__author__ = "Yannick Copin <yannick.copin@laposte.net>"
 
import numpy as NP
import matplotlib.pyplot as PLT
 
class TaylorDiagram(object):
    """Taylor diagram: plot model standard deviation and correlation
    to reference (data) sample in a single-quadrant polar plot, with
    r=stddev and theta=arccos(correlation).
    """
 
    def __init__(self, refstd, radmax=1.5, fig=None, rect=111, label='_'):
        """Set up Taylor diagram axes, i.e. single quadrant polar
        plot, using mpl_toolkits.axisartist.floating_axes. refstd is
        the reference standard deviation to be compared to.
        """
 
        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as FA
        import mpl_toolkits.axisartist.grid_finder as GF
 
        self.refstd = refstd            # Reference standard deviation
 
        tr = PolarAxes.PolarTransform()
 
        # Correlation labels
        rlocs = NP.concatenate((NP.arange(10)/10.,[0.95,0.99]))
        tlocs = NP.arccos(rlocs)        # Conversion to polar angles
        gl1 = GF.FixedLocator(tlocs)    # Positions
        tf1 = GF.DictFormatter(dict(zip(tlocs, map(str,rlocs))))
 
        # Standard deviation axis extent
        self.smin = 0
        self.smax = radmax*self.refstd
 
        ghelper = FA.GridHelperCurveLinear(tr,
                                           extremes=(0,NP.pi/2, # 1st quadrant
                                                     self.smin,self.smax),
                                           grid_locator1=gl1,
                                           tick_formatter1=tf1,
                                           )
 
        if fig is None:
            fig = PLT.figure()
 
        ax = FA.FloatingSubplot(fig, rect, grid_helper=ghelper)
        fig.add_subplot(ax)
 
        # Adjust axes
        ax.axis["top"].set_axis_direction("bottom")  # "Angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")
 
        ax.axis["left"].set_axis_direction("bottom") # "X axis"
        ax.axis["left"].label.set_text("Standard deviation")
 
        ax.axis["right"].set_axis_direction("top")   # "Y axis"
        ax.axis["right"].toggle(ticklabels=True)
        ax.axis["right"].major_ticklabels.set_axis_direction("left")
 
        ax.axis["bottom"].set_visible(False)         # Useless
        
        # Contours along standard deviations
        ax.grid(False)
 
        self._ax = ax                   # Graphical axes
        self.ax = ax.get_aux_axes(tr)   # Polar coordinates
 
        # Add reference point and stddev contour
        # print "Reference std:", self.refstd
        l, = self.ax.plot([0], self.refstd, 'k*',
                          ls='', ms=10, label=label)
        t = NP.linspace(0, NP.pi/2)
        r = NP.zeros_like(t) + self.refstd
        self.ax.plot(t,r, 'k--', label='_')
 
        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = [l]
 
    def add_sample(self, stddev, corrcoef, *args, **kwargs):
        """Add sample (stddev,corrcoeff) to the Taylor diagram. args
        and kwargs are directly propagated to the Figure.plot
        command."""
 
        l, = self.ax.plot(NP.arccos(corrcoef), stddev,
                          *args, **kwargs) # (theta,radius)
        self.samplePoints.append(l)
 
        return l
 
    def add_rms_contours(self, levels=5, **kwargs):
        """Add constant centered RMS difference contours."""
 
        rs,ts = NP.meshgrid(NP.linspace(self.smin,self.smax),
                            NP.linspace(0,NP.pi/2))
        # Compute centered RMS difference
        rms = NP.sqrt(self.refstd**2 + rs**2 - 2*self.refstd*rs*NP.cos(ts))
        
        contours = self.ax.contour(ts, rs, rms, levels, **kwargs)
    
    def add_stddev_contours(self, std, corr1, corr2, **kwargs):
        """Add a curved line with a radius of std between two points
        [std, corr1] and [std, corr2]"""

        t = NP.linspace(NP.arccos(corr1), NP.arccos(corr2)) 
        r = NP.zeros_like(t) + std
        return self.ax.plot(t,r,'red', linewidth=2)
    
    def add_contours(self,std1,corr1,std2,corr2, **kwargs):
        """Add a line between two points
        [std1, corr1] and [std2, corr2]"""
        
        t = NP.linspace(NP.arccos(corr1), NP.arccos(corr2)) 
        r = NP.linspace(std1, std2)

        return self.ax.plot(t,r,'red',linewidth=2)
 
