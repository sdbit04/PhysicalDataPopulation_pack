import csv
from pyxlsb import *


class AntennaDataReader(object):

    def __init__(self, technology):
        self.technology = technology
        if self.technology.upper() == 'UMTS':
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            self.SD_fields_need_to_update = ['RNC Id', 'Sector Name', 'NodeB Longitude', 'NodeB Latitude',
                                             'Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt',
                                             'Azimuth']
            # TODO:Sometime 'Sector name' is populated as 'eNodeBname' in planner file. then the 2nd element
            # in the below list will be changed
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            self.planner_fields_required = ['RNC Id', 'Sector Name', 'eNodeB Longitude', 'eNodeB Latitude',
                                            'Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt',
                                            'Azimuth', 'Antenna Model', 'Antenna Tilt-Electrical']
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            self.cgi_file_fields_required = ['LTE CGI', 'dummy', 'Longitude', 'Latitude', 'Longitude', 'Latitude',
                                             'Antenna Height (m)', 'Antenna Tilt-Mechanical', 'Azimuth',
                                             'Antenna  Model', 'Antenna Tilt-Electrical', 'Band',
                                             'Status Active / Locked', 'Site Type']
            self.lte_carrier_fields_required = ['RNC', 'Sector Name']

        elif self.technology.upper() == 'LTE':
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            self.SD_fields_need_to_update = ['RNC Id', 'Sector Name', 'NodeB Longitude', 'NodeB Latitude','Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model']
            # TODO:Sometime 'Sector name' is populated as 'eNodeBname' in planner file. then the 2nd element
            # in the below list will be changed
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            self.planner_fields_required = ['TAC id', 'Sector Name', 'eNodeB Longitude', 'eNodeB Latitude','Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model', 'Antenna Tilt-Electrical']
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            self.cgi_file_fields_required = ['LTE CGI', 'dummy', 'Longitude', 'Latitude', 'Longitude', 'Latitude',                       'Antenna Height (m)', 'Antenna Tilt-Mechanical', 'Azimuth', 'Antenna  Model', 'Antenna Tilt-Electrical', 'Band', 'Status Active / Locked', 'Site Type']
            self.lte_carrier_fields_required = ['TAC', 'Sector Name', 'MCC', 'MNC', 'Sector Carrier Name']
        else:
            raise ("{} technology is not supported ".format(self.technology))

    def __validate_fields(self, csv_sd_planner_path):
        # csv_sd_planner_path = csv_sd_planner_path
        if self.technology.upper() == 'UMTS':
            # check if all the fields at SD_fields_need_to_update are into the file
            return True
        elif self.technology.upper() == 'LTE':
            # check if all the fields at SD_fields_need_to_update are into the file
            return True

    def __read_csv_sd(self, csv_sd_path):
        """
        read planner file and return a dictionary having RNC-ID and Sector-name as key for each row of the input csv
        :param csv_sd_path:
        :param separator:
        :return:
        """
        # TODO at present I have only UMTS data
        sd_dict_out = {}
        with open(csv_sd_path, mode='r', encoding='utf-8') as sd_ob:
            # As we know the delimiter for parsed SD antennas.txt is tab, So I made it hard coded
            sd_dict = csv.DictReader(sd_ob, delimiter='\t')
            for row in sd_dict:
                rnc_id_sector_key = "{}-{}".format(row[self.SD_fields_need_to_update[0]],
                                                   row[self.SD_fields_need_to_update[1]])
                sd_dict_out[rnc_id_sector_key] = row
            return sd_dict_out

    def __read_csv_planner(self, csv_planner_path):
        """
        read planner file and return a dictionary having RNC-ID and Sector-name as key for each row of the input csv
        :param csv_planner_path:
        :param separator:
        :return:
        """
        planner_dict_out = {}
        try:
            with open(csv_planner_path, mode='r') as sd_ob:
                # , encoding='utf-8'
                # As we convert the planner.xlsx file into a tab delimited file, So I made it hard coded in next line
                sd_dict = csv.DictReader(sd_ob, delimiter='\t')
                for row in sd_dict:
                    rnc_id_sector_key = "{}-{}".format(row[self.planner_fields_required[0]],
                                                       row[self.planner_fields_required[1]])
                    # Insert data into dict, having rnc_id_sector_key as key for each top level dict item
                    planner_dict_out[rnc_id_sector_key] = row
                return planner_dict_out
        except UnicodeDecodeError:
            with open(csv_planner_path, mode='r', encoding='utf-8') as sd_ob:
                sd_dict = csv.DictReader(sd_ob, delimiter='\t')
                for row in sd_dict:
                    rnc_id_sector_key = "{}-{}".format(row[self.planner_fields_required[0]],
                                                       row[self.planner_fields_required[1]])
                    # Insert data into dict, having rnc_id_sector_key as key for each top level dict item
                    planner_dict_out[rnc_id_sector_key] = row
                return planner_dict_out

    def read_sd_antennas_file(self, sd_file_path):
        if self.__validate_fields(sd_file_path):
            sd_dict_out = self.__read_csv_sd(sd_file_path)
            return sd_dict_out
        else:
            raise NotImplementedError("SD input file was not valid, should be in tab separated csv file")

    def read_planner_file(self, planner_file_path):
        if self.__validate_fields(planner_file_path):
            planner_dict_out = self.__read_csv_planner(planner_file_path)
            return planner_dict_out
        else:
            raise NotImplementedError("Planner Input file was not valid, should be in tab separated csv file")

    def read_lte_carrier(self, lte_carrier_path):
        lte_carrier_dict_out = {}
        try:
            with open(lte_carrier_path, 'r') as lte_carrier_ob:
                lte_carrier_dict = csv.DictReader(lte_carrier_ob, delimiter='\t')
                # print(lte_carrier_dict.__next__())
                for row in lte_carrier_dict:
                    lte_carrier_rncid_sector_key = "{}-{}".format(row[self.lte_carrier_fields_required[0]],
                                                                  row[self.lte_carrier_fields_required[1]])
                    # TODO In the line below, I have assigned whole row to the key, I can only assign required fields
                    lte_carrier_dict_out[lte_carrier_rncid_sector_key] = row
            return lte_carrier_dict_out
        except:
            raise Exception("Lte_carrier file was not readable")

    def read_gsi_file(self, cgi_file_path):
        file_path = cgi_file_path
        col_name_position = {}
        data_dict = {}
        with open_workbook(file_path) as GSI_file:
            sheet = GSI_file.get_sheet(1)  # Index of first row is 1
            rows_iter = iter(sheet.rows())
            head_row = next(rows_iter)  # Header record only
            for cell in head_row:  # Speed linearly depends on number of columns into the GSI file
                if cell.v == self.cgi_file_fields_required[0]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[1]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[2]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[3]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[4]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[5]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[6]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[7]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[8]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[9]:
                    col_name_position[cell.v] = cell.c
                elif str(cell.v).__contains__(self.cgi_file_fields_required[10]):
                    print(str(cell.v))
                    col_name_position[self.cgi_file_fields_required[10]] = cell.c
                else:
                    pass
            # Following statement will print the header with their column position as key:value pair
            print(col_name_position)

            for row in rows_iter:  # accessing all data rows
                col_name_data = {}  # dict for each data row
                # print(row[3])  ==>  Cell(r=1, c=3, v='EKOL0000KONG')

                for col_name, position in col_name_position.items():  # Seems a quadratic, but this iteration is
                    # constant in count
                    cell = row[position]  # getting the cell using cell_position as an index of row, it is a constant
                    # time operation, output like -> Cell(r=1, c=3, v='EKOL0000KONG')
                    col_name_data[col_name] = cell.v
                data_dict["{0}".format(col_name_data[self.cgi_file_fields_required[0]])] = col_name_data
        return data_dict


if __name__ == "__main__":
    CGI_file = "D:\\D_drive_BACKUP\\Study\\PycharmProjects\\PhysicalDataPopulation\\Input_data_deep\\New\\4G GIS Data Kolkata.xlsb"
    lte_carrier = \
        "D:\\D_drive_BACKUP\\Study\\PycharmProjects\\PhysicalDataPopulation\\Input_data_deep\\New\\lte-carriers.txt"

    reader = AntennaDataReader(technology='LTE')
    lte_carrier_dict_out_r = reader.read_lte_carrier(lte_carrier_path=lte_carrier)
    print(lte_carrier_dict_out_r)
    for value in lte_carrier_dict_out_r.values():
        temp_l1 = str(value['Sector Carrier Name']).split('-')
        print('{0}-{1}-{2}-{3}'.format(value['MCC'], value['MNC'], temp_l1[1], temp_l1[2]))


    # cgi_file_dict = reader.read_gsi_file(CGI_file)
    # with open("cgi_file.json", 'a') as cgi_out_ob:
    #     print(cgi_file_dict, file=cgi_out_ob)


