import pandas as pd
from datetime import datetime

class Row:
    def __init__(self, table_path, row_number):
        self.main_data = pd.read_csv(table_path)
        self.row_number = row_number
        self.id = self.get_id()
        self.data = self.get_df_dict()
        self.answer = self.get_test_answer()
        
    def get_df_dict(self):
        data = self.main_data.iloc[self.row_number - 2, :]
        data = data.dropna().to_dict()
        data.update({'id': self.id})
        return data

    def get_test_answer(self):
        lst = []
        columns = list(self.data.keys()).copy()
        for column_name in columns:
            if column_name[0].isdigit() and column_name[1] == '.':
                tmp = int(self.data[column_name][0])
                lst.append(tmp)
                
                del self.data[column_name]
        return lst

    def get_id(self):
        other_dates = self.main_data['dt_created'].apply(
            lambda a: pd.Timestamp(datetime.strptime(str(a)[:10], "%Y-%m-%d")) if isinstance(a, str) and a[0].isdigit() else pd.NaT
        )
        created_date = self.main_data.iloc[self.row_number - 2, :]['dt_created']
        source = pd.Timestamp(datetime.strptime(str(created_date)[:10], "%Y-%m-%d"))
        d = source.day
        m = source.month
        y = source.year
        date_list = other_dates[other_dates.dt.month == m].reset_index()
        date_list = date_list['dt_created']
        inx = date_list[date_list == source].index[0]
        idd = str(d).rjust(2, '0') + str(m).rjust(2, '0') + str(y)[2:] + str(inx + 1) + 'SE'
        return idd

if __name__ == '__main__':
    row = Row('https://docs.google.com/spreadsheets/d/1hgC7-TI2INK2ZIU7gv82hALETcOnI35iRny5I3oV2KE/export?format=csv&gid=673713785',30)
    print(row.data, row.answer)
