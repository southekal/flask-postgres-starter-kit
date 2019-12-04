from hashids import Hashids


def generate_hashid(salt, id):
	hashids = Hashids(min_length=6, salt=salt)
	hashid = hashids.encode(int(id))
	return hashid


def decode_hashid(salt, hashid):
	hashids = Hashids(min_length=6, salt=salt)
	hashid = hashids.decode(hashid)
	return hashid


def generate_hashid_dict(salt, list_of_ids):
	hashids = {}
	for _id in list_of_ids:
		hashids[_id] = generate_hashid(salt=salt, id=_id)

	return hashids
