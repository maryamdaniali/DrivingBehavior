import os
from pathlib import Path
import csv
import pandas as pd

class Loadfile:
    """
    This class loads csv files based on three main challanges.
    1.Kid-ball
    2.Truck following
    3.Car pull out
    Output: data dictionary
    """
    def __init__(self):
        self.data = {}
    def kid_ball_reader(self,path,category):
        """ Method for the kid-ball challange
        path: file path
        category: label (healthy or MS)
        """
        with open(path) as f:
            rows = iter(csv.reader(f, delimiter=','))
            row = next(rows)
            self.data['id'] = path.parent.name
            self.data['label'] = category
            self.data['challenge'] = next(rows)[0]

            while not (len(row) > 1 and row[0] == 'Speeds'):
                row = next(rows)
            row = next(rows)
            while len(row)==5:
                self.data[row[0]] = row[2]
                row = next(rows)
            
            while not (len(row) >= 1 and row[0] == 'Deviation from Ideal Center Lane (ft)'):
                row = next(rows)
            fields = next(rows)
            values = next(rows)

            for idx in range(len(fields)):
                self.data[fields[idx]] = values[idx]

            while not (len(row) >= 1 and row[0] == 'Closest Approach (ft)'):
                row = next(rows)
            fields = next(rows)
            values = next(rows)

            for idx in range(len(fields)):
                self.data[fields[idx]] = values[idx]

            while not (len(row) > 1 and row[0] == 'Time'):
                row = next(rows)
            row = next(rows)
            while len(row)==4:
                self.data[row[0]] = row[1]
                row = next(rows)

        return self            
    def following_reader(self, path, category):
        """ Method for the truck following challange
        path: file path
        category: label (healthy or MS)
        """
        with open(path) as f:
            rows = iter(csv.reader(f, delimiter=','))
            row = next(rows)
            self.data['id'] = path.parent.name
            self.data['label'] = category
            self.data['challenge'] = next(rows)[0]

            while not (len(row) > 1 and row[0] == 'Speeds'):
                row = next(rows)
            row = next(rows)
            while len(row)==3:
                self.data[row[0]] = row[2]
                row = next(rows)
            
            while not (len(row) >= 1 and row[0] == 'Elapsed'):
                row = next(rows)
            fields = row
            values = next(rows)

            for idx in range(len(fields)):
                self.data[fields[idx]] = values[idx]

            while not (len(row) >= 1 and row[0] == 'Vehicle Spacing - Straight Line(ft)'):
                row = next(rows)
            fields = next(rows)
            values = next(rows)

            for idx in range(len(fields)):
                self.data['Straight_line_'+fields[idx]] = values[idx]

            while not (len(row) >= 1 and row[0] == 'Vehicle Spacing - C/L Dist (ft)'):
                row = next(rows)
            fields = next(rows)
            values = next(rows)

            for idx in range(len(fields)):
                self.data['Curve_'+fields[idx]] = values[idx]
        return self            
    def pull_out_reader(self, path, category):
        """ Method for the car pull out challange
        path: file path
        category: label (healthy or MS)
        """
        with open(path) as f:
            rows = iter(csv.reader(f,delimiter =','))
            row = next(rows)
            self.data['id'] = path.parent.name
            self.data['label'] = category
            self.data['challenge'] = next(rows)[0]

            while not (len(row) >= 1 and row[0] == 'Event'):
                row = next(rows)
            row = next(rows)
            while len(row)>=2:
                self.data['Event_'+row[0]] = row[1]
                row = next(rows)

            while not (len(row) > 1 and row[0] == 'Speeds'):
                row = next(rows)
            row = next(rows)
            while len(row)==3:
                self.data['Speed_'+row[0]] = row[2]
                row = next(rows)

            while not (len(row) >= 1 and row[0] == 'Doff'):
                row = next(rows)
            fields = row
            values = next(rows)
            for idx in range(len(fields)):
                self.data['Entryline_'+fields[idx]] = values[idx]

            while not (len(row) >= 1 and row[0] == 'Elapsed'):
                row = next(rows)
            fields = row
            values = next(rows)
            for idx in range(len(fields)):
                self.data[fields[idx]] = values[idx]

            while not (len(row) >= 1 and row[0] == 'toTarg'):
                row = next(rows)
            fields = row
            values = next(rows)
            for idx in range(len(fields)):
                self.data['Approach_'+fields[idx]] = values[idx]

            while not (len(row) >= 1 and row[0] == 'Dmin'):
                row = next(rows)
            fields = row
            values = next(rows)
            for idx in range(len(fields)):
                self.data['Separation_'+fields[idx]] = values[idx]

            while not (len(row) > 1 and row[0] == 'Vble'):
                row = next(rows)
            row = next(rows)
            while ( len(row)==3 and row[0]!='Pedal_Conf'):
                self.data['Braking_'+row[0]] = row[1]
                row = next(rows)
                
        return self


