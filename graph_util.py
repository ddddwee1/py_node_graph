typeDict = {'sampleNode':[['Attr1','Attr2'],{'Attr1':{'hasPlug':True,'hasSocket':True}, 'Attr2':{'hasPlug':True,'hasSocket':False}},'pass']}

typeDict['convNode'] = [['Input','Output'],{'Input':{'hasPlug':False,'hasSocket':True}, 'Output':{'hasPlug':True,'hasSocket':False}},'convLayer']

typeDict['addNode'] = [['Input1','Input2','Output'],{'Input1':{'hasPlug':False,'hasSocket':True}, 'Input2':{'hasPlug':False,'hasSocket':True}, 'Output':{'hasPlug':True,'hasSocket':False}},'tf.add']

typeDict['finalNode'] = [['Input'],{'Input':{'hasPlug':False,'hasSocket':True}},'return']

typeDict['startNode'] = [['Output'],{'Output':{'hasPlug':True,'hasSocket':False}},'tf.placeholder']
