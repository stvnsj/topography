import sys
import numpy as np
import utils
import levelCad
from pprint import pprint

def strToFltKey (string) :
    try:
        return float(string)
    except:
        return -1

class Point :

    
    def __init__ (
            self,
            num,
            start = False,
            point_uncorrected = 0.0,
            back_delta = 0.0,
            front_delta = 0.0,
            dm = np.array([]),
            intermediate = [],
            str_dm = np.array([])
    ):
        
        self.num                     = num  # Ordinal number of this point in the segment
        self.start                   = start # Boolean. True if it is the first point in the segment
        
        self.dm                      = dm # List of kilometers
        self.intermediate            = intermediate # list of deltas for each dm
        
        self.back_delta              = back_delta
        self.front_delta             = front_delta
        
        self.point_uncorrected       = point_uncorrected # Uncorrected height for each dm
        self.instr_uncorrected       = 0.0 # Uncorreted instr 
        
        # self.point_corrected  = []
        self.point_corrected  = 0.0
        self.instr_corrected  = 0.0
        self.size = len(dm) + 1
        self.str_dm = str_dm
        
        
    def __str__ (self):
        DM = f'{self.dm}'
        ATRAS = f'{self.back_delta}'
        INTERM = f'{self.intermediate}'
        ADELANTE = f'{self.front_delta}'
        A = f'{self.instr_corrected}'
        B = f'{self.point_corrected}'
        return f'{DM}  -  {ATRAS}  - {INTERM}  -  {ADELANTE}  -  {A}  -   {B} \n'
 
    def build (self, prev = None):
        """initializes point_uncorrected and instr_uncorrected
        interacting with previous control point."""
        if not self.start:
            self.__init_point_uncorrected (prev)
        self.__init_instr_uncorrected ()
        
    
    def __init_point_uncorrected (self, prev):
        instr = prev.instr_uncorrected
        self.point_uncorrected = utils.round(instr - self.front_delta)
    
    def __init_instr_uncorrected (self) :
        self.instr_uncorrected = utils.round(self.point_uncorrected + self.back_delta)
        
 
    def correct_instr (self, correction):
        self.instr_corrected = utils.round(self.instr_uncorrected + correction * self.num)
 
    def correct_point (self):
        self.point_corrected = utils.round(self.instr_corrected - self.intermediate)
 
    def get_table (self):
        # X = np.column_stack((
        #     np.round(self.dm[:,None],3),
        #     np.round(self.point_corrected[:,None],3),
            
        # ))
        return (
            self.str_dm, # Dm of the point 
            np.round(self.point_corrected,3)) # Corrected height of the point
    
    ###########
    # GETTERS #
    ###########
    def get_point_uncorrected (self):
        return self.point_uncorrected
    def get_instr_uncorrected (self):
        return self.instr_uncorrected
    def get_intermediate_size (self): 
        return len(self.intermediate)







