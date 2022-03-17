import datetime
import hashlib

class Block(object):
	"""docstring for Block"""
	def __init__(self, id, timestamp, data, prevHash):
		super(Block, self).__init__()
		self.id = id
		self.timestamp = timestamp
		self.data = data
		self.prevHash = prevHash
		self.hash = self.hashblock()

	def hashblock(self):
		args = ''.join(list(map(str, [self.id, self.timestamp, self.data, self.prevHash]))).encode('utf-8')
		print(args)

		Encrypt = hashlib.sha256()
		Encrypt.update(args)
		return Encrypt.hexdigest()

	#first block is unmutable and declared indepent from instantiation of the blockchain
	@staticmethod
	def genesis():
		return Block(0, datetime.datetime.now(), 'genesis block transaction', '')

	@staticmethod
	def nextblock(lastBlock):
		id = lastBlock.id + 1
		timestamp = datetime.datetime.now()
		prevHash = lastBlock.hash
		data = 'Transaction {}'.format(id)
		return Block(id, timestamp, data, prevHash)


#init blockchain
blockchain = [Block.genesis()] 
prevblock = blockchain[0]


# let's print the genesis block information
print('Block ID # {} '.format(prevblock.id))
print ("Timestamp:{}".format(prevblock.timestamp))
print ("Hash of the block:{}".format(prevblock.hash))
print ("Previous Block Hash:{}".format(prevblock.hash))
print ("data:{}\n".format(prevblock.data))


for i in range (0,5): # the loop starts from here, we will need only 5 blocks in our ledger for now, this number can be increased
	addblock = Block.nextblock(prevblock) #  the block to be added to our chain 
	blockchain.append(addblock) # we add that block to our chain of blocks
	prevblock = addblock #now the previous block becomes the last block so we can add another one if needed

	print('Block ID # {} '.format(addblock.id))
	print ("Timestamp:{}".format(addblock.timestamp))
	print ("Hash of the block:{}".format(addblock.hash))
	print ("Previous Block Hash:{}".format(addblock.hash))
	print ("data:{}\n".format(addblock.data))
