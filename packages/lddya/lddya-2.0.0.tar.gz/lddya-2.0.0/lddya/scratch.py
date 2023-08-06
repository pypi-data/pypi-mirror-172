from Algorithm import ACO
from Draw import ShanGeTu,IterationGraph
from Map import Map

map = Map()    
map.load_map_file('map.dll')
aco = ACO(map_data=map.data)
aco.run()
sfig = ShanGeTu(map.data)
sfig.draw_way(aco.way_data_best)
sfig.save()
dfig = IterationGraph([aco.generation_aver,aco.generation_best],
                    style_list=['--r','-.g'],
                    legend_list=['1','2'])
dfig.save()



