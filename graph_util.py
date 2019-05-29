typeDict = {}
typeDict['convNode'] = [
							['x', 'out'],
							{
								'x':{'hasPlug':False, 'hasSocket':True},
								'out':{'hasPlug':True, 'hasSocket':False}
							},
							{
								'intrinsic':{
									'size':3,
									'outchn':16,
									'stride':1,
									'pad':'SAME',
									'dilation_rate':1,
									'usebias':True,
									'batch_norm':False,
									'activation':1
								},
								'CodeInit':[
									'%s = M.ConvLayer(size=%d, outchn=%d, stride=%d, pad="%s", dilation_rate=%d, usebias=%d, batch_norm=%d, activation=%d)',
									'__layerdef',
									'size',
									'outchn',
									'stride',
									'pad',
									'dilation_rate',
									'usebias',
									'batch_norm',
									'activation'
								],
								'CodeForward':[
									'%s = self.%s(%s)',
									'__layerout',
									'__layerdef',
									'x'
								]
							}
						]

typeDict['outNode'] = [
							['x'],
							{
								'x':{'hasPlug':False, 'hasSocket':True}
							},
							{
								'CodeForward':[
									'return %s',
									'x'
								]
							}

						]

typeDict['inNode'] = [
							['x'],
							{
								'x':{'hasPlug':True, 'hasSocket':False}
							},
							{}

						]

