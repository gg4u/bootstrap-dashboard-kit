from py2neo import Graph, NodeMatcher
from py2neo.data import Node, Relationship

graph = Graph(password="test")
matcher = NodeMatcher(graph)



def init_db():
	graph.run("CREATE CONSTRAINT user_address IF NOT EXISTS FOR (n:User) REQUIRE n.id IS UNIQUE")
	graph.run("CREATE CONSTRAINT resource_address IF NOT EXISTS FOR (n:Resource) REQUIRE n.id IS UNIQUE")
	graph.run("CREATE CONSTRAINT process_address IF NOT EXISTS FOR (n:Process) REQUIRE n.id IS UNIQUE")

init_db()


def create_user(userId, name):
    graph.run("MERGE (n:User {id: $userId, name: $name})",
    	userId=userId, name=name)

def user_create_contract(userId, nodeId, nodeType, relType):
	#normalise nodeType
	#TODO

    graph.run("MATCH (a:User) WHERE a.id = $userId "
           "MERGE (a)-[:"+ relType +"]->(:" + nodeType + "{id: $nodeId})",
           userId=userId, nodeId=nodeId)

def update_contract_props(nodeId, nodeType, data):
	# data is a dictionary (not nested)
	node = matcher.match( nodeType, id=nodeId).first()
	for k, v in data.items():
		node[k] = v
	graph.push(node)

def contract_create_contract(fromId, toId, nodeType, relType):
	#normalise nodeType
	#TODO

    graph.run("MATCH (a:Process) WHERE a.id = $fromId "
           "MERGE (a)-[:" + relType + "]->(:" + nodeType + "{id: $toId})",
           fromId=fromId, toId=toId)

def create_relationship(u, v, typeRelationship):
	rel = Relationship(u, typeRelationship, v)
	graph.merge(rel)





# create a user
create_user(userId="32893", name="pippo")

# user create a resource
user_create_contract(userId="32893", nodeId="32", nodeType="Resource", relType="use")
update_contract_props(nodeId="32", nodeType="Resource", data={
		"name" : "impedence calculator",
		"what" : "A script to calculate impedence "
		})

# user create a process
user_create_contract(userId="32893", nodeId="74387", nodeType="Process", relType="create")
update_contract_props(nodeId="74387", nodeType="Process", data={
		"what" : " ",
		"why" : " ",
		"how" : " ",
		"expected_output" : " ",
		"expected_outcome" : " "
		})

#process create output
contract_create_contract(fromId="74387", toId="289923", nodeType="Resource", relType="create")
u = matcher.match("Process", id="74387").first()
v = matcher.match("Resource", id="32").first()
create_relationship(v, u, "input")

