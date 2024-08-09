'''Gempy model builder class:
    Intended use for distributed probabalistic model generation or,
    if you would just like to create model objects from observation data'''

"""
Parameters:
    surface_points:    *.CSV for gempy surface point inputs ()
    orientations:      *.CSV for gempy formatted orientations
    extents:           [list] 3D model extents in any units you would like [xmin,xmax,ymin,ymax,zmin,zmax]
    formation_map_type:[dict] dictionary keys are ordered model formation groups, 
                                values must be a [list] of the element names [str], and a single variable, 
                                choices are from Stack Relation type (FAULT, ERODE, ONLAP) e.g. {"Befeld_fault" : ['Belfeld' , FAULT],
                                                                                                      "Cenezoic": ['NSG', ERODE],
                                                                                                     "Mesozoic" : ['Mesozoic', ONLAP],}
    fault_relations: [bool, matrix] must be square MxN dimensional matrix with lengths equal to the number groups defined in formation map
    data_path: [str] pointer to input data *.CSV (surface and orientation points)
    refinement: [int] refinement calculation in Gempy solver, default is 6
    project_name: [str] to set model metadata
    **kwargs: [TODO, pass kwargs to gempy_viewer class]
    
    kwargs:
        model_name: [string] desired model name
        data_path: [string] path to the input csv surface or orientation files
        
"""



"""
Comes with some output functions:

    return_geo_data: this returns a computed geo-model from the input params

    return_3d_plot_inputs: This is a visualization function to look at input data
"""


import gempy as gp
import gempy_viewer as gpv
from gempy_engine.core.data.stack_relation_type import StackRelationType

class create_gempy_model(object):

    def __init__(self, surface_points, orientations, extents, formation_map_type, fault_relations, data_path, refinement=6, project_name='my project', **kwargs):
    
            
        # Stack realtions references, should probably be handled in the input...
            FAULT = StackRelationType.FAULT
            ERODE = StackRelationType.ERODE
            ONLAP = StackRelationType.ONLAP
            
            
        #Keyword Args assingment
            self.data_path = kwargs.get('data_path')   # eg.. 'https://raw.githubusercontent.com/cgre-aachen/gempy_data/master/'
            self.project_name = kwargs.get('model_name')  # This is the project name
            if self.project_name == '':
                self.project_name = 'No_Name'
    
        #Required arguments 
            self.surface_points = data_path + surface_points
            self.orients = data_path + orientations
            self.extent = extents
            
            #formations are held as the first value in the formation_map_type dictionary
            formation_map = {key: value[0] for key, value in formation_map_type.items()}

            #stack relation is held as
            stack_relation = {key: value[1] for key, value in formation_map_type.items()}
        
        # Create a GeoModel instance
            data = gp.create_geomodel(
                project_name=project_name,
                extent=self.extent,
                refinement=refinement,
                importer_helper=gp.data.ImporterHelper(
                    path_to_orientations=self.orients,
                    path_to_surface_points=self.surface_points
                    )
                )
        # Map geological series to surfaces
            gp.map_stack_to_surfaces(
                gempy_model=data,
                mapping_object=formation_map
                )
        # Define fault groups
            for i, relation in zip(range(len(stack_relation)), stack_relation):
                data.structural_frame.structural_groups[i].structural_relation = stack_relation[relation]
                
        # Set Fault relationships
            data.structural_frame.fault_relations = fault_relations
            
            
            
                                
            #data.structural_frame.structural_groups[0].structural_relation = StackRelationType.FAULT
            #data.structural_frame.fault_relations = np.array([[0,0,0,1], [0,0,0,1],[0,0,0,1],[0,0,0,0]])
            #data.structural_frame.structural_groups[1].structural_relation = StackRelationType.FAULT
            #data.structural_frame.fault_relations = np.array([[0,0,0,1],[0,0,0,1],[0,0,0,1],[0,0,0,0]])
            #data.structural_frame.structural_groups[2].structural_relation = StackRelationType.FAULT
        # Define NSG group
            #data.structural_frame.structural_groups[3].structural_relation = StackRelationType.ERODE
            
        # Define fault groups
            #data.structural_frame.structural_groups[2].structural_relation = StackRelationType.ERODE
        # Compute the geological model
        #    gp.compute_model(data)
        #    self.geo_data = data
            self.data = data
            
    def return_geo_data(self):
        # Compute the geological model with the model inputs and return to object
        
        #return gp.compute_model(self.data)
        gp.compute_model(self.data)
        self.geo_data = self.data
        return self.geo_data
    
    def return_3d_plot_inputs(self, show_data=True, show_boundaries=True, show_lith=False, kwargs_notebook_plotter=True):
        return gpv.plot_3d(self.data, show_data=show_data, show_boundaries=show_boundaries, show_lith=show_lith, kwargs_plotter={'notebook' : kwargs_notebook_plotter})
