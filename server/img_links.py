

def test_result_img(self):
        result = []
        for i in range(1, len(self.test_result) + 1):
            data1 = self.test_result[i]['meta']
            lower_bound_value = self.test_result[i]['level'][1] // 10
            upper_bound_value = self.test_result[i]['level'][2] // 10
            lower_ttl = self.test_result[i]['level'][3]
            upper_ttl = self.test_result[i]['level'][4]
            result.append(self.plot_radar_chart(data1, lower_bound_value, upper_bound_value, lower_ttl, upper_ttl))
        result.append(self.plot_bar_chart_with_annotations())
        print('Графики на сервере!')
        return result