import pstats
p = pstats.Stats('pop.out')

p.sort_stats('cumulative').print_stats(5)