if __name__ == "__main__":
    """ Define paths to the csv files"""
    curr_dir = Path().absolute()
    rootdir_healthy = curr_dir.parent/"Databases"/"Sim data"/"Data"/"HC"
    rootdir_MS = curr_dir.parent/"Databases"/"Sim data"/"Data"/"MS"


    
    curr_challenge = 'KidBallStats.csv' 
    file_list_healthy = [f for f in rootdir_healthy.glob('**/*') if (f.is_file() and f.name.endswith(curr_challenge))]
    file_list_MS = [f for f in rootdir_MS.glob('**/*') if (f.is_file() and f.name.endswith(curr_challenge))]

    data = {}
    df_kid_ball = pd.DataFrame() 
    file_load = Loadfile() 
 
    for file in file_list_healthy:
        file_load.data = {}  
        file_load.kid_ball_reader(file, 'Healthy')
        data[file.name] = file_load.data
        if len(df_kid_ball) == 0:
            df_kid_ball = pd.DataFrame([file_load.data])
        else:
            df_kid_ball = df_kid_ball.append([file_load.data])

        
    for file in file_list_MS:
        file_load.data = {}  
        file_load.kid_ball_reader(file, 'MS')
        data[file.name] = file_load.data
        if len(df_kid_ball) == 0:
            df_kid_ball = pd.DataFrame([file_load.data])
        else:
            df_kid_ball = df_kid_ball.append([file_load.data])
    df_kid_ball.index = range(1,len(df_kid_ball)+1)



    curr_challenge = 'FollowStats.csv' 
    file_list_healthy = [f for f in rootdir_healthy.glob('**/*') if (f.is_file() and f.name.endswith(curr_challenge))]
    file_list_MS = [f for f in rootdir_MS.glob('**/*') if (f.is_file() and f.name.endswith(curr_challenge))]

    data = {}
    df_following = pd.DataFrame() 
    file_load = Loadfile() 
 
    for file in file_list_healthy:
        file_load.data = {}  
        file_load.following_reader(file, 'Healthy')
        data[file.name] = file_load.data
        if len(df_following) == 0:
            df_following = pd.DataFrame([file_load.data])
        else:
            df_following = df_following.append([file_load.data])

        
    for file in file_list_MS:
        file_load.data = {}  
        file_load.following_reader(file, 'MS')
        data[file.name] = file_load.data
        if len(df_following) == 0:
            df_following = pd.DataFrame([file_load.data])
        else:
            df_following = df_following.append([file_load.data])
    df_following.index = range(1,len(df_following)+1)

    
    
    curr_challenge = 'PullOutStats.csv' 
    file_list_healthy = [f for f in rootdir_healthy.glob('**/*') if (f.is_file() and f.name.endswith(curr_challenge))]
    file_list_MS = [f for f in rootdir_MS.glob('**/*') if (f.is_file() and f.name.endswith(curr_challenge))]

    data = {}
    df_pull_out = pd.DataFrame() 
    file_load = Loadfile() 
 
    for file in file_list_healthy:
        file_load.data = {}  
        file_load.pull_out_reader(file, 'Healthy')
        data[file.name] = file_load.data
        if len(df_pull_out) == 0:
            df_pull_out = pd.DataFrame([file_load.data])
        else:
            df_pull_out = df_pull_out.append([file_load.data])

        
    for file in file_list_MS:
        file_load.data = {}  
        file_load.pull_out_reader(file, 'MS')
        data[file.name] = file_load.data
        if len(df_pull_out) == 0:
            df_pull_out = pd.DataFrame([file_load.data])
        else:
            df_pull_out = df_pull_out.append([file_load.data])
    df_pull_out.index = range(1,len(df_pull_out)+1)


    """ Save dataframe to pickled pandas object """
    df_kid_ball.to_pickle('df_kid_ball.plk') 
    df_following.to_pickle('df_following.plk')
    df_pull_out.to_pickle('df_pull_out.plk')

    # Load dataframe from pickled pandas object 
    # df= pd.read_pickle(file_name)   
    
    
    print('Done')