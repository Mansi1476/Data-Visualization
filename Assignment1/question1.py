from vtk import *

def marching_squares(numCells, C, DataArray, data, points, cells):
    for i in range(numCells):
        cell = data.GetCell(i)
        pid1 = cell.GetPointId(0)
        pid2 = cell.GetPointId(1)
        pid3 = cell.GetPointId(3)
        pid4 = cell.GetPointId(2)
        
        val1 = DataArray.GetTuple1(pid1)
        val2 = DataArray.GetTuple1(pid2)
        val3 = DataArray.GetTuple1(pid3)
        val4 = DataArray.GetTuple1(pid4)
        
        cas = 0
        if val1 >= C and val2 >= C and val3 >= C and val4 >= C:
            continue
        if val1 <= C and val2 <= C and val3 <= C and val4 <= C:
            continue
        
        point1 = data.GetPoint(pid1)
        point2 = data.GetPoint(pid2)
        point3 = data.GetPoint(pid3)
        point4 = data.GetPoint(pid4)
        p1=p2=p3=p4=0
        if (val1 - C) * (val2 - C) < 0:
            t = (C - val1) / (val2 - val1)
            x = (1 - t) * point1[0] + t * point2[0]
            y = (1 - t) * point1[1] + t * point2[1]
            z = (1 - t) * point1[2] + t * point2[2]
            p1id = points.InsertNextPoint(x, y, z)
            p1=1
            cas += 8
        
        if (val2 - C) * (val3 - C) < 0:
            t = (C - val2) / (val3 - val2)
            x = (1 - t) * point2[0] + t * point3[0]
            y = (1 - t) * point2[1] + t * point3[1]
            z = (1 - t) * point2[2] + t * point3[2]
            p2id = points.InsertNextPoint(x, y, z)
            p2=1
            cas += 4
        
        if (val3 - C) * (val4 - C) < 0:
            t = (C - val3) / (val4 - val3)
            x = (1 - t) * point3[0] + t * point4[0]
            y = (1 - t) * point3[1] + t * point4[1]
            z = (1 - t) * point3[2] + t * point4[2]
            p3id = points.InsertNextPoint(x, y, z)
            p3=1
            cas += 2
        
        if (val4 - C) * (val1 - C) < 0:
            t = (C - val4) / (val1 - val4)
            x = (1 - t) * point4[0] + t * point1[0]
            y = (1 - t) * point4[1] + t * point1[1]
            z = (1 - t) * point4[2] + t * point1[2]
            p4id = points.InsertNextPoint(x, y, z)
            p4=1
            cas += 1
        
        if cas == 5 or cas == 10:
            if p1 and p3:
                line = vtkPolyLine()
                line.GetPointIds().SetNumberOfIds(2)
                line.GetPointIds().SetId(0, p1id)
                line.GetPointIds().SetId(1, p3id)
                cells.InsertNextCell(line)
            
            if p2 and p4:
                line = vtkPolyLine()
                line.GetPointIds().SetNumberOfIds(2)
                line.GetPointIds().SetId(0, p2id)
                line.GetPointIds().SetId(1, p4id)
                cells.InsertNextCell(line)
        
        else:
            if p1 and p2:
                line = vtkPolyLine()
                line.GetPointIds().SetNumberOfIds(2)
                line.GetPointIds().SetId(0, p1id)
                line.GetPointIds().SetId(1, p2id)
                cells.InsertNextCell(line)

            if p2 and p3:
                line = vtkPolyLine()
                line.GetPointIds().SetNumberOfIds(2)
                line.GetPointIds().SetId(0, p2id)
                line.GetPointIds().SetId(1, p3id)
                cells.InsertNextCell(line)

            if p3 and p4:
                line = vtkPolyLine()
                line.GetPointIds().SetNumberOfIds(2)
                line.GetPointIds().SetId(0, p3id)
                line.GetPointIds().SetId(1, p4id)
                cells.InsertNextCell(line)

            if p4 and p1:
                line = vtkPolyLine()
                line.GetPointIds().SetNumberOfIds(2)
                line.GetPointIds().SetId(0, p4id)
                line.GetPointIds().SetId(1, p1id)
                cells.InsertNextCell(line)

    return

reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

points = vtkPoints()
cells = vtkCellArray()

numCells = data.GetNumberOfCells()
dataArr = data.GetPointData().GetArray('Pressure')

C = float(input("Enter the isovalue: "))

marching_squares(numCells, C, dataArr, data, points, cells)

pdata = vtkPolyData()
pdata.SetPoints(points)
pdata.SetLines(cells)

writer = vtkXMLPolyDataWriter()
writer.SetInputData(pdata)
writer.SetFileName('Output.vtp')
writer.Write()
