import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

class OutlierDetector:
    def __init__(self, dataframe):
        self.df = dataframe.select_dtypes(include=['number'])

    def find_fences(self, columns=None, plot=False):
        '''
        columns: Can be a single string 'Col' or a list ['Col1', 'Col2']
        plot: If True, generates subplots for the provided list
        '''
        # Convert single string to a list for consistent processing
        if isinstance(columns, str):
            columns = [columns]
        elif columns is None:
            columns = self.df.columns.tolist()

        fence_report = {}

        # 1. Calculate Fences
        for col in columns:
            if col in self.df.columns:
                q1 = self.df[col].quantile(0.25)
                q3 = self.df[col].quantile(0.75)
                iqr = q3 - q1
                lf = round(float(q1 - 1.5 * iqr), 4)
                uf = round(float(q3 + 1.5 * iqr), 4)
                fence_report[col] = {"Lower Fence": lf, "Upper Fence": uf}

        # 2. Plotting Logic (Subplots)
        if plot and columns:
            num_cols = len(columns)
            grid_cols = 3  # Set how many charts per row
            grid_rows = math.ceil(num_cols / grid_cols)

            plt.figure(figsize=(15, 5 * grid_rows))
            
            for i, col in enumerate(columns):
                plt.subplot(grid_rows, grid_cols, i + 1)
                sns.boxplot(x=self.df[col], color='skyblue')
                
                # Add fence lines to the plot
                lf = fence_report[col]["Lower Fence"]
                uf = fence_report[col]["Upper Fence"]
                plt.axvline(lf, color='red', linestyle='--', alpha=0.6)
                plt.axvline(uf, color='red', linestyle='--', alpha=0.6)
                
                plt.title(f'Outliers in {col}')
            
            plt.tight_layout()
            plt.show()

        return fence_report


# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# class OutlierDetector:
#     def __init__(self, dataframe):
#         self.df = dataframe.select_dtypes(include=['number'])

#     def find_fences(self, column_name=None, plot=False):
#         '''Calculates fences and optionally plots a boxplot'''
        
#         # If a specific column is requested
#         if column_name:
#             if column_name not in self.df.columns:
#                 return f"Error: {column_name} not found."
            
#             # Calculate logic
#             q1 = self.df[column_name].quantile(0.25)
#             q3 = self.df[column_name].quantile(0.75)
#             iqr = q3 - q1
#             lf = round(float(q1 - 1.5 * iqr), 4)
#             uf = round(float(q3 + 1.5 * iqr), 4)

#             # --- Plotting Logic ---
#             if plot:
#                 plt.figure(figsize=(10, 4))
#                 sns.boxplot(x=self.df[column_name], color='skyblue')
#                 plt.title(f'Boxplot for {column_name} (Outlier Detection)')
#                 # Add visual lines for the fences
#                 plt.axvline(lf, color='red', linestyle='--', label=f'Lower Fence: {lf}')
#                 plt.axvline(uf, color='red', linestyle='--', label=f'Upper Fence: {uf}')
#                 plt.legend()
#                 plt.show()

#             return {"Lower Fence": lf, "Upper Fence": uf}

#         # Logic for all columns (default plot=False behavior)
#         fence_report = {}
#         for col in self.df.columns:
#             q1 = self.df[col].quantile(0.25)
#             q3 = self.df[col].quantile(0.75)
#             iqr = q3 - q1
#             fence_report[col] = {
#                 "Lower Fence": round(float(q1 - 1.5 * iqr), 4),
#                 "Upper Fence": round(float(q3 + 1.5 * iqr), 4)
#             }
#         return fence_report
