'''Gempy model builder class:
    Intended use for distributed probabalistic model generation or,
    if you would just like to create model objects from observation data'''

"""
Parameters:
    surface_points: *.CSV for gempy surface point inputs ()
    orientations: *.CSV for gempy formatted orientations
    extents: [list] 3D model extents in any units you would like [xmin,xmax,ymin,ymax,zmin,zmax]
    kwargs:
        model_name: [string] desired model name
        data_path: [string] path to the input csv surface or orientationfiles
"""



"""
Comes with some output functions:

    return_geo_data: this returns a computed model from the model inputed

    return_3d_plot_inputs: This is a visualization function to look at input data
"""


import gempy
from gempy_engine.core.data.stack_relation_type import StackRelationType

class create_gempy_model(object):

    def __init__(self, surface_points, orientations, extents, **kwargs):
    #Keyword Args assingment
            '''_priors = kwargs.get('prior')    # choices are "const", "geometric", "neg_binomial"'''
        
            self.data_path = kwargs.get('data_path')   # eg.. 'https://raw.githubusercontent.com/cgre-aachen/gempy_data/master/'
            self.project_name = kwargs.get('model_name')  # This is the project name
            if self.project_name == '':
                self.project_name = 'No_Name'
    
    #Required arguments 
            self.surface_points = data_path + surface_points
            self.orients = data_path + orientations
            self.extent = extents
            
    
        
        # Create a GeoModel instance
            data = gp.create_geomodel(
                project_name=project_name,
                extent=self.extent,
                refinement=6,
                importer_helper=gp.data.ImporterHelper(
                    path_to_orientations=self.orients,
                    path_to_surface_points=self.surface_points
                )
            )
        # Map geological series to surfaces
            gp.map_stack_to_surfaces(
            gempy_model=data,
            mapping_object={
                "Tegelen_fault": 'Tegelen',
                "Dulkener_fault": 'Dulkener',
                "Befeld_fault" : 'Belfeld',
                "Stratigraphy": ('NSG', 'Mesozoic', 'Namurian', 'Zeeland')
                #"Paleozoic Series": ('Top_Carboniferous', 'Top_zeeland')
            }
            )
        # Define fault groups
            data.structural_frame.structural_groups[0].structural_relation = StackRelationType.FAULT
            data.structural_frame.fault_relations = np.array([[0,0,0,1], [0,0,0,1],[0,0,0,1],[0,0,0,0]])
            
            data.structural_frame.structural_groups[1].structural_relation = StackRelationType.FAULT
            data.structural_frame.fault_relations = np.array([[0,0,0,1],[0,0,0,1],[0,0,0,1],[0,0,0,0]])
        
            data.structural_frame.structural_groups[2].structural_relation = StackRelationType.FAULT
        # Define NSG group
            data.structural_frame.structural_groups[3].structural_relation = StackRelationType.ERODE
            
        # Define fault groups
            #data.structural_frame.structural_groups[2].structural_relation = StackRelationType.ERODE
        # Compute the geological model
        #    gp.compute_model(data)
        #    self.geo_data = data
            self.data = data
            
    def return_geo_data(self):
        # Compute the geological model with the model inputs and return to object
        
        return gp.compute_model(self.data)
        #self.geo_data = self.data
        #return self.geo_data
    
    def return_3d_plot_inputs(self, show_data=True, show_boundaries=True, show_lith=False ):
        return gpv.plot_3d(self.data, show_data=show_data, show_boundaries=show_boundaries, show_lith=show_lith)