class Segment :
    
    def __init__ (self, 
                  pr0, pr1, 
                  first_height, 
                  last_height, 
                  cplst=[], 
                  start_points = [], 
                  end_points=[], 
                  end_points_list = []
                  ):
        self.pr0 = pr0 # string name of pr0
        self.pr1 = pr1 # string name of pr1
        self.pr_dict = {}

        # I have to define a new criteria that assigns the 
        # positive or negative sign to each segment. 
        
        if ((pr0, pr1) not in end_points_list) and ((pr1, pr0) not in end_points_list):
            self.positive = True
            end_points_list.append((pr0,pr1))
        else:
            self.positive = False
        
        self.pr = (utils.pr_number(pr0),self.positive)
        
        self.points = cplst
        
        self.diff = 0.0
        
        self.length = len(cplst)
     
        self.first_height = first_height
        self.last_height  = last_height
        
        self.point_uncorrected = last_height
        
        self.ref_height = last_height
        
        self.size = 0
        
        self.__build()

        self.print_registro_nivelacion ()

 
    def __build (self):
        
        for i , cp in enumerate(self.points) :
            
            if i == 0:
                cp.build()
                continue
            
            cp.build(self.points[i-1])
        
        point_uncorrected = self.points[-1].get_point_uncorrected()
     
        self.diff = np.round (self.ref_height - point_uncorrected , 3)
        
        self.size = len(self.points) - 2
        
        for cp in self.points:
            
            cp.correct_instr(self.diff / self.size);
            cp.correct_point()
        
        if utils.pr_number(self.pr0) < utils.pr_number(self.pr1):
            for p in self.points:
                self.pr_dict.update({dm:(self.pr0,self.pr1) for dm in p.str_dm})
        else :
            for p in self.points:
                self.pr_dict.update({dm:(self.pr1,self.pr0) for dm in p.str_dm})
                
    def __str__ (self):
        return f'Punto A : {self.pr0} , Punto B: {self.pr1}, positive : {self.positive}'
    
        
    def get_pr_dict(self):
        return self.pr_dict
    

    def print_registro_nivelacion (self
            
    ) : 
        return 1
    

    def minimal_stuff (f) : 
        np.abs(f) < 0.01 
        

    def get_registro_nivelacion (self) :

        segment_size = 0
        INSTR = self.points[0].instr_corrected

        for pp in self.points :
            segment_size += pp.get_intermediate_size() + 1

        n, m = segment_size, 6
        registro_table = np.full((n, m), "", dtype="U20")
        registro_table [0][0]  = self.pr0
        registro_table [0][5]  = f'{self.first_height}'
        registro_table [-1][0] = self.pr1
        CURR_ROW = 0

        for i, pp in enumerate(self.points):
            registro_table[CURR_ROW][1]= f'{pp.back_delta}'
            registro_table[CURR_ROW][4]= f'{pp.instr_corrected}'
            registro_table[CURR_ROW][3]= f'{pp.front_delta}'
            if i > 0:
                registro_table[CURR_ROW][5] = f'{INSTR - pp.back_delta}'
                INSTR = pp.instr_corrected
            CURR_ROW += 1
            N = len(pp.intermediate)
            for i in range(N):
                registro_table[CURR_ROW + i][2]=f'{pp.intermediate[i]}'
                registro_table[CURR_ROW + i][0]=f'{pp.dm[i]}'
                registro_table[CURR_ROW + i][5]=f'{pp.point_corrected[i]}'
            CURR_ROW += N

        registro_table [0][3]  = ""
        registro_table [-1][1] = ""
        registro_table [-1][4] = ""
        registro_table [-1][5] = f'{self.last_height}'

        
        

        
            
        return registro_table




    def get_table (self):
        lst = [p.get_table() for p in self.points]
        dm_list, pnt_list = list(zip(*lst))
        return (np.concatenate(dm_list),np.concatenate(pnt_list))

