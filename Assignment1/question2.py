from vtk import *

# load_data
reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_3D.vti')
reader.Update()
pdata = reader.GetOutput()

# color transfer function
ColorTransferFunction = vtkColorTransferFunction()
ColorTransferFunction.AddRGBPoint(-4931.54,0,1,1)
ColorTransferFunction.AddRGBPoint(-2508.95,0,0,1)
ColorTransferFunction.AddRGBPoint(-1873.9,0,0,0.5)
ColorTransferFunction.AddRGBPoint(-1027.16,1,0,0)
ColorTransferFunction.AddRGBPoint(-298.031,1,0.4,0)
ColorTransferFunction.AddRGBPoint(2594.97,1,1,0)

# opacity transfer function
OpacityTransferFunction = vtkPiecewiseFunction()
OpacityTransferFunction.AddPoint(-4931.54,1.0)
OpacityTransferFunction.AddPoint(101.815,0.002)
OpacityTransferFunction.AddPoint(2594.97,0.0)

# Create a volume property
VolumeProperty = vtkVolumeProperty()
VolumeProperty.SetColor(ColorTransferFunction)
VolumeProperty.SetScalarOpacity(OpacityTransferFunction)

# Create a smart volume mapper
VolumeMapper = vtkSmartVolumeMapper()
VolumeMapper.SetInputConnection(reader.GetOutputPort())

# Create a volume
volume = vtkVolume()
volume.SetMapper(VolumeMapper)
volume.SetProperty(VolumeProperty)

# Create an outline filter
OutlineFilter = vtkOutlineFilter()
OutlineFilter.SetInputConnection(reader.GetOutputPort())

# Create a mapper for the outline
OutlineMapper = vtkPolyDataMapper()
OutlineMapper.SetInputConnection(OutlineFilter.GetOutputPort())

# Create an actor for the outline
OutlineActor = vtkActor()
OutlineActor.SetMapper(OutlineMapper)
OutlineActor.GetProperty().SetLineWidth(5)
OutlineActor.GetProperty().SetColor(0, 0, 0)  # Set outline color to black

# Prompt user for Phong shading
PhongShading = input("Do you want to use Phong shading? (yes/no): ").lower()

# Create a renderer, render window, and interactor
renderer = vtkRenderer()
RenderWindow = vtkRenderWindow()
RenderWindow.SetSize(1000, 1000)  # Set render window size
RenderWindow.AddRenderer(renderer)
RenderWindowInteractor = vtkRenderWindowInteractor()
RenderWindowInteractor.SetRenderWindow(RenderWindow)

if PhongShading == "yes":
    # Enable Phong shading
    VolumeProperty.ShadeOn()
    # Set Phong shading parameters
    VolumeProperty.SetAmbient(0.5)
    VolumeProperty.SetDiffuse(0.5)
    VolumeProperty.SetSpecular(0.5)

# Add the volume and outline to the renderer
renderer.AddVolume(volume)
renderer.AddActor(OutlineActor)

# Set background color
renderer.SetBackground(1, 1, 1)

# Render and start interaction
RenderWindow.Render()
RenderWindowInteractor.Start()
