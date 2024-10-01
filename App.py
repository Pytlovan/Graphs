# graph_gui.py

import tkinter as tk                    # Used as the main GUI library
from tkinter import messagebox          # Used to show message boxes to the user
from matplotlib import pyplot as plt    # Used for plotting the graph
from Grafos import Graph                # Importing the Graph class from Grafos.py
from tkinter import ttk                 # Used for graph canvas on the GUI

class GraphApp:
    def __init__(self, root):
        #App Initialization
        self.graph = Graph()
        self.root = root
        self.root.title("Graph Analysis v0.3.2")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Variable Initialization
        self.fig = None     # Used on the draw_graph method
        self.file_path = None   # Used to check if there is a file_path for the current graph, and to quicksave a graph on the current file_path

        #------------------------------------------------#
        #Frames (Divs)

        #Main Frame
        self.frame = tk.Frame(root)                                             
        self.frame.pack(padx=10, pady=10)

        self.file_frame = tk.Frame(self.frame, height=10)
        self.file_frame.grid(row=0, column=0, columnspan=5, sticky='W')

        #Vertex Frame
        self.vertex_frame = tk.Frame(self.frame, bd=2, relief='raised')
        self.vertex_frame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        #Matrix Frame
        self.matrix_frame = tk.Frame(self.frame, bd=2, relief='raised')
        self.matrix_frame.grid(row=2, column=0, padx=5, columnspan=2, pady=5)

        #Searches Frame
        self.search_frame = tk.Frame(self.frame, bd=2, relief='raised')
        self.search_frame.grid(row=1,column=4, padx=5, pady=5)

        #Connectivity Frame
        self.connected_frame = tk.Frame(self.frame, bd=2, relief='raised')
        self.connected_frame.grid(row=2, column=4, padx=5, pady=5)

        #Subgraphs Frame
        self.subgraphs_frame = tk.Frame(self.frame, width=750, bd=2, relief='raised')
        self.subgraphs_frame.grid(row=2, column=2, pady=5, padx=5, sticky='S')

        #labels frame
        self.label_frame = tk.Frame(self.frame, bd=2, height=10)
        self.label_frame.grid(row=0, column=2, sticky='S')

        #Canvas Frame
        self.canvas_frame = ttk.Frame(self.frame, relief='raised')
        self.canvas_frame.grid(row=1, rowspan=2, column=2,pady=5,padx=5, sticky='N')

        #-------------------------------------------------#
        #File Buttons:
        self.saveas_button = tk.Button(self.file_frame, text='Save as', command=self.save_to_file)
        self.save_button = tk.Button(self.file_frame, text='Save', command=self.save)
        self.open_button = tk.Button(self.file_frame, text='Open', command=self.open_from_file)
        self.clear_button = tk.Button(self.file_frame, text='Clear', command=self.clear_graph)

        #File Widgets:
        self.saveas_button.grid(row=0, column=2, padx=5)
        self.save_button.grid(row=0, column=1,padx=5)
        self.open_button.grid(row=0, column=0, padx=5)
        self.clear_button.grid(row=0, column=3, padx=5)

        #Vertex Input
        self.vertex_label = tk.Label(self.vertex_frame, text="Vertex:")
        self.vertex_entry = tk.Entry(self.vertex_frame, width=5)

        #Vertex Buttons
        self.add_vertex_button = tk.Button(self.vertex_frame, text="Add", command=self.add_vertex)
        self.remove_vertex_button = tk.Button(self.vertex_frame, text="Remove", command = self.remove_vertex)

        #Vertex Widgets
        self.vertex_label.grid(row=0, column=0, padx=5)
        self.vertex_entry.grid(row=1, column=0, padx=5)
        self.add_vertex_button.grid(row=0, column=1, padx=5, sticky='W')
        self.remove_vertex_button.grid(row=1, column=1, padx=5,sticky="W")

        #Edge Input
        self.edge_label = tk.Label(self.vertex_frame, text="Edge:")
        self.edge_entry_u = tk.Entry(self.vertex_frame, width=5)
        self.edge_entry_v = tk.Entry(self.vertex_frame, width=5)

        #Edge Buttons
        self.add_edge_button = tk.Button(self.vertex_frame, text="Add", command=self.add_edge)
        self.remove_edge_button = tk.Button(self.vertex_frame, text="Remove", command=self.remove_edge)

        #Directed Checkbox
        self.is_directed = tk.BooleanVar()
        self.directed_checkbox = tk.Checkbutton(self.vertex_frame, text = "Directed", variable=self.is_directed, command=self.set_graph_type)

        #Edges Widgets
        self.edge_label.grid(row=0, column=2, padx=5, pady=5, sticky="E")
        self.edge_entry_u.grid(row=1, column=2, padx=5, pady=5, sticky="E")
        self.edge_entry_v.grid(row=2, column=2, padx=5, pady=5, sticky="E")
        self.add_edge_button.grid(row=0, column=3, padx=5, pady=5, sticky="W")
        self.remove_edge_button.grid(row=1, column=3, padx=5, pady=5, sticky="W")
        self.directed_checkbox.grid(row=2, column=3, padx=5, pady=5, sticky="W")

        #-------------------------------------------------#
        #Matrix Positioning
        self.matrix_label = tk.Label(self.matrix_frame, text="Adjacency Matrix:")
        self.matrix_text = tk.Text(self.matrix_frame, height=32, width=53, state='disabled')

        #Matrix Widgets
        self.matrix_label.grid(row=0, column=0, pady=5)
        self.matrix_text.grid(row=1, column=0, pady=5, padx=5)

        #-------------------------------------------------#
        #Search Inputs
        self.start_label = tk.Label(self.search_frame, text="Start: ")
        self.start_entry = tk.Entry(self.search_frame, width=5)
        self.search_label = tk.Label(self.search_frame, text="Search: ")
        self.search_entry = tk.Entry(self.search_frame, width=5)
        
        #Search Buttons
        self.bfs_button = tk.Button(self.search_frame, text="BFS", command=self.run_bfs)
        self.dfs_button = tk.Button(self.search_frame, text="DFS", command=self.run_dfs)
        
        #Search Results
        self.result_label = tk.Label(self.search_frame, text="Search Result:")
        self.result_text = tk.Text(self.search_frame, height=2, width=53, state='disabled')
        
        #Search Widgets
        self.start_label.grid(row=0, column=0, pady=5)
        self.start_entry.grid(row=0, column=1, pady=5)
        self.search_label.grid(row=1, column=0, pady=5)
        self.search_entry.grid(row=1,column=1, pady=5)
        self.bfs_button.grid(row=2,column=0, pady=5)
        self.dfs_button.grid(row=2, column=1, pady=5)
        self.result_label.grid(row=3,column=0, columnspan=2, pady=5)
        self.result_text.grid(row=4,column=0, columnspan=2, pady=5, padx=5)

        #-------------------------------------------------#
        #Connectivity Inputs
        self.conn_label = tk.Label(self.connected_frame, text="Start/End:")
        self.conn_entry = tk.Entry(self.connected_frame, width=5)

        #Connectivity Buttons
        self.ftd_button = tk.Button(self.connected_frame, text="FTD", command = self.run_ftd)
        self.fti_button = tk.Button(self.connected_frame, text="FTI", command = self.run_fti)

        self.is_connected_button = tk.Button(self.connected_frame, text = 'Is Connected?', command = self.check_connectivity)

        #Connectivity Results
        self.ftdi_label = tk.Label(self.connected_frame, text="Results")
        self.ftdi_text = tk.Text(self.connected_frame, height=26, width=53, state='disabled')
        self.is_connected_text = tk.Text(self.connected_frame, height = 1, width=10, state='disabled', font=("Helvetica", 12, "italic"))

        #Connectivity Widgets
        self.conn_label.grid(row=0, column=0, pady=5)
        self.conn_entry.grid(row=0, column=1, pady=5)
        self.ftd_button.grid(row=1, column=0, pady=5)
        self.fti_button.grid(row=1, column=1, pady=5)
        self.ftdi_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.ftdi_text.grid(row=3, column=0, columnspan=2, pady=5, padx=5)
        self.is_connected_text.grid(row=4, column=1, pady=5)
        self.is_connected_button.grid(row=4, column=0, pady=5)

        #-------------------------------------------------#
       
        #Subgraph Positioning
        self.subgraphs_label = tk.Label(self.subgraphs_frame, text="Subgraphs:")
        self.subgraphs_text = tk.Text(self.subgraphs_frame, height = 8, width = 92, state='disabled')

        #Subgraph Widgets
        self.subgraphs_label.grid(row=0, column=0, pady=5)
        self.subgraphs_text.grid(row=1, column=0, pady=5, padx=5, sticky='W')
       
        #-------------------------------------------------#

        #Canvas Positioning
        self.canvas_label = tk.Label(self.label_frame, text = "Canvas:")

        #Canvas Widgets
        self.canvas_label.grid(column=0, row=0, pady=5, padx=5)

        #Log Positioning
        self.log_label = tk.Label(self.vertex_frame, text="Log:")
        self.log_text = tk.Text(self.vertex_frame, height=3, width=53, state='disabled', font=("Helvetica", 10, "italic"))

        #Log Widgets
        self.log_label.grid(row=3, column=0, pady=5)
        self.log_text.grid(row=3, column=1, columnspan = 3, pady=5, padx=5)

        self.generate_graph()
        self.update_matrix()

    def set_graph_type(self):
        self.graph.directed = self.is_directed.get()

    def add_vertex(self):
        vertex = self.vertex_entry.get()
        if vertex:
            msg = self.graph.add_vertex(vertex)
            self.update_log(msg)
            self.update_matrix()
            self.update_subgraphs()
            self.generate_graph()
            self.vertex_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a vertex value.")

    def add_edge(self):
        u = self.edge_entry_u.get()
        v = self.edge_entry_v.get()
        if u and v:
            msg = self.graph.add_edge(u, v)
            self.update_log(msg)
            self.update_matrix()
            self.update_subgraphs()
            self.generate_graph()
            self.edge_entry_u.delete(0, tk.END)
            self.edge_entry_v.delete(0, tk.END) 

        else:
            messagebox.showwarning("Input Error", "Please enter both vertices for the edge.")
    
    def remove_vertex(self):
        vertex = self.vertex_entry.get()
        if vertex:
            msg = self.graph.remove_vertex(vertex)
            self.update_log(msg)
            self.update_matrix()
            self.update_subgraphs()
            self.generate_graph()
            self.vertex_entry.delete(0, tk.END) 
        else:
            messagebox.showwarning("Input Error", "Please enter a vertex value.")
    
    def remove_edge(self):
        u = self.edge_entry_u.get()
        v = self.edge_entry_v.get()
        if u and v:
            msg = self.graph.remove_edge(u, v)
            self.update_log(msg)
            self.update_matrix()
            self.update_subgraphs()
            self.generate_graph()
            self.update = True
            self.edge_entry_u.delete(0, tk.END)
            self.edge_entry_v.delete(0, tk.END) 
        else:
            messagebox.showwarning("Input Error", "Please enter both vertices for the edge.")

    def run_bfs(self):
        start = self.start_entry.get()
        search = self.search_entry.get()
        if start in self.graph.graph:
            if search in self.graph.graph:
                result = self.graph.bfs(start, search)
            else:
                result = self.graph.bfs(start)
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, ' '.join(result))
            self.start_entry.delete(0, tk.END)
            self.search_entry.delete(0,tk.END)
            self.result_text.config(state='disabled')
        else:
            messagebox.showwarning("Input Error", "Start vertex not in graph.")
    
    def run_dfs(self):
        start = self.start_entry.get()
        search = self.search_entry.get()
        if start in self.graph.graph:
            if search in self.graph.graph:
                result = self.graph.dfs(start, search)
            else:
                result = self.graph.dfs(start)
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, ' '.join(result))
            self.start_entry.delete(0, tk.END)
            self.search_entry.delete(0,tk.END)
            self.result_text.config(state='disabled')

        else:
            messagebox.showwarning("Input Error", "Start vertex not in graph.")

    def run_ftd(self):
        start = self.conn_entry.get()
        if start in self.graph.graph:
            set, result = self.graph.ftd(start)
            self.ftdi_text.config(state='normal')
            self.ftdi_text.delete(1.0,tk.END)
            self.ftdi_text.insert(tk.END, f'Set: {' '.join(map(str, sorted(list(set))))}\n')
            for vertex, level in result.items():
                self.ftdi_text.insert(tk.END, f'{vertex}: {level}\n')
            self.conn_entry.delete(0, tk.END)
            self.ftdi_text.config(state='disabled')
        else:
            messagebox.showwarning("Input Error", "Vertex not in graph.")

    def run_fti(self):
        end = self.conn_entry.get()
        if end in self.graph.graph:
            set, result = self.graph.fti(end)
            self.ftdi_text.config(state='normal')
            self.ftdi_text.delete(1.0,tk.END)
            self.ftdi_text.insert(tk.END, f'Set: {' '.join(map(str, sorted(list(set))))}\n')
            for vertex, level in result.items():
                self.ftdi_text.insert(tk.END, f'{vertex}: {level}\n')
            self.conn_entry.delete(0, tk.END)
            self.ftdi_text.config(state='disabled')
        else:
            messagebox.showwarning("Input Error", "Vertex not in graph.")

    def check_connectivity(self):
        vertices = sorted(list(self.graph.graph.keys()))
        if vertices:
            set, result = self.graph.connectivity(vertices[0])
            self.is_connected_text.config(state='normal')
            self.is_connected_text.delete(1.0, tk.END)
            self.is_connected_text.insert(tk.END, f'{result}')
            self.is_connected_text.config(state='disabled')
        else:
            messagebox.showwarning("Empty Graph", "No vertex in graph.")

    def update_subgraphs(self):
        vertices = sorted(list(self.graph.graph.keys()))
        if vertices:
            subgraphs = self.graph.find_all_subgraphs(vertices[0])
        else:
            subgraphs = []
        
        self.subgraphs_text.config(state='normal')
        self.subgraphs_text.delete(1.0, tk.END)
        for i, subgraph in enumerate(subgraphs):
            row_label = i+1
            row_data = ', '.join(map(str, sorted(list(subgraph))))
            self.subgraphs_text.insert(tk.END, f"{row_label}) {row_data}\n")
        
        self.subgraphs_text.config(state='disabled')

    def update_matrix(self):
        vertices = sorted(list(self.graph.graph.keys()))

        self.matrix_text.config(state='normal')
        self.matrix_text.delete(1.0, tk.END)

        self.matrix_text.insert(tk.END, "Vertices:\n")
        self.matrix_text.insert(tk.END, ', '.join(vertices) + "\n\n")

        self.matrix_text.insert(tk.END, "Adjacency Matrix:\n")
        
        matrix = self.graph.adjacency_matrix()

        self.matrix_text.insert(tk.END, '   ' + ' '.join(vertices) + '\n\n')

        for i, row in enumerate(matrix):
            row_label = vertices[i] 
            row_data = ' '.join(map(str, row))
            self.matrix_text.insert(tk.END, f"{row_label}  {row_data}\n")
        
        self.matrix_text.config(state='disabled')

    def update_log(self, msg):
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, msg)
        self.log_text.config(state='disabled')

    def generate_graph(self):
        if self.fig is not None:
            plt.close(self.fig)
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        self.fig = self.graph.draw_graph(self.canvas_frame)

    def save_to_file(self):
        if self.graph.graph != {}:
            saved, self.file_path = self.graph.saveas_graph()
            if saved:
                self.update_log('Graph saved!')
            else:
                messagebox.showinfo("Canceled","Save aborted")
        else:
            messagebox.showwarning("No graph detected", "There is no graph created or loaded currently.")
    
    def save(self):
        if not self.file_path:
            self.save_to_file()
        else:
            saved = self.graph.save_graph(self.file_path)
            if saved:
                self.update_log('Graph saved!')
            else:
                messagebox.showerror("Error", "Invalid file or path")
            
    def open_from_file(self):
        loaded, self.file_path = self.graph.open_graph()
        if loaded:
            self.update_log('Graph loaded!')
            self.update_matrix()
            self.update_subgraphs()
            self.generate_graph()
        else:
            messagebox.showinfo("Canceled","Load aborted")

    def clear_graph(self):
        if self.graph.graph != {}:
            print(self.graph.graph)
            clear = messagebox.askyesno("Clear Graph","Do you really want to clear the current graph?")
            if clear:
                save = messagebox.askyesno("Clear Graph","Do you want to save before clearing the current graph?")
                if save:
                    self.save_to_file()
                self.graph.clear_graph()
                self.update_matrix()
                self.update_subgraphs()
                self.generate_graph()
                self.update_log('Graph cleared!')
            else:
                self.update_log("No changes!")
        else:
            messagebox.showwarning("No graph detected", "There is no graph created or loaded currently.")
    
    def on_closing(self):
        if self.fig is not None:
            plt.close(self.fig)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