class Circuit :
    
    def __init__ (self, positive, negative, trigonometric = None):
        
        # self.positive and self.negative are lists
        # of Segment instances.
        self.positive = positive
        self.negative = negative
        
        self.pr_dict  =  {}
        self.trig_dict = self.__build_trig_dict__(trigonometric)
        
        for s in positive:
            self.pr_dict.update(s.get_pr_dict())
            
        for s in negative:
            self.pr_dict.update(s.get_pr_dict())

        self.positive_list = []
        self.negative_list = [] 
        self.get_data () 
    
    def __build_trig_dict__ (self, table) :
        if table is None:
            return {}
        dic = {table[i][0] : np.round(float(table[i][1]),3) for i in range(len(table))}
        return dic
    
    def get_data (self) :

        lst1 = [s.get_table() for s in self.positive]
        lst2 = [s.get_table() for s in self.negative]

        lst = lst1 + lst2

        dm_segments, z_segments = list(zip(*lst))

        dm_list = np.concatenate(dm_segments)
        z_list  = np.concatenate(z_segments)

        #pos_dm, pos_pnt = (np.concatenate(dm_list1, dm_list2),np.concatenate(pnt_list1,pnt_list2))

        positive_set = set () 
        negative_set = set () 

        for dm in dm_list :
            if not (dm in positive_set):
                positive_set.add(dm)
            else:
                negative_set.add(dm)

        table = list(zip(dm_list , z_list))


        for pair in table :

            dm = pair[0] 

            if dm in positive_set:
                self.positive_list.append(pair)
                positive_set.remove(dm)

            elif dm in negative_set:
                self.negative_list.append(pair)
                negative_set.remove(dm)




  
    # Refactored positive tables: 
    def get_positive_table(self):
        # self.positive no longer is the source of the 
        # positive dm
        # lst = [s.get_table() for s in self.positive]
        dm_list, pnt_list = list(zip(*self.positive_list))
        return dm_list, pnt_list
    
    def get_negative_table(self):
        #lst = [s.get_table() for s in self.negative]
        dm_list, pnt_list = list(zip(*self.negative_list))
        return dm_list, pnt_list
 
 
    
    # This is used for the REPORT
    #
    # Trig: All DM not in the "libreta" and in the trig table
    # must be incorporated into the report.
    def write_circuit_table(self, filename):
        
        pos_dm, pos_pnt = self.get_positive_table()
        neg_dm, neg_pnt = self.get_negative_table()
        intersection    = np.intersect1d(pos_dm, neg_dm)
        union           = np.union1d(pos_dm, neg_dm)
        positive_dict   = dict (zip(pos_dm,pos_pnt))
        negative_dict   = dict (zip(neg_dm,neg_pnt))
        full_table = np.empty((0, 8))

        
        
        
        for dm in union:
            
            if dm == "":
                continue
            
            if dm in intersection:
                
                positive_h = positive_dict.get(dm)
                negative_h = negative_dict.get(dm)
                
                # Content of the report cells.
                if (not np.isnan(positive_h)) and (not np.isnan(negative_h)):
                    dif = np.round(np.absolute(float(positive_h) - float(negative_h)),3)
                    mean = np.mean([float(positive_h),float(negative_h)])
                elif (not np.isnan(positive_h)):
                    dif = 0.000
                    mean = float(positive_h)
                elif (not np.isnan(negative_h)):
                    dif = 0.000
                    mean = float(negative_h)
                else :
                    dif = 0.000
                    mean = 0.0
                
                new_row = np.array([[
                    dm,
                    utils.format_float(positive_h) if not np.isnan(positive_h) else "VACIO",
                    utils.format_float(negative_h) if not np.isnan(negative_h) else "VACIO",
                    utils.format_float(dif),
                    utils.format_float(mean),
                    self.pr_dict.get(dm)[0],
                    self.pr_dict.get(dm)[1],
                    "FT" if dif > 0.01 else ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            if dm in positive_dict:
                positive_h = positive_dict.get(dm)
                negative_h = "SIN COTA"
                dif        = 0.000
                mean       = positive_h
                new_row = np.array([[
                    dm,
                    utils.format_float(positive_h) if not np.isnan(positive_h) else "VACIO",
                    negative_h,
                    utils.format_float(dif),
                    utils.format_float(mean),
                    self.pr_dict.get(dm)[0],
                    self.pr_dict.get(dm)[1],
                    ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
                
            if dm in negative_dict:
                positive_h = "SIN COTA"
                negative_h = negative_dict.get(dm)
                dif        = 0.0
                mean       = negative_h
                new_row = np.array([[
                    dm,
                    positive_h,
                    utils.format_float(negative_h) if not np.isnan(negative_h) else "VACIO",
                    utils.format_float(dif),
                    utils.format_float(mean),
                    self.pr_dict.get(dm)[0],
                    self.pr_dict.get(dm)[1],
                    ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
        
        for dm in self.trig_dict:
            if dm in union:
                print(f'dm={dm} ya se encuentra en la libreta')
                continue
            
            if not utils.is_float(self.trig_dict.get(dm)):
                print(f'Cota de {dm} no es un valor numérico')
                continue
            
            trig_height = self.trig_dict.get(dm)
            
            new_row = np.array([[
                dm,
                utils.format_float(trig_height),
                utils.format_float(trig_height),
                utils.format_float(0.000),
                utils.format_float(trig_height),
                '',
                '',
                "TRIG"
            ]])
            
            full_table = np.append(full_table, new_row, axis=0)
        
        
        num_index = np.where([utils.is_float(x) for x in full_table[:,0]])
        str_index = np.where([not utils.is_float(x) for x in full_table[:,0]])
        ordered_num_index = np.argsort(full_table[num_index][:,0].astype(float))
        
        output = np.vstack((
            np.array([["DM", "IDA","VUELTA","DIF","MEDIA","PR-A","PR-B","TOLERANCIA"]]),
            full_table[num_index][ordered_num_index], # Use the ordered_num_index over the num_index indexed full table.
            full_table[str_index]
        ))
        
        with open(filename, "w") as f:
            np.savetxt(f,output,delimiter=',',fmt='%s')
        
        print("OPERACION EXITOSA")
 
 
    # This is the table used for the longitudinal ANNEX 3
    def get_report_long (self):
        
        pos_dm, pos_pnt = self.get_positive_table()
        neg_dm, neg_pnt = self.get_negative_table()
        
        intersection    = np.intersect1d(pos_dm, neg_dm)
        union           = np.union1d(pos_dm, neg_dm)
        
        positive_dict   = dict (zip(pos_dm,pos_pnt))
        negative_dict   = dict (zip(neg_dm,neg_pnt))
        
        full_table = np.empty((0, 6))
        
        for dm in intersection:
            if dm == "" or not utils.is_float(dm):
                continue
                
            positive_h = utils.round(positive_dict.get(dm))
            negative_h = utils.round(negative_dict.get(dm))
                
            if np.isnan(positive_h):
                print(f'Revisar dm={dm}')
                continue
                    
            if np.isnan(negative_h):
                print(f'Revisar dm={dm}')
                continue
                
            dif        = np.absolute(positive_h - negative_h)
            mean       = np.mean([positive_h,negative_h])
                
            new_row = np.array([[
                utils.round(float(dm)),
                positive_h,
                negative_h,
                dif,
                utils.round(mean),
                -1 # Trig field
            ]])
            full_table = np.append(full_table, new_row, axis=0)
        
        
        for dm in self.trig_dict:
            
            if dm in union:
                print(f'dm={dm} ya se encuentra en la libreta')
                continue
            
            if not utils.is_float(self.trig_dict.get(dm)):
                print(f'Cota de {dm} no es un valor numérico')
                continue
            
            trig_height = self.trig_dict.get(dm)
            
            new_row = np.array([[
                utils.round(float(dm)),
                utils.round(float(trig_height)),
                utils.round(float(trig_height)),
                utils.round(0.000),
                utils.round(float(trig_height)),
                1                
            ]])
            
            full_table = np.append(full_table, new_row, axis=0)
        
        num_index = np.where([utils.is_float(x) for x in full_table[:,0]])
        ordered_num_index = np.argsort(full_table[num_index][:,0].astype(float))
        
        output = np.vstack((full_table[num_index][ordered_num_index]))
        
        return output
 
 
 
    # This is the INPUT of adjusted heights for CROSS SECTIONS heights.
    def write_longitudinal(self, filename):
        
        pos_dm, pos_pnt = self.get_positive_table()
        neg_dm, neg_pnt = self.get_negative_table()
        intersection    = np.intersect1d(pos_dm, neg_dm)
        union           = np.union1d(pos_dm, neg_dm)
        positive_dict   = dict (zip(pos_dm,pos_pnt))
        negative_dict   = dict (zip(neg_dm,neg_pnt))
        full_table = np.empty((0, 3))
        
        for dm in union:
            
            if dm == "" or not utils.is_float(dm):
                continue
            
            if dm in intersection:
                
                positive_h = positive_dict.get(dm)
                negative_h = negative_dict.get(dm)
                
                dif = np.round(np.absolute(float(positive_h) - float(negative_h)),3)
                mean = np.mean([float(positive_h),float(negative_h)])
                
                if np.isnan(positive_h) or np.isnan(negative_h):
                    continue
                
                new_row = np.array([[
                    dm,
                    utils.format_float(mean),
                    "FT" if dif > 0.01 else ""
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            if dm in positive_dict:
                positive_h = positive_dict.get(dm)
                mean       = positive_h
                
                if np.isnan(positive_h):
                    continue
                
                new_row = np.array([[
                    dm,
                    utils.format_float(mean),
                    "COTA UNICA"
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
                
            if dm in negative_dict:
                negative_h = negative_dict.get(dm)
                mean       = negative_h
                if np.isnan(negative_h):
                    continue
                new_row = np.array([[
                    dm,
                    utils.format_float(mean),
                    "COTA UNICA"
                ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
        
        for dm in self.trig_dict:
            
            if dm in union:
                print(f'dm={dm} ya se encuentra en la libreta')
                continue
            
            if not utils.is_float(self.trig_dict.get(dm)):
                print(f'Cota de {dm} no es un valor numérico')
                continue
            
            trig_height = self.trig_dict.get(dm)
            
            new_row = np.array([[
                dm,
                utils.format_float(trig_height),
                "TRIG"
            ]])
            
            full_table = np.append(full_table, new_row, axis=0)
        
        num_index = np.where([utils.is_float(x) for x in full_table[:,0]])
        ordered_num_index = np.argsort(full_table[num_index][:,0].astype(float))
         
        with open(filename, "w") as f:
            np.savetxt(f,full_table[num_index][ordered_num_index],delimiter=',',fmt='%s')
    
 
    
    def plot(self, filename):
        
        pos_dm, pos_pnt = self.get_positive_table()
        neg_dm, neg_pnt = self.get_negative_table()
        
        intersection    = np.intersect1d(pos_dm, neg_dm)
        union           = np.union1d(pos_dm, neg_dm)
        
        positive_dict   = dict (zip(pos_dm,pos_pnt))
        negative_dict   = dict (zip(neg_dm,neg_pnt))
        
        full_table = np.empty((0, 2))
        
        for dm in union:
            
            if (dm == "") or (not utils.is_float(dm)):
                continue
            
            # DM's with two measurements 
            if dm in intersection:
                
                positive_h = positive_dict.get(dm) 
                negative_h = negative_dict.get(dm)
                
                if (not np.isnan(positive_h)) and (not np.isnan(negative_h)):
                    mean = np.mean([float(positive_h),float(negative_h)])
                elif (not np.isnan(positive_h)):
                    mean = float(positive_h)
                elif (not np.isnan(negative_h)):
                    mean = float(negative_h)
                else :
                    continue
                    
                new_row = np.array([[ np.round(float(dm),3), mean]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            # DM's with positive direction only
            if dm in positive_dict:
                positive_h = positive_dict.get(dm)
                if np.isnan(positive_h):
                    continue
                mean       = utils.round(positive_h)                
                new_row = np.array([[ np.round(float(dm),3), utils.round(mean) ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
            
            # DM's with negative direction only
            if dm in negative_dict:
                negative_h = negative_dict.get(dm)
                if np.isnan(negative_h):
                    continue
                mean       = utils.round(negative_h)
                new_row = np.array([[  np.round(float(dm),3), utils.round(mean) ]])
                full_table = np.append(full_table, new_row, axis=0)
                continue
        
        for dm in self.trig_dict:
            
            if dm in union:
                print(f'dm={dm} ya se encuentra en la libreta')
                continue
            
            if not utils.is_float(self.trig_dict.get(dm)):
                print(f'Cota de {dm} no es un valor numérico')
                continue
            
            trig_height = self.trig_dict.get(dm)
            
            new_row = np.array([[
                utils.round(float(dm)),
                utils.round(float(trig_height)),
            ]])
            
            full_table = np.append(full_table, new_row, axis=0)
        
        
        num_index = np.where([utils.is_float(x) for x in full_table[:,0]])
        ordered_num_index = np.argsort(full_table[num_index][:,0].astype(float))
        
        with open(filename, "w") as f:
            cad = levelCad.LevelCad(full_table[num_index][ordered_num_index])
            cad.write(f)






def parse_circuit (circuit_matrix, height_matrix, circuit_num_matrix = None, pr_num_matrix = None):
    start = 0
    end   = 1
    
    start_points = []
    end_points   = []
    end_points_list = []
    
    height_dict = dict(zip (utils.normalize_pr_array(height_matrix[:,0]), pr_num_matrix[:,1]))
    segment_list = []
    
    for i , row in enumerate(circuit_matrix):
        
        if row[0] != "" :
            start = i
        
        if row[2] != "":
            
            end = i
         
            pr0 = utils.normalize_pr(circuit_matrix[start][0])
            pr1 = utils.normalize_pr(circuit_matrix[end][2])

            h0  = height_dict[pr0.upper()]
            h1  = height_dict[pr1.upper()]
           
            seg = parse_segment(circuit_matrix[start:end+1], pr0, pr1, h0, h1, num_matrix=circuit_num_matrix[start:end+1],
                                start_points = start_points, end_points=end_points, end_points_list=end_points_list)
            segment_list.append(seg)
    
    return segment_list


def parse_segment (string_matrix, pr0, pr1, h0, h1, num_matrix=None, start_points= [], end_points= [], end_points_list=[] ):
    POINT_NUM = 0
    START = 0
    END   = 0
    N     = len(string_matrix)
 
    point_list = []
    
    for i, row in enumerate(string_matrix):
        
        # NULL followed by NULL    or     final NULL
        if (row[1] == "" and i == N - 1)   or   (row[1] == "" and string_matrix[i+1][1] == ""):
            first = True if POINT_NUM == 0 else False
            point = parse_point(POINT_NUM,first,h0,string_matrix[i:i+1],num_matrix[i:i+1])
            POINT_NUM += 1
            point_list.append(point)
            continue
        
        # NULL followed by NON-NULL
        if (row[1] == "" and  string_matrix[i+1][1] != ""):
            START = i
            continue
        
        # NON-NULL followed by NULL
        if (row[1] != "" and string_matrix[i+1][1] == ""):
            first = True if POINT_NUM == 0 else False
            point = parse_point(POINT_NUM,first,h0,string_matrix[START:i+1],num_matrix[START:i+1])
            POINT_NUM += 1
            point_list.append(point)
            continue 
 
    
    return Segment(
        utils.normalize_pr(pr0),
        utils.normalize_pr(pr1),
        h0, h1,
        point_list,
        start_points=start_points,
        end_points=end_points,
        end_points_list=end_points_list
    )


def parse_point (num, start, h0, string_matrix, num_matrix = None):
    
    back_delta   = 0.0 if np.isnan(num_matrix[0][3]) else num_matrix[0][3]
    front_delta  = 0.0 if np.isnan(num_matrix[0][5]) else num_matrix[0][5]
 
    point_uncorrected = h0 if start else 0.0
 
    dm = np.array([])
    im = np.array([])
 
    if len(string_matrix) > 1 :
        dm = num_matrix[1:,1]
        im = num_matrix[1:,4]
    
    point = Point(
        num,
        start=start,
        point_uncorrected=point_uncorrected,
        back_delta = back_delta,
        front_delta = front_delta,
        dm = dm,
        intermediate = im,
        str_dm = string_matrix[1:,1]
    )
    
    return point


def parser (filename1, filename2, trigonometric=""):
    
    
    
    libreta_string_matrix = np.genfromtxt(filename1, delimiter=',', dtype=str, skip_header=0,invalid_raise=False)
    height_string_matrix  = np.genfromtxt(filename2, delimiter=',', dtype=str, skip_header=0,invalid_raise=False)
    
    libreta_num_matrix = np.round(np.genfromtxt(filename1, delimiter=',', skip_header=0,invalid_raise=False),3)
    height_num_matrix =  np.round(np.genfromtxt(filename2, delimiter=',', skip_header=0,invalid_raise=False),3)

    if trigonometric:
        trig_table = utils.normalize_fstring_array ( # Trig table is normalized
            np.genfromtxt(
                trigonometric,
                delimiter=',',
                dtype=str,
                skip_header=0,
                invalid_raise=False
            )
        )
    else:
        trig_table = np.array([])
    
    
    pro = parse_circuit(libreta_string_matrix, height_string_matrix,
                  circuit_num_matrix=libreta_num_matrix,
                  pr_num_matrix=height_num_matrix)
 
    positive_segments = []
    negative_segments = []
 
    for seg in pro:
        if seg.positive:
            positive_segments.append(seg)
        else: 
            negative_segments.append(seg)
 
    return Circuit(
        positive_segments,
        negative_segments,
        trigonometric = trig_table if trigonometric else None)








    


if __name__ == "__main__":
    f1 = sys.argv[0]
    f2 = sys.argv[1]
    f3 = sys.argv[2]
    cir = parser(f1,f2,f3)
    cir.write_circuit_table("REPORT.csv")
