import writeConfig
import json
import os


matNo = [1335, 300, 2170, 410]
pageNo = [1046, 3154, 1466, 3230]
# matNo = [1946, 238, 2257, 304]	# mat no  region box on image
# pageNo = [1088, 3219, 1391, 3276]	# page no  region box on image
candidates = ['2488853', '248885343', '123456789', '1234567', '1234767', '4822636', '1597839',]

writeConfig.addParam('ws 2017/2018', matNo, pageNo) 
writeConfig.addCandidates(candidates)

writeConfig.addQuestion(['1.1', '1', 352, 1022, 2098, 1330])
writeConfig.addQuestion(['1.2', '1', 358, 1738, 2102, 2040])
writeConfig.addQuestion(['1.3', '1', 366, 2686, 2108, 2988])
writeConfig.addQuestion(['2.1', '2', 352, 1026, 2098, 1328])
writeConfig.addQuestion(['2.2', '2', 362, 1738, 2098, 2038])
writeConfig.addQuestion(['2.3', '2', 366, 2684, 2108, 2984])


writeConfig.saveConfig()


if __name__ == '__main__':
	fileName = os.path.join(os.pardir, 'config.json')
	with open(fileName, 'r') as file:
		configData = json.load(file)
	print(configData)




