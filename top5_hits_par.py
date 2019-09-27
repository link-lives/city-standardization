#This is the script I used to "parallelize" the selection of the top 5 matches per potential matches
import pandas as pd
import numpy as np
import sys
import os

_from = int(sys.argv[1])
_to = int(sys.argv[2])
_top = 5 #Top what? sys.argv[1]
THRESHOLD = 0.9

if os.path.isfile('/home/roregu/workspace/tmp/concatenate_'+str(_from)+'_'+str(_to)+'.tsv'):
    print('done')
    exit()

distance_jaro = pd.read_csv('/home/roregu/workspace/aux.tsv', sep = '\t', usecols=[0]+list(np.arange(_from,_to)), index_col=0 )

#print(distance_jaro.head())

concatenate = []
i=0
for col in distance_jaro.columns:
    i = i+1
    #if i % 100 == 0: print(i, 'out of', len(distance_jaro.columns))
    aux = distance_jaro.nlargest(5, col)[[col]]
    aux.columns = ['score']
    aux['original'] = col
    concatenate.append(aux)

#print(concatenate)
concatenate = pd.concat(concatenate, sort=False)
concatenate = concatenate.reset_index()
concatenate.columns = ['potential_match','score','original']
#print(concatenate)
concatenate[['original','potential_match','score']][~concatenate.original.isin(concatenate[(concatenate.score >= THRESHOLD) & ~concatenate.original.isna()].original.unique())].to_csv('/home/roregu/workspace/tmp/concatenate_'+str(_from)+'_'+str(_to)+'.tsv', index=False, sep='\t')

print('done_'+str(_from)+'_'+str(_to))

exit()