from vtk import *
#load data
import numpy as np
reader = vtkXMLImageDataReader()
filename = "tornado3d_vector.vti"
reader.SetFileName(filename)
reader.Update()
data = reader.GetOutput()
bounds = data.GetBounds()
point_data = data.GetPointData()
points1 = vtkPoints()


def boundcheck(point):
    x, y, z = point
    min_x, max_x, min_y, max_y, min_z, max_z = bounds
    if min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z:
        return True
    else:
        return False

   
    

def interpolation(point):
    points=vtkPoints()
    points.InsertNextPoint(point)
    pdata = vtkPolyData()
    pdata.SetPoints(points)
    probefilter = vtkProbeFilter()
    probefilter.SetInputData(pdata)
    probefilter.SetSourceData(data)

    probefilter.Update()

    outputdata = probefilter.GetOutput()
    interpolatedvalues = outputdata.GetPointData().GetVectors().GetTuple3(0)
    return interpolatedvalues

def streamline(seed):
    seed = np.array(seed)
    point = seed.copy()
    step_size = 0.05
    stream_points = [seed]
    half = 0.5
    for i in range(1000):

        vect = np.array(interpolation(point))
        vect1 = np.array(interpolation(point + half * step_size * vect))
        vect2 = np.array(interpolation(point + half * step_size * vect1))
        vect3 = np.array(interpolation(point + step_size * vect2))
        next_point = point + (step_size/6.0) * (vect + 2*vect1 + 2*vect2 + vect3)
        if not boundcheck(next_point):
            break
        stream_points.append(next_point)
        point = next_point

    point = seed.copy()
    step_size  = -0.05
    for i in range(1000):
        vect = step_size * np.array(interpolation(point))
        vect1 = step_size *np.array(interpolation(point + half * vect))
        vect2 = step_size *np.array(interpolation(point + half *  vect1))
        vect3 = step_size *np.array(interpolation(point +  vect2))
        next_point = point +   (vect + 2*vect1 + 2*vect2 + vect3)/6
        if not boundcheck(next_point):
            break
        stream_points.insert(0,next_point)
        point = next_point

    points = vtkPoints()

    # Create a cell array and add the line to it
    lines = vtkCellArray()

    for i,point in enumerate(stream_points):
        points.InsertNextPoint(point)
        if i>0:
            line = vtkLine()
            line.GetPointIds().SetId(0, i - 1)
            line.GetPointIds().SetId(1, i)
            lines.InsertNextCell(line)


    polydata=vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)
    writer = vtkXMLPolyDataWriter()
    writer.SetInputData(polydata)
    writer.SetFileName('Streamline_Output1.vtp')
    writer.Write()


def take_point_input():
    x = float(input("Enter the x-coordinate: "))
    y = float(input("Enter the y-coordinate: "))
    z = float(input("Enter the z-coordinate: "))
    return (x, y, z)

#Enter input point
point = take_point_input()
streamline(point)

