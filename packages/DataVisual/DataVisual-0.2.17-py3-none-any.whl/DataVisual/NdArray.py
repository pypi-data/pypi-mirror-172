#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass

import DataVisual.Tables as Table
import MPSPlots.Plots as Plots




class DataV(object):
    def __init__(self, array, Xtable, Ytable, **kwargs):

        self.Data   = array

        self.Xtable = Xtable if isinstance(Xtable, Table.XTable) else Table.XTable(Xtable) 
   
        self.Ytable = Ytable if isinstance(Ytable, Table.YTable) else Table.YTable(Ytable) 



    @property
    def Shape(self):
        return self.Data.shape


    def Mean(self, axis: str):
        """Method compute and the mean value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the mean value of axis.

        """
        Array = numpy.mean(self.Data, axis=axis.Position)

        return DataV(Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)



    def Std(self, axis: str):
        """Method compute and the std value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the std value of axis.

        """

        Array = numpy.mean(self.Data, axis=axis.Position)

        return DataV(array=Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)


    def Weights(self, Weight, axis):
        """Method add weight to array in the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the std value of axis.

        """


        Array = numpy.multiply(self.Data, Weight, axis =self.Xtable.NameTable[axis])
        return DataV(array=Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)

        return Array


    def Rsd(self, axis: str):
        """Method compute and the rsd value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.
        rsd is defined as std/mean.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the rsd value of axis.

        """

        Array  = numpy.std(self.Data, axis=self.Xtable.NameTable[axis] ) \
                /numpy.mean(self.Data, axis=self.Xtable.NameTable[axis] )

        return DataV(array=Array, Xtable=[x for x in self.Xtable if x != axis], Ytable=self.Ytable)


    def Plot(self, x, y, Normalize=False, xScale='linear', yScale='linear', Std=None, xScaleFactor=None, **kwargs):
        Fig = Plots.Scene(UnitSize=(11,4.5))

        x.UpdateUnit(xScaleFactor)

        ax = Plots.Axis(Row       = 0,
                          Col       = 0,
                          xLabel    = x.Label,
                          yLabel    = y.Label,
                          Title     = None,
                          Grid      = True,
                          xScale    = xScale,
                          Legend    = True,
                          yScale    = yScale)

        Fig.AddAxes(ax)

        if Normalize: y.Normalize()

        if Std is not None:
            Artists = self.PlotSTD(x=x, y=y, Fig=Fig, ax=ax, Std=Std, **kwargs)
        else:
            Artists = self.PlotNormal(x=x, y=y, Fig=Fig, ax=ax, **kwargs)

        ax.AddArtist(*Artists)

        return Fig


    def PlotNormal(self, x, y, Fig, ax):
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Parameters
        ----------
        x : str
            Key of the self dict which represent the abscissa.
        Scale : str
            Options allow to switch between log and linear scale ['log', 'linear'].

        """  
        Artist = []

        for Y in self.Ytable:

            if Y is not y: continue

            Slicer, CommonLabel = self.Xtable.GetSlicer(x)

            for idx, DiffLabel in Slicer:
                Label = Y.Legend + DiffLabel

                y = self.Data[(*idx, Y.Position)]

                if numpy.iscomplexobj(Y):
                    Artist.append( Plots.Line(X=x.Values, Y=y.real, Label=Label + " real") )
                    Artist.append( Plots.Line(X=x.Values, Y=y.imag, Label=Label + " imag") )
                else:
                    Artist.append( Plots.Line(X=x.Values, Y=y, Label=Label) )

        Artist.append( Plots.Text(Text=CommonLabel, Position=[0.9, 0.9], FontSize=8) )

        return Artist




    def PlotSTD(self, x, y, Fig, ax, Polar=False, Std=None):
        """Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Parameters
        ----------
        x : str
            Key of the self dict which represent the abscissa.
        Scale : str
            Options allow to switch between log and linear scale ['log', 'linear'].

        """
        Artist = []

        for Y in self.Ytable:

            if Y is not y: continue

            axSTD = self.Xtable.GetPosition(Std)

            Ystd = self.Data.std( axis=axSTD )
            Ymean = self.Data.mean( axis=axSTD )

            Slicer, CommonLabel = self.Xtable.GetSlicer(x, Exclude=Std)

            for idx, DiffLabel in Slicer:
                Label = Y.Legend + DiffLabel

                artist = Plots.STDLine(X=x.Values, YMean=Ymean[( *idx, Y.Position )], YSTD=Ystd[( *idx, Y.Position )], Label=Label)

                Artist.append( artist )

        Artist.append( Plots.Text(Text=CommonLabel, Position=[0.9, 0.9], FontSize=8) )

        return Artist


    def __str__(self):
        name = [parameter.Name for parameter in self.Ytable]

        newLine = '\n' + '=' * 120 + '\n'

        text =  f'PyMieArray \nVariable: {name.__str__()}' + newLine

        text += "Parameter" + newLine

        for xParameter in self.Xtable:
            text += f"""| {xParameter.Label:40s}\
            | dimension = {xParameter.Name:30s}\
            | size      = {xParameter.GetSize()}\
            \n"""

        text += newLine

        text += "Numpy data array is accessible via the <.Data> attribute"

        return text
