import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.collections import LineCollection

class MyTerPlot:
    def __init__(self, x_values, y_values, mesh_values):
        self.x_values = x_values
        self.y_values = y_values
        self.mesh_values = mesh_values

    def get_ternary_plot(self):
        
        # create a triangulation out of these points
        T = tri.Triangulation(self.x_values, self.y_values)

        fig,axx = plt.subplots(figsize=(8, 7))
        # plot the contour
        axx.tricontourf(self.x_values, self.y_values, T.triangles, self.mesh_values, cmap='gist_rainbow', levels=35)

        # create the grid
        corners = np.array([[0, 0], [1, 0], [0.5,  np.sqrt(3)*0.5]])
        triangle = tri.Triangulation(corners[:, 0], corners[:, 1])

        # creating the grid
        refiner = tri.UniformTriRefiner(triangle)
        trimesh = refiner.refine_triangulation(subdiv=4)

        # plotting the mesh
        axx.triplot(trimesh,'k--', lw=0.75)
        corner_srch = np.r_[corners, corners[[0],:]]
        c_tol = 1e-09
        for i in range(corner_srch.shape[0]-1):
            m_slope = (corner_srch[i+1,1]-corner_srch[i,1]) / (corner_srch[i+1,0]-corner_srch[i,0])
            c_intercept = -m_slope*corner_srch[i+1,0] + corner_srch[i+1,1]
            edge_ls = []
            for j,k in zip(trimesh.x, trimesh.y):
                edge_ls.append(abs(m_slope*j + c_intercept - k)<c_tol)
        labels = trimesh.x[edge_ls]

        ax = plt.gca()
        tick_lines = LineCollection(np.c_[trimesh.x[edge_ls], trimesh.y[edge_ls], 
                                        trimesh.x[edge_ls]-0.025, trimesh.y[edge_ls]+0.020].reshape(-1, 2, 2), color="k", lw=2)
        ax.add_collection(tick_lines)
        for i in range(trimesh.x[edge_ls].shape[0]):
            plt.text(trimesh.x[edge_ls][i]-0.05, trimesh.y[edge_ls][i]+0.01, str(labels[i]), va="center", ha="center")
    
    def get_future_meth():
        pass