typeDict = {'sampleNode':[['Attr1','Attr2'],{'Attr1':{'hasPlug':True,'hasSocket':True}, 'Attr2':{'hasPlug':True,'hasSocket':False}}]}

typeDict['convNode'] = [['Input','Output'],{'Input':{'hasPlug':False,'hasSocket':True}, 'Output':{'hasPlug':True,'hasSocket':False}}]

typeDict['addNode'] = [['Input1','Input2','Output'],{'Input1':{'hasPlug':False,'hasSocket':True}, 'Input2':{'hasPlug':False,'hasSocket':True}, 'Output':{'hasPlug':True,'hasSocket':False}}]

typeDict['fusionNode3'] = [['Input1','Input2','Input3','Output'],{'Input1':{'hasPlug':False,'hasSocket':True}, 'Input2':{'hasPlug':False,'hasSocket':True}, 'Input3':{'hasPlug':False,'hasSocket':True}, 'Output':{'hasPlug':True,'hasSocket':False}}]

typeDict['finalNode'] = [['Input'],{'Input':{'hasPlug':False,'hasSocket':True}}]

typeDict['startNode'] = [['Output'],{'Output':{'hasPlug':True,'hasSocket':False}}]
