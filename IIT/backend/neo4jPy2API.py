from py2neo import Graph, NodeMatcher
from py2neo.data import Node, Relationship


class Topology:

	def __init__(self, password):
		self.graph = Graph(password= password)
		self.matcher = NodeMatcher(self.graph)

	def init_db(self):
		self.graph.run("CREATE CONSTRAINT user_address IF NOT EXISTS FOR (n:User) REQUIRE n.id IS UNIQUE")
		self.graph.run("CREATE CONSTRAINT resource_address IF NOT EXISTS FOR (n:Resource) REQUIRE n.id IS UNIQUE")
		self.graph.run("CREATE CONSTRAINT process_address IF NOT EXISTS FOR (n:Process) REQUIRE n.id IS UNIQUE")

	def create_user(self, userId, name):
		self.graph.run("MERGE (n:User {id: $userId, name: $name})",
			userId=userId, name=name)

	def user_create_contract(self, userId, nodeId, nodeType, relType):
		#normalise nodeType
		#TODO

		self.graph.run("MATCH (a:User) WHERE a.id = $userId "
			   "MERGE (a)-[:"+ relType +"]->(:" + nodeType + "{id: $nodeId})",
			   userId=userId, nodeId=nodeId)

	def update_contract_props(self, nodeId, nodeType, data):
		# data is a dictionary (not nested)
		node = self.matcher.match( nodeType, id=nodeId).first()
		for k, v in data.items():
			node[k] = v
		self.graph.push(node)

	def contract_create_contract(self, fromId, toId, nodeType, relType):
		#normalise nodeType
		#TODO

		self.graph.run(
				"MERGE (a:Process {id : $fromId})"
				"MERGE (b:"+ nodeType + "{id : $toId})"
			   	"MERGE (a)-[:" + relType + "]->(b)",
			   fromId=fromId, toId=toId)

	def create_relationship(self, u, v, typeRelationship):
		rel = Relationship(u, typeRelationship, v)
		self.graph.merge(rel)

	# high level API - Was it simpler the first version?
	def user_create_resource(self, userId, resourceId, data):
		print('user', userId)
		self.user_create_contract(userId = userId, nodeId = resourceId, nodeType="Resource", relType="use")
		self.update_contract_props(nodeId= resourceId, nodeType="Resource", data= data)

	def user_create_process(self, userId, inputIds, processId, data):
		'''
		User does:
			select inputs
			describe process
			describe output

		Process returns:
			ouput
			There is only 1 output per process.


		The transaction tracks the KPIs of the whole project. 
		'''

		# create process
		self.user_create_contract(userId = userId, nodeId = processId, nodeType="Process", relType="output")
		self.update_contract_props(nodeId= processId, nodeType="Process", data= data)

		# links it with inputs
		v = self.matcher.match( "Process", id = processId).first()
		for inputId in inputIds:
			u = self.matcher.match( "Resource", id=inputId).first()
			self.create_relationship(u, v, "input")

		# return processId
		return processId


	def process_create_output(self, processId, resourceId, data):
		self.contract_create_contract(fromId = processId, toId = resourceId, nodeType="Resource", relType="output")
		self.update_contract_props(nodeId= resourceId, nodeType="Resource", data= data)

