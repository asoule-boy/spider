import requests
from lxml import etree

class BusSpider(object):
    def __init__(self):
        self.header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
        self.first_url = "https://wuhan.8684.cn/"
    
    def requestBus(self,url):
        r = requests.get(url,headers=self.header)
        return r.text
    
    def select_startwith_Road(self):
        tree = etree.HTML(self.requestBus(self.first_url))
        nummber_bus_route_href = tree.xpath("//div[@class='bus_kt_r1']/a/@href")
        chr_bus_route_href = tree.xpath("//div[@class='bus_kt_r2']/a/@href")
        bus_route_href = nummber_bus_route_href + chr_bus_route_href
        bus_route_url = map(lambda x:self.first_url + x,bus_route_href)
        return bus_route_url
    
    def select_specific_road(self,second_url):
        second_tree = etree.HTML(self.requestBus(second_url))
        specific_bus_href = second_tree.xpath("//div[@id='con_site_1']/a/@href")
        specific_bus_url = map(lambda x:self.first_url + x,specific_bus_href)
        return specific_bus_url
    
    def get_specific_bus_info(self,third_url):
        third_tree = etree.HTML(self.requestBus(third_url))
        bus_route = third_tree.xpath("//div[@class='bus_i_t1']/h1/text()")[0].replace("&nbsp","")
        work_time = third_tree.xpath("//p[@class='bus_i_t4'][1]/text()")[0]
        bus_price = third_tree.xpath("//p[@class='bus_i_t4'][2]/text()")[0]
        bus_station_1 = third_tree.xpath("//div[@class='bus_line_site '][1]/div/div/a/text()")
        bus_station_2 = third_tree.xpath("//div[@class='bus_line_site '][2]/div/div/a/text()")
        self.__print_bus_info(bus_route,work_time,bus_price,bus_station_1,bus_station_2)
        
    
    def __print_bus_info(self,bus_route,work_time,bus_price,bus_station_1,bus_station_2):
        print("*****************", bus_route, "******************")
        print(work_time)
        print(bus_price)
        print("**公交站点信息:", bus_station_1[0], "--->", bus_station_1[-1],"(共%d站)"%len(bus_station_1))
        print("—>".join(bus_station_1))
        if bus_station_2 != []:
            print("**公交站点信息:", bus_station_2[0], "--->", bus_station_2[-1],"(共%d站)"%len(bus_station_2))
            print("—>".join(bus_station_2))
        print("\n")
        
    def main(self):
        second_url_list = self.select_startwith_Road()
        for second_url in second_url_list:
            third_url_list = self.select_specific_road(second_url)
            for third_url in third_url_list:
                self.get_specific_bus_info(third_url)
    
 
if __name__ == '__main__':
    busSpider = BusSpider()
    busSpider.main()