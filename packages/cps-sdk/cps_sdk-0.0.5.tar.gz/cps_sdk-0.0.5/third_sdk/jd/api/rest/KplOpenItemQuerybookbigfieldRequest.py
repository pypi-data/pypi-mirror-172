from third_sdk.jd.api.base import RestApi

class KplOpenItemQuerybookbigfieldRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.skus = None

		def getapiname(self):
			return 'jd.kpl.open.item.querybookbigfield'

		def get_version(self):
			return '1.0'
			
	




